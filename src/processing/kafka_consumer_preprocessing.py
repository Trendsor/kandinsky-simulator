import os
import json
import psycopg2
from confluent_kafka import Consumer, Producer, KafkaError
from pipeline import preprocess_data
import logging
import pandas as pd

from src.utils.logging import setup_logger

# Initialize logger
logger = setup_logger(
    name="kafka-consumer-preprocessing",
    log_file="logs/consumer_preprocessing.log",
    level=logging.DEBUG,
    file_log_level=logging.DEBUG,
    console_log_level=logging.INFO,
)

logger.info("Consumer started.")


# Kafka Configurations
RAW_TOPIC = "stock_data.trades"
PROCESSED_TOPIC = "processed-stock-data"
BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVER")

# PostgreSQL Configuration
POSTGRES_CONN_STRING = os.getenv("POSTGRES_CONN_STRING")

# Kafka Consumer
consumer = Consumer({
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'group.id': 'data-processing-group',
    'auto.offset.reset': 'earliest'
})

# Kafka Producer
producer = Producer({'bootstrap.servers': BOOTSTRAP_SERVERS})

def save_to_db(processed_data, conn, cur):
    """
    Save processed data to PostgreSQL.

    Args:
        processed_data (dict): Preprocessed data to be stored.
        conn: Active PostgreSQL connection.
        cur: Cursor for PostgreSQL operations.
    """
    try:
        insert_query = """
        INSERT INTO stock_data_processed (symbol, price, size, timestamp, rolling_mean_200, rolling_std_200, target)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(insert_query, (
            processed_data["symbol"],
            processed_data["price"],
            processed_data["size"],
            processed_data["timestamp"],
            processed_data["rolling_mean_200"],
            processed_data["rolling_std_200"],
            processed_data["target"],
        ))
        conn.commit()
        logger.info(f"Saved processed data to DB: {processed_data}")
    except Exception as e:
        logger.error(f"Failed to save data to DB: {e}")
        conn.rollback()

def handle_message(message, conn, cur):
    """
    Process incoming Kafka messages and save to DB.

    Args:
        message: Kafka message object.
        conn: Active PostgreSQL connection.
        cur: Cursor for PostgreSQL operations.
    """
    logger.info(f"Raw message value: {message.value()}")

    try:
        # Parse the raw message
        raw_data = json.loads(message.value().decode('utf-8'))
        symbol = raw_data.get("symbol")
        logger.info(f"Received raw data for symbol {symbol}: {raw_data}")
        
        # Run the preprocessing pipeline
        processed_data = preprocess_data(raw_data, symbol)
        logger.info(f"Processed data for symbol {symbol}: {processed_data}")
        
        # Extract the latest processed row
        latest_row = processed_data.iloc[-1].to_dict()

        # Convert Timestamp to ISO 8601 string
        if isinstance(latest_row["timestamp"], pd.Timestamp):
            latest_row["timestamp"] = latest_row["timestamp"].isoformat()

        logger.info(f"Latest processed row for symbol {symbol}: {latest_row}")
        
        # Save processed data to DB
        save_to_db(latest_row, conn, cur)

        # Produce processed data to Kafka
        producer.produce(PROCESSED_TOPIC, value=json.dumps(latest_row).encode('utf-8'))
        producer.flush()
    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(POSTGRES_CONN_STRING)
    cur = conn.cursor()

    # Subscribe to Kafka topic
    consumer.subscribe([RAW_TOPIC])
    logger.info(f"Consumer listening on topic: {RAW_TOPIC}")

    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                logger.error(f"Error: {msg.error()}")
                break
        handle_message(msg, conn, cur)

finally:
    consumer.close()
    cur.close()
    conn.close()
