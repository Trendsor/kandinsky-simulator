import pandas as pd

def process_numerical(raw_data, historical_data, window=200):
    """
    Process numerical data including rolling mean calculation.
    
    Args:
        raw_data (dict): The latest raw data entry.
        historical_data (pd.DataFrame): Historical data with 'timestamp' and 'price'.
        window (int): Window size for rolling mean (default is 200 days).
        
    Returns:
        pd.DataFrame: Updated DataFrame with new rolling mean.
    """
    try:
       # Ensure historical data timestamps are pd.Timestamp
        if isinstance(historical_data['timestamp'].iloc[0], str):
            print("Converting historical data timestamps from string to pd.Timestamp.")
            historical_data['timestamp'] = pd.to_datetime(historical_data['timestamp'])

        # Normalize timestamps to timezone-naive
        if historical_data['timestamp'].dt.tz is not None:
            print("Converting historical data timestamps to timezone-naive.")
            historical_data['timestamp'] = historical_data['timestamp'].dt.tz_localize(None)

        # Convert raw_data timestamp to pd.Timestamp
        print(f"Raw data timestamp before conversion: {raw_data['timestamp']}")
        raw_data['timestamp'] = pd.Timestamp(raw_data['timestamp']).tz_localize(None)
        print(f"Raw data timestamp after conversion: {raw_data['timestamp']}")


        # Convert raw_data to a DataFrame
        new_data = pd.DataFrame([{
            'symbol': raw_data['symbol'],
            'size': int(raw_data['size']),
            'timestamp': pd.Timestamp(raw_data['timestamp']),  # Ensure consistent timestamp
            'price': float(raw_data['price'])  # Ensure price is a float
        }])

        # Append the new data entry to historical data
        combined_data = pd.concat([historical_data, new_data], ignore_index=True)

        # Sort combined data by timestamp (just in case)
        combined_data = combined_data.sort_values(by='timestamp').reset_index(drop=True)

        # Calculate rolling mean/std (200-day mean by default)
        combined_data[f'rolling_mean_{window}'] = combined_data['price'].rolling(window=window, min_periods=1).mean()
        combined_data[f'rolling_std_{window}'] = combined_data['price'].rolling(window=window, min_periods=1).std()

        combined_data['target'] = 0 # Default to 0
        combined_data.loc[combined_data['price'].shift(-1) > combined_data['price'], 'target'] = 1
        combined_data.loc[combined_data['price'].shift(-1) < combined_data['price'], 'target'] = -1

        # Adjust target for abnormal volatility
        combined_data.loc[
            combined_data['price'].shift(-1) > combined_data['price'] + combined_data[f'rolling_std_{window}'],
            'target'
        ] = 2
        combined_data.loc[
            combined_data['price'].shift(-1) < combined_data['price'] + combined_data[f'rolling_std_{window}'],
            'target'
        ] = -2

        return combined_data
    except Exception as e:
        raise ValueError(f"Error in numerical processing: {e}")

