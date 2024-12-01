#!/bin/bash

# Define the base directory as the script's location
BASE_DIR="$(dirname "$0")/../../../kubernetes/secrets"

# Specify the path to the .env file
ENV_FILE_PATH="$(dirname "$0")/../../../env/dev.env"

# Load environment variables from .env file if it exists
if [ -f "$ENV_FILE_PATH" ]; then
  export $(sed 's/\r//g' "$ENV_FILE_PATH" | grep -v '^#' | grep -v '^$' | xargs)
else
  echo "Error: .env file not found at $ENV_FILE_PATH"
  exit 1
fi

NAMESPACE="trading-bot-ingestion"

# Create or update postgres-secret
kubectl -n $NAMESPACE create secret generic postgres-secret \
    --from-literal=POSTGRES_USER="$POSTGRES_USER" \
    --from-literal=POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
    --from-literal=POSTGRES_DB="$POSTGRES_DB" \
    --from-literal=POSTGRES_HOST="$POSTGRES_HOST" \
    --dry-run=client -o yaml | kubectl apply -f -

# Create or update broker-data-api-secret
kubectl -n $NAMESPACE create secret generic broker-data-api-secret \
    --from-literal=BROKER_API_KEY="$BROKER_API_KEY" \
    --from-literal=BROKER_API_SECRET="$BROKER_API_SECRET" \
    --from-literal=BROKER_API_URL="$BROKER_API_URL" \
    --dry-run=client -o yaml | kubectl apply -f -

# Create or update kafka-secrets
kubectl -n $NAMESPACE create secret generic kafka-secrets \
    --from-literal=KAFKA_LISTENERS="$KAFKA_LISTENERS" \
    --from-literal=KAFKA_ADVERTISED_LISTENERS="$KAFKA_ADVERTISED_LISTENERS" \
    --from-literal=KAFKA_ZOOKEEPER_CONNECT="$KAFKA_ZOOKEEPER_CONNECT" \
    --from-literal=KAFKA_BOOTSTRAP_SERVER="$KAFKA_BOOTSTRAP_SERVER" \
    --dry-run=client -o yaml | kubectl apply -f -

echo "Secrets applied successfully."
