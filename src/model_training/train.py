import os
import psycopg2
import pandas as pd
from datetime import datetime, timezone
from minio import Minio
from sklearn.linear_model import LinearRegression
from minio.error import S3Error
from src.utils.minio_utils import create_minio_client, upload_file, create_bucket
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("model-training")

# PostgreSQL Configuration
POSTGRES_CONN_STRING = os.getenv("POSTGRES_CONN_STRING")

BUCKET_NAME = "trained-models"

# Local file paths
MODEL_FILE_PATH = f"{datetime.now(timezone.utc)}_trained_model.pkl"

def fetch_training_data(conn_string):
    """
    Fetch historical training data from the PostgreSQL database.

    Args:
        conn_string (str): PostgreSQL connection string.

    Returns:
        pd.DataFrame: Training data as a pandas DataFrame.
    """
    query = "SELECT * FROM stock_data_processed"  # Adjust based on your table schema
    try:
        with psycopg2.connect(conn_string) as conn:
            df = pd.read_sql_query(query, conn)
            logger.info(f"Fetched {len(df)} rows of training data from PostgreSQL.")
            return df
    except Exception as e:
        logger.error(f"Error fetching training data: {e}")
        raise

def train_model(data):
    """
    Train a model using the provided data.

    Args:
        data (pd.DataFrame): Training data.

    Returns:
        Trained model (placeholder for actual implementation).
    """
    # Placeholder for training logic
    logger.info("Training model with provided data...")
    X = data[["price", "rolling_mean_200", "rolling_std_200"]]  # Replace with actual feature columns
    y = data["target"]  # Replace with actual target column
    model = LinearRegression()  # Replace with your model
    model.fit(X, y)
    return model

def save_model(model, file_path):
    """
    Save the trained model to a local file.

    Args:
        model: Trained model object.
        file_path (str): Path to save the model.
    """
    try:
        # Placeholder: Replace with actual model saving logic
        with open(file_path, "w") as f:
            f.write(str(model))  # Serialize model
        logger.info(f"Model saved to {file_path}.")
    except Exception as e:
        logger.error(f"Error saving model to {file_path}: {e}")
        raise

def main():
    # Step 1: Connect to PostgreSQL and fetch data
    logger.info("Fetching training data...")
    training_data = fetch_training_data(POSTGRES_CONN_STRING)

    # Step 2: Train the model
    logger.info("Training model...")
    model = train_model(training_data)

    # Step 3: Save the model locally
    logger.info("Saving model locally...")
    save_model(model, MODEL_FILE_PATH)

    # Step 4: Set up MinIO client
    logger.info("Setting up MinIO client...")
    client = create_minio_client()

    # Step 5: Ensure the bucket exists
    logger.info(f"Ensuring bucket '{BUCKET_NAME}' exists...")
    try:
        create_bucket(client, BUCKET_NAME)
    except S3Error as e:
        logger.error(f"Error creating or verifying bucket: {e}")
        raise

    # Step 6: Upload the model file to MinIO
    logger.info("Uploading model to MinIO...")
    try:
        upload_file(client, BUCKET_NAME, MODEL_FILE_PATH)
    except Exception as e:
        logger.error(f"Error uploading model: {e}")
        raise

if __name__ == "__main__":
    main()
