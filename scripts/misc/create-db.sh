#!/bin/bash

ENV_FILE_PATH="$(dirname "$0")/../../../env/dev.env"

# Load environment variables from .env file if it exists
if [ -f "$ENV_FILE_PATH" ]; then
  export $(sed 's/\r//g' "$ENV_FILE_PATH" | grep -v '^#' | grep -v '^$' | xargs)
else
  echo "Error: .env file not found at $ENV_FILE_PATH"
  exit 1
fi

# Define variables
NAMESPACE="trading-bot-ingestion"
SCHEMA_FILE_ORIG="$(dirname "$0")/../../../database/schemas/ingestion/schema.sql"
SCHEMA_FILE_TMP="$(dirname "$0")/../../../database/schemas/ingestion/schema_temp.sql"

# Substitute the password placeholder in schema file
sed "s/{{PASSWORD_PLACEHOLDER}}/$POSTGRES_PASSWORD/g" "$SCHEMA_FILE_ORIG" > "$SCHEMA_FILE_TMP"

# Export the password to avoid password prompt
export PGPASSWORD=$POSTGRES_PASSWORD

# Port-forward the PostgreSQL service to localhost
echo "Starting port-forward to PostgreSQL service in Kubernetes..."
kubectl port-forward svc/$POSTGRES_SERVICE $LOCAL_PORT:$POSTGRES_PORT -n $NAMESPACE &

# Capture the PID of the background port-forward process to kill it later
PF_PID=$!

# Wait for port-forward to establish
sleep 5

# Run SQL commands from the modified schema file
echo "Connecting to PostgreSQL and applying schema..."
psql -h localhost -p $LOCAL_PORT -U $DB_ADMIN -d $POSTGRES_DB -f "$SCHEMA_FILE_TMP"

# Check if command succeeded
if [[ $? -eq 0 ]]; then
  echo "Schema applied successfully."
else
  echo "Failed to apply schema."
fi

# Kill the port-forward process and remove temp file
kill $PF_PID
rm "$SCHEMA_FILE_TMP"
echo "Port-forward closed and temporary schema file deleted."
