import pandas as pd
import psycopg2
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kafka-consumer")

def fetch_historical_data(symbol, limit=200):
    """
    Fetch historical data for a given symbol from the stock_data_raw table.
    
    Args:
        symbol (str): Stock symbol.
        limit (int): Number of recent records to fetch.
        
    Returns:
        pd.DataFrame: Historical data as a pandas DataFrame.
    """

    POSTGRES_CONN_STRING = os.getenv("POSTGRES_CONN_STRING")

    # Connect to PostgreSQL
    try:
        conn = psycopg2.connect(POSTGRES_CONN_STRING)
        logger.info("Connected to PostgreSQL successfully.")
    except Exception as e:
        logger.error(f"Error connecting to PostgreSQL: {e}")
        exit(1)
    query = f"""
        SELECT timestamp, price 
        FROM stock_data_raw 
        WHERE symbol = %s 
        ORDER BY timestamp DESC 
        LIMIT %s
    """
    df = pd.read_sql_query(query, conn, params=(symbol, limit))
    conn.close()
    return df
