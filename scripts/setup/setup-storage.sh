#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "Creating MinIO storage and scheduling the model training job..."

# Apply MinIO configurations
echo "Applying MinIO Deployment..."
kubectl apply -f storage/minio-deployment.yaml || { echo "Failed to apply minio-deployment.yaml"; exit 1; }

echo "Applying MinIO Service..."
kubectl apply -f storage/minio-svc.yaml || { echo "Failed to apply minio-svc.yaml"; exit 1; }

echo "Applying MinIO PVC..."
kubectl apply -f storage/minio-pvc.yaml || { echo "Failed to apply minio-pvc.yaml"; exit 1; }

# Wait for MinIO deployment to be ready
echo "Waiting for MinIO deployment to be ready..."
kubectl rollout status deployment/minio-deployment -n model-training-namespace

# Schedule model-training job
echo "Applying model-training Job..."
kubectl apply -f jobs/model-training-job.yaml || { echo "Failed to apply model-training-job.yaml"; exit 1; }

echo "Storage and job setup complete."
