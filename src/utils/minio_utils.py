import boto3
from botocore.client import Config
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("minio-utils")

def create_minio_client():
    """
    Create and return a MinIO client using environment variables.
    """
    try:
        endpoint = os.getenv("MINIO_ENDPOINT")
        access_key = os.getenv("MINIO_ACCESS_KEY")
        secret_key = os.getenv("MINIO_SECRET_KEY")
        
        if not all([endpoint, access_key, secret_key]):
            raise ValueError("One or more required environment variables are missing.")
        
        client = boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version="s3v4"),
        )
        logger.info("MinIO client created successfully.")
        return client
    except Exception as e:
        logger.error(f"Failed to create MinIO client: {e}")
        raise

def create_bucket(client, bucket_name):
    """
    Create a bucket in MinIO if it doesn't exist.
    """
    try:
        client.create_bucket(Bucket=bucket_name)
        logger.info(f"Bucket '{bucket_name}' created successfully.")
    except client.exceptions.BucketAlreadyOwnedByYou:
        logger.info(f"Bucket '{bucket_name}' already exists.")
    except Exception as e:
        logger.error(f"Error creating bucket '{bucket_name}': {e}")
        raise

def upload_file(client, bucket_name, file_path, object_name=None):
    """
    Upload a file to a MinIO bucket.

    Args:
        client: MinIO client instance.
        bucket_name (str): Name of the bucket to upload to.
        file_path (str): Path to the local file to upload.
        object_name (str, optional): Name of the object in the bucket. Defaults to the file name.
    """
    try:
        if not object_name:
            object_name = os.path.basename(file_path)
        
        client.upload_file(file_path, bucket_name, object_name)
        logger.info(f"File '{file_path}' uploaded as '{object_name}' in bucket '{bucket_name}'.")
    except Exception as e:
        logger.error(f"Error uploading file '{file_path}': {e}")
        raise

def download_file(client, bucket_name, object_name, download_path):
    """
    Download a file from a MinIO bucket.

    Args:
        client: MinIO client instance.
        bucket_name (str): Name of the bucket.
        object_name (str): Name of the object in the bucket.
        download_path (str): Path to save the downloaded file.
    """
    try:
        client.download_file(bucket_name, object_name, download_path)
        logger.info(f"File '{object_name}' downloaded from bucket '{bucket_name}' to '{download_path}'.")
    except Exception as e:
        logger.error(f"Error downloading file '{object_name}': {e}")
        raise

def list_files(client, bucket_name):
    """
    List all files in a given bucket.

    Args:
        client: MinIO client instance.
        bucket_name (str): Name of the bucket.

    Returns:
        list: List of object names in the bucket.
    """
    try:
        response = client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            files = [obj['Key'] for obj in response['Contents']]
            logger.info(f"Files in bucket '{bucket_name}': {files}")
            return files
        else:
            logger.info(f"No files found in bucket '{bucket_name}'.")
            return []
    except Exception as e:
        logger.error(f"Error listing files in bucket '{bucket_name}': {e}")
        raise

def delete_file(client, bucket_name, object_name):
    """
    Delete a file from a MinIO bucket.

    Args:
        client: MinIO client instance.
        bucket_name (str): Name of the bucket.
        object_name (str): Name of the object to delete.
    """
    try:
        client.delete_object(Bucket=bucket_name, Key=object_name)
        logger.info(f"File '{object_name}' deleted from bucket '{bucket_name}'.")
    except Exception as e:
        logger.error(f"Error deleting file '{object_name}': {e}")
        raise
