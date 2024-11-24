#!/bin/bash

# Exit immediately if any command exits with a non-zero status
set -e

# Deploy the Kubernetes Dashboard
echo "Deploying Kubernetes Dashboard..."
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.5.1/aio/deploy/recommended.yaml

# Create Service Account and ClusterRoleBinding for Dashboard Access
echo "Creating service account and ClusterRoleBinding for dashboard access..."
kubectl create serviceaccount dashboard-admin-sa -n kubernetes-dashboard || echo "Service account already exists"
kubectl create clusterrolebinding dashboard-admin-sa-binding --clusterrole=cluster-admin --serviceaccount=kubernetes-dashboard:dashboard-admin-sa || echo "ClusterRoleBinding already exists"

# Manually Generate a Token for the Service Account
echo "Generating token for dashboard-admin-sa..."
TOKEN=$(kubectl -n kubernetes-dashboard create token dashboard-admin-sa)

# Output the token for login
echo -e "\nDashboard setup complete. Use the following token to log into the Kubernetes Dashboard:"
echo "$TOKEN"
echo -e "\nStart the proxy with 'kubectl proxy' and access the dashboard at:"
echo "http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/"
