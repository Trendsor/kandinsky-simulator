import os
import json
import asyncio
import logging
from kubernetes import client, config
from alpaca.data.live.stock import StockDataStream
from confluent_kafka import Producer

# Logging setup
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("alpaca-producer")

# Load Kubernetes configuration (assumes this runs in-cluster)
config.load_incluster_config()

# Environment Variables
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "stock_data.trades")
KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER")
BROKER_API_KEY = os.getenv("BROKER_API_KEY")
BROKER_API_SECRET = os.getenv("BROKER_API_SECRET")
BROKER_API_URL = os.getenv("BROKER_API_URL", "wss://stream.data.alpaca.markets/v2")
NAMESPACE = os.getenv("NAMESPACE", "trading-bot-ingestion")
SYMBOLS = os.getenv("SYMBOLS", "AAPL,TSLA").split(",")  # Default symbols to track

# Kubernetes API client
v1 = client.CoreV1Api()

# Helper functions for session lock management
def get_session_status():
    """Retrieve the session lock status from Kubernetes ConfigMap."""
    try:
        config_map = v1.read_namespaced_config_map("websocket-session-lock", NAMESPACE)
        return config_map.data.get("session_status", "unlocked")
    except Exception as e:
        logger.error(f"Failed to read session lock status: {e}")
        return "unlocked"

def update_session_status(status):
    """Update the session lock status in Kubernetes ConfigMap."""
    try:
        config_map = client.V1ConfigMap(
            data={"session_status": status},
            metadata=client.V1ObjectMeta(name="websocket-session-lock", namespace=NAMESPACE)
        )
        v1.replace_namespaced_config_map("websocket-session-lock", NAMESPACE, config_map)
        logger.info(f"Session status updated to: {status}")
    except Exception as e:
        logger.error(f"Failed to update session status: {e}")

# Kafka producer setup
producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVER})

async def trade_handler(data):
    """
    Handles trade data received from Alpaca WebSocket and sends it to Kafka.

    Args:
        data: Trade data from Alpaca WebSocket.
    """
    try:
        trade_data = {
            'symbol': data.symbol,
            'price': float(data.price),
            'size': int(data.size),
            'timestamp': str(data.timestamp)
        }
        logger.info(f"Received trade data: {trade_data}")

        # Send data to Kafka
        producer.produce(KAFKA_TOPIC, value=json.dumps(trade_data).encode('utf-8'))
        producer.flush()
        logger.info(f"Sent trade data to Kafka topic {KAFKA_TOPIC}")
    except Exception as e:
        logger.error(f"Failed to process trade data: {e}")

async def start_alpaca_stream():
    """
    Starts the Alpaca WebSocket stream and subscribes to trades for configured symbols.
    """
    logger.info("Setting up Alpaca WebSocket stream.")
    stream = StockDataStream(api_key=BROKER_API_KEY, secret_key=BROKER_API_SECRET, url_override=BROKER_API_URL)

    # Subscribe to trade streams for the configured symbols
    for symbol in SYMBOLS:
        logger.info(f"Subscribing to trade data for symbol: {symbol}")
        stream.subscribe_trades(trade_handler, symbol)

    try:
        logger.info("Running Alpaca WebSocket stream.")
        await stream.run()
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        raise

def main():
    """
    Main function to manage WebSocket session and send trade data to Kafka.
    """
    if get_session_status() == "unlocked":
        logger.info("No active session found. Locking session and starting WebSocket.")
        update_session_status("locked")

        try:
            asyncio.run(start_alpaca_stream())
        except KeyboardInterrupt:
            logger.info("WebSocket stream interrupted. Cleaning up.")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
        finally:
            logger.info("Releasing session lock.")
            update_session_status("unlocked")
    else:
        logger.info("An active WebSocket session is already running. Exiting.")

if __name__ == "__main__":
    main()
