import os
import json
from confluent_kafka import Consumer, Producer, KafkaError

# Kafka Configurations
RAW_TOPIC = "stock_data.trades"
PROCESSED_TOPIC = "processed-stock-data"
BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVER")

# Kafka Consumer
consumer = Consumer({
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'group.id': 'data-processing-group',
    'auto.offset.reset': 'earliest'
})

# Kafka Producer
producer = Producer({'bootstrap.servers': BOOTSTRAP_SERVERS})

def process_data(raw_data):
    """
    Example data transformation:
    Clean, normalize, or feature engineer data.
    """
    processed_data = {
        "symbol": raw_data.get("symbol"),
        "price": float(raw_data.get("price")) * 1.01,  # Example adjustment
        "size": raw_data.get("size"),
        "timestamp": raw_data.get("timestamp"),
        "processed_flag": True
    }
    return processed_data

def handle_message(message):
    try:
        raw_data = json.loads(message.value().decode('utf-8'))
        print(f"Received raw data: {raw_data}")
        
        # Process data
        processed_data = process_data(raw_data)
        print(f"Processed data: {processed_data}")
        
        # Produce to processed topic
        producer.produce(PROCESSED_TOPIC, value=json.dumps(processed_data).encode('utf-8'))
        producer.flush()
    except Exception as e:
        print(f"Error processing message: {e}")

try:
    consumer.subscribe([RAW_TOPIC])
    print("Consumer is listening for raw-stock-data...")
    
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
        handle_message(msg)
finally:
    consumer.close()
