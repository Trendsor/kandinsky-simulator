import os
import pickle
from datetime import datetime
from minio import Minio
from src.utils.minio_utils import create_minio_client, download_file

def get_latest_model_name(client, bucket_name):
    """
    Retrieve the name of the latest model file from the MinIO bucket.

    Args:
        client: MinIO client.
        bucket_name (str): The bucket name in MinIO.

    Returns:
        str: The name of the latest model file.
    """
    # List objects in the bucket sorted by name
    objects = client.list_objects(bucket_name, recursive=True)
    
    latest_model = None
    for obj in objects:
        # Ensure the object name ends with the model suffix
        if obj.object_name.endswith("_trained_model.pkl"):
            latest_model = obj.object_name  # The last valid object is the latest
    if not latest_model:
        raise FileNotFoundError(f"No valid model file found in bucket '{bucket_name}'.")

    return latest_model

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

    # Download the latest model
    download_file(client, bucket_name, latest_model_name, model_path)

    # Load the model
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    return model
