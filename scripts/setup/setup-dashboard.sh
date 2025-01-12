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

# Check if Kubernetes version supports 'kubectl create token'
if kubectl -n kubernetes-dashboard create token dashboard-admin-sa --duration=720h &>/dev/null; then
    echo "Generating token for dashboard-admin-sa with 720h expiration..."
    TOKEN=$(kubectl -n kubernetes-dashboard create token dashboard-admin-sa --duration=720h)
else
    echo "Kubernetes version does not support 'kubectl create token'. Generating token manually..."
    
    # Manually extract the secret name associated with the service account
    SECRET_NAME=$(kubectl -n kubernetes-dashboard get sa dashboard-admin-sa -o jsonpath="{.secrets[0].name}")
    if [ -z "$SECRET_NAME" ]; then
        echo "Error: Unable to find a secret associated with the service account. Please check your setup."
        exit 1
    fi

    # Decode the token from the secret
    TOKEN=$(kubectl -n kubernetes-dashboard get secret "$SECRET_NAME" -o jsonpath="{.data.token}" | base64 --decode)
fi

# Output the token for login
echo -e "\nDashboard setup complete. Use the following token to log into the Kubernetes Dashboard:"
echo "$TOKEN"
echo -e "\nStart the proxy with 'kubectl proxy' and access the dashboard at:"
echo "http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/"
