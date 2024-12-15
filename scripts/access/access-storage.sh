#!/bin/bash

echo "Starting port-forwarding for MinIO API and WebUI..."

# Port-forward for MinIO API
nohup kubectl port-forward --address 127.0.0.1 svc/minio-svc 9090:9090 -n trading-bot-model-training > scripts/logs/minio-api.log 2>&1 &
echo "MinIO API available at http://localhost:9000"

# Port-forward for MinIO WebUI
nohup kubectl port-forward --address 127.0.0.1 svc/minio-svc 9000:9000 -n trading-bot-model-training > scripts/logs/minio-webui.log 2>&1 &
echo "MinIO WebUI available at http://localhost:9090"

echo "Port-forwarding setup complete."
