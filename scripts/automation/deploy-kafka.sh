#!/bin/bash

BASE_DIR="$(dirname "$0")/../.."

# Deploy Zookeeper
kubectl apply -f "$BASE_DIR/kafka/zookeeper-deployment.yaml"

# Deploy Kafka
kubectl apply -f "$BASE_DIR/kafka/kafka-deployment.yaml"
kubectl apply -f "$BASE_DIR/kafka/kafka-svc.yaml"

# Deploy Kafka producer and consumer pods
kubectl apply -f "$BASE_DIR/kubernetes/deployments/kafka-data-consumer-deployment.yaml"

echo "Kafka setup completed."
