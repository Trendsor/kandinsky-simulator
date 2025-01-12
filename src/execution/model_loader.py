import os
import pickle
import logging
from datetime import datetime
from src.utils.minio_utils import create_minio_client, download_file

# Initialize the logger
logger = logging.getLogger("model-loader")
logging.basicConfig(level=logging.INFO)

def get_latest_model_name(client, bucket_name):
    """
    Retrieve the name of the latest model file from the S3-compatible bucket using Boto3.

    Args:
        client: Boto3 S3 client.
        bucket_name (str): The bucket name.

    Returns:
        str: The name of the latest model file.
    """
    try:
        response = client.list_objects_v2(Bucket=bucket_name)

        if "Contents" not in response:
            raise FileNotFoundError(f"No objects found in bucket '{bucket_name}'.")

        latest_model = None
        for obj in response["Contents"]:
            if obj["Key"].endswith("_trained_model.pkl"):
                latest_model = obj["Key"]  # The last valid object is the latest

        if not latest_model:
            raise FileNotFoundError(f"No valid model file found in bucket '{bucket_name}'.")
        
        return latest_model
    except client.exceptions.NoSuchBucket:
        raise FileNotFoundError(f"Bucket '{bucket_name}' does not exist.")
    except Exception as e:
        raise RuntimeError(f"Error retrieving objects from bucket '{bucket_name}': {e}")


def load_model(bucket_name, save_path="/tmp"):
    """
    Load the latest model from MinIO.

    Args:
        bucket_name (str): The bucket name in MinIO.
        save_path (str): Local path to save the downloaded model.

    Returns:
        The loaded model.
    """
    client = create_minio_client()
    latest_model_name = get_latest_model_name(client, bucket_name)
    model_path = os.path.join(save_path, latest_model_name)

    # Ensure the save directory exists
    os.makedirs(save_path, exist_ok=True)

    # Download the latest model
    try:
        download_file(client, bucket_name, latest_model_name, model_path)
        logger.info(f"Model downloaded to: {model_path}")
    except Exception as e:
        logger.error(f"Failed to download the model: {e}")
        raise

    # Verify the downloaded file size
    if not os.path.exists(model_path) or os.path.getsize(model_path) == 0:
        raise FileNotFoundError(f"Downloaded model file is missing or empty: {model_path}")

    # Load the model using pickle
    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        logger.info("Model loaded successfully.")
    except pickle.UnpicklingError as e:
        logger.error(f"Failed to unpickle the model file: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while loading the model: {e}")
        raise

    return model
