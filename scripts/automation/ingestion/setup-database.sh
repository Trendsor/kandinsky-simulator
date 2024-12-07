#!/bin/bash

BASE_DIR="$(dirname "$0")/../../../database"

# Function to check if a file exists and is not empty
check_file() {
  if [[ ! -s "$1" ]]; then
    echo "Error: File $1 is missing or empty."
    exit 1
  fi
}

# Check files before applying them
check_file "$BASE_DIR/postgres-deployment.yaml"
check_file "$BASE_DIR/postgres-svc.yaml"

# Apply psql Deployment
kubectl apply -f "$BASE_DIR/postgres-svc.yaml"
kubectl apply -f "$BASE_DIR/postgres-volume.yaml"
kubectl apply -f "$BASE_DIR/postgres-deployment.yaml"


echo "Postgres setup completed."