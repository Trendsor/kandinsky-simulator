#!/bin/bash

# Load environment variables from .env file if available
ENV_FILE_PATH="$(dirname "$0")/../../env/dev.env"

if [ -f "$ENV_FILE_PATH" ]; then
  export $(grep -v '^#' "$ENV_FILE_PATH" | grep -v '^$' | xargs)
else
  echo "Error: .env file not found at $ENV_FILE_PATH"
  exit 1
fi

# Check PostgreSQL connection
echo "Checking PostgreSQL connection..."

kubectl run postgres-client --rm -i --tty --image=postgres:13 --namespace trading-bot-ingestion -- \
  psql postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST/$POSTGRES_DB -c "\q"

if [ $? -eq 0 ]; then
  echo "PostgreSQL connection successful."
else
  echo "Error: Unable to connect to PostgreSQL."
  exit 1
fi
