from confluent_kafka import Consumer
from sqlalchemy import create_engine
import json

# PostgreSQL setup
DATABASE_URL = "postgresql://<user>:<password>@<host>:<port>/<database>"
engine = create_engine(DATABASE_URL)

# Kafka Consumer Configuration
consumer = Consumer({
    'bootstrap.servers': "kafka-service:9092",
    'group.id': 'postgres-storage-group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(["stock_data.trades"])

def handle_message(msg):
    data = json.loads(msg.value())
    with engine.connect() as conn:
        conn.execute("INSERT INTO trades (symbol, price, size, timestamp) VALUES (%s, %s, %s, %s)",
                     (data['symbol'], data['price'], data['size'], data['timestamp']))

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    handle_message(msg)

consumer.close()
