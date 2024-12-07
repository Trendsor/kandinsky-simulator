# from feature_engineering.categorical_processing import process_categorical
from feature_engineering.numerical_processing import process_numerical
# from normalization.scaling import scale_data
# from normalization.encoding import encode_categorical
from normalization.imputation import impute_missing_values
from utils.rolling_buffer import RollingDataBuffer
from utils.fetch_historical_data import fetch_historical_data

# Global buffer instance (for simplicity in this example)
rolling_buffers = {}

def get_or_initialize_buffer(symbol: str, window: int = 200):
    """
    Retrieve or initialize a rolling buffer for a given symbol.

    Args:
        symbol (str): Stock symbol.
        window (int): Rolling window size.

    Returns:
        RollingDataBuffer: Initialized or retrieved rolling buffer.
    """
    global rolling_buffers
    if symbol not in rolling_buffers:
        # Assume initial data is fetched only once for the symbol
        initial_data = fetch_historical_data(symbol, limit=window)
        rolling_buffers[symbol] = RollingDataBuffer(initial_data, window=window)
    return rolling_buffers[symbol]

def preprocess_data(raw_data, symbol: str):
    """
    Complete preprocessing pipeline for incoming data with rolling buffer support.
    
    Args:
        raw_data (dict): Raw input data.
        symbol (str): Stock symbol.

    Returns:
        dict: Fully preprocessed data.
    """
    try:
        # Step 1: Handle missing values
        data = impute_missing_values(raw_data)

        # Step 2: Retrieve or initialize rolling buffer
        buffer = get_or_initialize_buffer(symbol)
        updated_historical_data = buffer.update({
            "timestamp": data["timestamp"],
            "price": data["price"],
            "symbol": data["symbol"],
            "size": data["size"],
        })

        # Step 3: Feature engineering using rolling buffer data
        # Use the updated historical buffer for additional features
        data = process_numerical(data, updated_historical_data, window=200)

        # Step 4: Normalize data
        # data = encode_categorical(data)
        # data = scale_data(data)

        return data

    except Exception as e:
        print(f"Error in preprocessing pipeline: {e}")
        raise
