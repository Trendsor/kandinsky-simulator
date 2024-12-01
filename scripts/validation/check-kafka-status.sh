#!/bin/bash

NAMESPACE="trading-bot-ingestion"
KAFKA_POD_NAME=$(kubectl get pods -n $NAMESPACE -l app=kafka -o jsonpath="{.items[0].metadata.name}")

echo "Checking Kafka status in namespace '$NAMESPACE'..."

if [ -z "$KAFKA_POD_NAME" ]; then
  echo "Error: Kafka pod not found in namespace '$NAMESPACE'."
  exit 1
fi

# Check if the Kafka pod is running
KAFKA_STATUS=$(kubectl get pod $KAFKA_POD_NAME -n $NAMESPACE -o jsonpath="{.status.phase}")

if [ "$KAFKA_STATUS" == "Running" ]; then
  echo "Kafka pod is running."
else
  echo "Error: Kafka pod is not running. Current status: $KAFKA_STATUS"
  exit 1
fi

# Verify Kafka port connectivity (ensure netcat is installed)
echo "Verifying Kafka port connectivity..."

kubectl exec -n $NAMESPACE -it $KAFKA_POD_NAME -- nc -zv localhost 9092

if [ $? -eq 0 ]; then
  echo "Kafka is accessible on port 9092."
else
  echo "Error: Unable to connect to Kafka on port 9092."
  exit 1
fi
