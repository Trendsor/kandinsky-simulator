#!/bin/bash

# Check if Kubernetes Dashboard service is available
NAMESPACE="kubernetes-dashboard"
SERVICE_NAME="kubernetes-dashboard"

echo "Checking Kubernetes Dashboard access..."

kubectl get svc $SERVICE_NAME -n $NAMESPACE > /dev/null 2>&1

if [ $? -ne 0 ]; then
  echo "Error: Kubernetes Dashboard service not found in namespace '$NAMESPACE'."
  exit 1
fi

# Get the token for accessing the Dashboard
SECRET_NAME=$(kubectl -n $NAMESPACE get secret | grep dashboard-admin-sa | awk '{print $1}')
DASHBOARD_TOKEN=$(kubectl -n $NAMESPACE get secret $SECRET_NAME -o jsonpath="{.data.token}" | base64 --decode)

echo "Kubernetes Dashboard is accessible. Use the following token to log in:"
echo "$DASHBOARD_TOKEN"
