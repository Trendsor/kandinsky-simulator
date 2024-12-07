import boto3
from botocore.client import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("minio-utils")

def create_minio_client(endpoint, access_key, secret_key):
    """
    Create a MinIO client using Boto3.
    """
    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version="s3v4"),
    )

def create_bucket(s3_client, bucket_name):
    """
    Create a bucket in MinIO.
    """
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        logger.info(f"Bucket '{bucket_name}' created successfully.")
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        logger.info(f"Bucket '{bucket_name}' already exists.")
    except Exception as e:
        logger.error(f"Error creating bucket: {e}")

def upload_file(s3_client, bucket_name, file_path, object_name):
    """
    Upload a file to a MinIO bucket.
    """	
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        logger.info(f"File '{file_path}' uploaded as '{object_name}' inb bucket '{bucket_name}'.")
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
    
def download_file(s3_client,  bucket_name, object_name, downloaded_path):
    """
    Downloaded a file from a MinIO bucket.
    """
    try:
        s3_client.download_file(bucket_name, object_name, downloaded_path)
        logger.info(f"File '{object_name}' downloaded from bucket '{bucket_name}' to '{downloaded_path}'.")
    except Exception as e:
        logger.error(f"Error downloading file: {e}")