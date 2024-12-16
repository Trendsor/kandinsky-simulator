import alpaca_trade_api as tradeapi

def send_order_to_broker(api_key, secret_key, base_url, symbol, qty, side="buy", order_type="market", time_in_force="gtc"):
    """
    Send an order to Alpaca.

    Args:
        api_key (str): Alpaca API key.
        secret_key (str): Alpaca secret key.
        base_url (str): Alpaca base Url.
        symbol (str): The stock symbol to trade.
        qty (int): Quantity to trade.
        side (str): "buy" or "sell".
        order_type (str): Type of order ("market", "limit", etc.).
        time_in_force (str): Time in force ("day", "gtc", etc.).
    """
    api = tradeapi.REST(api_key, secret_key, base_url, api_version="v2")
    order = api.submit_order(
        symbol=symbol,
        qty=qty,
        side=side,
        type=order_type,
        time_in_force=time_in_force
    )
    return order