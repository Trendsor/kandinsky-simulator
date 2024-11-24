import os
from alpaca.data.live.stock import StockDataStream
from dotenv import load_dotenv
import logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv('../../env/dev.env')

# Alpaca WebSocket setup with optional URL
BROKER_API_URL = os.getenv("BROKER_API_URL", "wss://stream.data.alpaca.markets/v2")  # Default to Alpaca's standard endpoint

# Alpaca WebSocket setup
stream = StockDataStream(
    api_key=os.getenv("BROKER_API_KEY"),
    secret_key=os.getenv("BROKER_API_SECRET"),
    url_override=BROKER_API_URL
)

# Handler to print the trade data received from Alpaca
async def trade_handler(data):
    # Adjusted attributes based on FAKEPACA response structure
    trade_data = {
        'symbol': data.symbol,         # Access symbol
        'price': data.price,               # Access price
        'size': data.size,                # Access trade size
        'timestamp': str(data.timestamp)       # Convert timestamp to string if needed
    }
    print(trade_data)  # Print instead of sending to Kafka for testing

# Subscribe to trade updates for a test symbol
stream.subscribe_trades(trade_handler, "FAKEPACA")

# Run the WebSocket stream to start receiving data
stream.run()
