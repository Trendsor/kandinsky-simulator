from confluent_kafka import Consumer, KafkaError
import psycopg2
import os

# Kafka and PostgreSQL configuration
KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER")
KAFKA_TOPIC = "raw-stock-data"
POSTGRES_CONN_STRING = os.getenv("POSTGRES_CONN_STRING")  # "dbname='data_ingestion' user='user' password='password' host='postgres-service'"

# Initialize Kafka Consumer
consumer = Consumer({
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVER,
    'group.id': 'postgres-consumer-group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe([KAFKA_TOPIC])

# Connect to PostgreSQL
conn = psycopg2.connect(POSTGRES_CONN_STRING)
cur = conn.cursor()

def process_message(msg):
    # Parse message and insert into PostgreSQL
    data = eval(msg.value().decode('utf-8'))
    insert_query = """
    INSERT INTO stock_data_raw (symbol, price, size, timestamp)
    VALUES (%s, %s, %s, %s)
    """
    cur.execute(insert_query, (data['symbol'], data['price'], data['size'], data['timestamp']))
    conn.commit()

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Error: {msg.error()}")
                break
        process_message(msg)
finally:
    # Cleanup
    consumer.close()
    cur.close()
    conn.close()
