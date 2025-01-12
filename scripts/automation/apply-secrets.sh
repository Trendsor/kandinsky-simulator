#!/bin/bash

# Define the base directory as the script's location
BASE_DIR="$(dirname "$0")/../../kubernetes/secrets"

# Specify the path to the .env file
ENV_FILE_PATH="$(dirname "$0")/../../env/prod.env"

# Load environment variables from .env file if it exists
if [ -f "$ENV_FILE_PATH" ]; then
  export $(sed 's/\r//g' "$ENV_FILE_PATH" | grep -v '^#' | grep -v '^$' | xargs)
else
  echo "Error: .env file not found at $ENV_FILE_PATH"
  exit 1
fi

INGESTION_NAMESPACE="trading-bot-ingestion"
TRAINIG_NAMESPACE="trading-bot-model-training"
EXECUTION_NAMESPACE="trading-bot-execution"

# Dynamically construct POSTGRES_CONN_STRING
export POSTGRES_CONN_STRING="dbname='${POSTGRES_DB}' user='${POSTGRES_USER}' password='${POSTGRES_PASSWORD}' host='${POSTGRES_HOST}' port=${POSTGRES_PORT}"
export POSTGRES_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

# Create or update postgres-secret
kubectl -n $INGESTION_NAMESPACE create secret generic postgres-secret \
    --from-literal=POSTGRES_USER="$POSTGRES_USER" \
    --from-literal=POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
    --from-literal=POSTGRES_DB="$POSTGRES_DB" \
    --from-literal=POSTGRES_HOST="$POSTGRES_HOST" \
    --from-literal=POSTGRES_PORT="$POSTGRES_PORT" \
    --from-literal=POSTGRES_CONN_STRING="$POSTGRES_CONN_STRING" \
    --dry-run=client -o yaml | kubectl apply -f -

# Create or update broker-data-api-secret
kubectl -n $INGESTION_NAMESPACE create secret generic broker-data-api-secret \
    --from-literal=BROKER_API_KEY="$BROKER_API_KEY" \
    --from-literal=BROKER_API_SECRET="$BROKER_API_SECRET" \
    --from-literal=BROKER_API_URL="$BROKER_API_URL" \
    --from-literal=SYMBOLS="$SYMBOLS" \
    --dry-run=client -o yaml | kubectl apply -f -

# Create or update kafka-secrets
kubectl -n $INGESTION_NAMESPACE create secret generic kafka-secrets \
    --from-literal=KAFKA_LISTENERS="$KAFKA_LISTENERS" \
    --from-literal=KAFKA_ADVERTISED_LISTENERS="$KAFKA_ADVERTISED_LISTENERS" \
    --from-literal=KAFKA_ZOOKEEPER_CONNECT="$KAFKA_ZOOKEEPER_CONNECT" \
    --from-literal=KAFKA_BOOTSTRAP_SERVER="$KAFKA_BOOTSTRAP_SERVER" \
    --dry-run=client -o yaml | kubectl apply -f -

# Create or update kafka-secrets
kubectl -n $TRAINIG_NAMESPACE create secret generic minio-secret \
    --from-literal=MINIO_ROOT_USER="$MINIO_ROOT_USER" \
    --from-literal=MINIO_ROOT_PASSWORD="$MINIO_ROOT_PASSWORD" \
    --from-literal=MINIO_ENDPOINT="$MINIO_ENDPOINT" \
    --dry-run=client -o yaml | kubectl apply -f -

# Create or update postgres-secret
kubectl -n $TRAINIG_NAMESPACE create secret generic postgres-secret \
    --from-literal=POSTGRES_USER="$POSTGRES_USER" \
    --from-literal=POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
    --from-literal=POSTGRES_DB="$POSTGRES_DB" \
    --from-literal=POSTGRES_HOST="$POSTGRES_HOST" \
    --from-literal=POSTGRES_PORT="$POSTGRES_PORT" \
    --from-literal=POSTGRES_CONN_STRING="$POSTGRES_CONN_STRING" \
    --dry-run=client -o yaml | kubectl apply -f -

# Create or update postgres-secret
kubectl -n $EXECUTION_NAMESPACE create secret generic postgres-secret \
    --from-literal=POSTGRES_URL="$POSTGRES_URL" \
    --dry-run=client -o yaml | kubectl apply -f -

# Create or update broker-data-api-secret
kubectl -n $EXECUTION_NAMESPACE create secret generic broker-data-api-secret \
    --from-literal=BROKER_API_KEY="$BROKER_API_KEY" \
    --from-literal=BROKER_API_SECRET="$BROKER_API_SECRET" \
    --from-literal=BROKER_BASE_URL="$BROKER_BASE_URL" \
    --dry-run=client -o yaml | kubectl apply -f -

# Create or update kafka-secrets
kubectl -n $EXECUTION_NAMESPACE create secret generic kafka-secrets \
    --from-literal=KAFKA_BOOTSTRAP_SERVER="$KAFKA_BOOTSTRAP_SERVER" \
    --dry-run=client -o yaml | kubectl apply -f -

# Create or update kafka-secrets
kubectl -n $EXECUTION_NAMESPACE create secret generic minio-secret \
    --from-literal=MINIO_ROOT_USER="$MINIO_ROOT_USER" \
    --from-literal=MINIO_ROOT_PASSWORD="$MINIO_ROOT_PASSWORD" \
    --from-literal=MINIO_ENDPOINT="$MINIO_ENDPOINT" \
    --dry-run=client -o yaml | kubectl apply -f -

echo "Secrets applied successfully."
