import os
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv

# Load environment variables
load_dotenv("dev.env")

BROKER_API_KEY = os.getenv("BROKER_API_KEY")
BROKER_SECRET_KEY = os.getenv("BROKER_SECRET_KEY")
BROKER_API_URL = os.getenv("BROKER_API_URL")

api = tradeapi.REST(BROKER_API_KEY, BROKER_SECRET_KEY, BROKER_API_URL, api_version='v2')

def execute_trade(signal, symbol, quantity=1):
    if signal == 1:
        api.submit_order(symbol=symbol, qty=quantity, side="buy", type="market", time_in_force="gtc")
    elif signal == -1:
        api.submit_order(symbol=symbol, qty=quantity, side="sell", type="market", time_in_force="gtc")
