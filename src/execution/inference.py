from utils.minio_utils import create_minio_client, download_file

# Initialize MinIO client
minio_client = create_minio_client()

# Load model for inference
download_path = "/tmp/markov_model.pkl"
download_file(minio_client, bucket_name="models", object_name="markov_model.pkl", download_path=download_path)
