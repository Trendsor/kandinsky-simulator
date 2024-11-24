import tensorflow as tf
import numpy as np
import requests
import time

# Define the API endpoint and request headers if needed
API_ENDPOINT = "https://api.example.com/minute_data"
API_KEY = "your_api_key_here"

def fetch_minute_data():
    """Fetches the latest minute-level data from the API."""
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    response = requests.get(API_ENDPOINT, headers=headers)
    data = response.json()
    return data

def preprocess_data(raw_data):
    """Preprocesses raw data into a format suitable for the model."""
    # Assuming raw_data is a list of dictionaries with a 'value' field
    data = np.array([item['value'] for item in raw_data]).reshape(-1, 1)
    # Create sequences for LSTM input
    window_size = 10
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i + window_size])
        y.append(data[i + window_size])
    return np.array(X), np.array(y)

# Load or define the model
model = tf.keras.models.load_model("time_series_model.h5")

def train_on_new_data():
    """Fetches new data and trains the model."""
    raw_data = fetch_minute_data()
    X, y = preprocess_data(raw_data)
    model.fit(X, y, epochs=1, batch_size=32)
    model.save("time_series_model.h5")
    print("Model updated with new data.")

# Periodically fetch new data and train the model
while True:
    train_on_new_data()
    time.sleep(60)  # Wait for 1 minute before fetching new data
