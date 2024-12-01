#!/bin/bash

BASE_DIR="$(dirname "$0")/../../kafka"

# Function to check if a file exists and is not empty
check_file() {
  if [[ ! -s "$1" ]]; then
    echo "Error: File $1 is missing or empty."
    exit 1
  fi
}

# Check files before applying them
check_file "$BASE_DIR/zookeeper-deployment.yaml"
check_file "$BASE_DIR/kafka-deployment.yaml"
check_file "$BASE_DIR/kafka-svc.yaml"
check_file "$BASE_DIR/zookeeper-svc.yaml"

# Apply Zookeeper Deployment
kubectl apply -f "$BASE_DIR/zookeeper-deployment.yaml"
kubectl apply -f "$BASE_DIR/zookeeper-svc.yaml"

# Apply Kafka Deployment and Service
kubectl apply -f "$BASE_DIR/kafka-deployment.yaml"
kubectl apply -f "$BASE_DIR/kafka-svc.yaml"

echo "Kafka setup completed."
