import os
import json
from kubernetes import client, config
from alpaca.data.live.stock import StockDataStream
from confluent_kafka import Producer
import time
import logging
logging.basicConfig(level=logging.DEBUG)

# Load Kubernetes configuration (assumes this runs in-cluster)
config.load_incluster_config()

# Set up Kafka and Alpaca configurations
KAFKA_TOPIC = "stock_data.trades"
KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER")
BROKER_API_KEY = os.getenv("BROKER_API_KEY")
BROKER_API_SECRET = os.getenv("BROKER_API_SECRET")
BROKER_API_URL = os.getenv("BROKER_API_URL", "wss://stream.data.alpaca.markets/v2")
NAMESPACE = os.getenv("NAMESPACE", "trading-bot-ingestion")

# Initialize Kubernetes API client
v1 = client.CoreV1Api()

# Helper function to get the session lock status
def get_session_status():
    config_map = v1.read_namespaced_config_map("websocket-session-lock", NAMESPACE)
    return config_map.data.get("session_status", "unlocked")

# Helper function to update the session lock status
def update_session_status(status):
    config_map = client.V1ConfigMap(
        data={"session_status": status},
        metadata=client.V1ObjectMeta(name="websocket-session-lock", namespace=NAMESPACE)
    )
    v1.replace_namespaced_config_map("websocket-session-lock", NAMESPACE, config_map)

# Kafka Producer setup
producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVER})

print("Starting Kafka producer and session control script.")

# Check if session is already active
if get_session_status() == "unlocked":
    print("No active session found. Locking session and starting WebSocket.")
    update_session_status("locked")
    
    print("Session locked, setting up WebSocket.")
    # Alpaca WebSocket setup
    stream = StockDataStream(api_key=BROKER_API_KEY, secret_key=BROKER_API_SECRET, url_override=BROKER_API_URL)
    print("WebSocket configured successfully.")
    
    async def trade_handler(data):
        print("Received trade data:", data)
        trade_data = {
            'symbol': data.symbol,
            'price': data.price,
            'size': data.size,
            'timestamp': str(data.timestamp)
        }
        print("Sending data to Kafka:", trade_data)
        producer.produce(KAFKA_TOPIC, value=json.dumps(trade_data).encode('utf-8'))
        producer.flush()

    print("Subscribing to trade stream.")
    stream.subscribe_trades(trade_handler, "FAKEPACA")
    
    try:
        print("Running WebSocket stream.")
        stream.run()
    finally:
        # Ensure the lock is released if the connection is terminated
        print("Releasing session lock.")
        update_session_status("unlocked")
else:
    print("An active WebSocket session is already running. Exiting.")
