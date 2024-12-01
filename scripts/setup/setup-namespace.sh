#!/bin/bash
echo "Creating namespaces..."
kubectl apply -f kubernetes/namespaces/trading-bot-ingestion.yaml
kubectl apply -f kubernetes/namespaces/trading-bot-execution.yaml
kubectl apply -f kubernetes/namespaces/trading-bot-inference.yaml
kubectl apply -f kubernetes/namespaces/trading-bot-model-training.yaml
kubectl apply -f kubernetes/namespaces/trading-bot-monitoring.yaml
echo "Namespaces created."
