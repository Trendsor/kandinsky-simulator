#!/bin/bash

# Port-forward to PGADMIN
nohup kubectl port-forward svc/postgres-svc 5433:5432 -n trading-bot-ingestion > scripts/logs/postgres-port-forward.log 2>&1 &

echo "Port forwarding for MinIO started."