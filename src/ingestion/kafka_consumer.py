from confluent_kafka import Consumer, KafkaError
import psycopg2
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kafka-consumer")

# Kafka and PostgreSQL configuration
KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "stock_data.trades")
POSTGRES_CONN_STRING = os.getenv("POSTGRES_CONN_STRING")

# Initialize Kafka Consumer
consumer = Consumer({
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVER,
    'group.id': 'postgres-consumer-group',
    'auto.offset.reset': 'earliest',
})
consumer.subscribe([KAFKA_TOPIC])

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(POSTGRES_CONN_STRING)
    cur = conn.cursor()
    logger.info("Connected to PostgreSQL successfully.")
except Exception as e:
    logger.error(f"Error connecting to PostgreSQL: {e}")
    exit(1)

def process_message(msg):
    try:
        # Parse message and insert into PostgreSQL
        data = eval(msg.value().decode('utf-8'))
        insert_query = """
        INSERT INTO stock_data_raw (symbol, price, size, timestamp)
        VALUES (%s, %s, %s, %s)
        """
        cur.execute(insert_query, (data['symbol'], data['price'], data['size'], data['timestamp']))
        conn.commit()
        logger.info(f"Inserted data into PostgreSQL: {data}")
    except Exception as e:
        logger.error(f"Failed to process message {msg.value()}: {e}")

try:
    logger.info("Starting Kafka Consumer...")
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                logger.error(f"Kafka error: {msg.error()}")
                break
        process_message(msg)
finally:
    # Cleanup
    consumer.close()
    cur.close()
    conn.close()
    logger.info("Kafka Consumer shutdown complete.")
