#!/bin/bash

# Define the services to match in the process list
SERVICES=("minio-svc" "postgres-svc")

LOG_FILE="port-forward-cleanup.log"
echo "$(date): Starting port-forward cleanup." >> $LOG_FILE

for service in "${SERVICES[@]}"; do
    echo "Searching for port-forward processes related to $service..."
    pids=$(ps aux | grep "kubectl port-forward svc/$service" | grep -v "grep" | awk '{print $2}')

    if [ -n "$pids" ]; then
        echo "Found processes for $service: $pids"
        read -p "Do you want to terminate these processes? (y/n): " confirm_service
        if [[ $confirm_service != "y" ]]; then
            echo "Skipping termination for $service."
            echo "$(date): Skipped termination for $service." >> $LOG_FILE
            continue
        fi

        for pid in $pids; do
            read -p "Do you want to terminate process $pid for $service? (y/n): " confirm_pid
            if [[ $confirm_pid == "y" ]]; then
                if kill -9 $pid; then
                    echo "$(date): Terminated process $pid for $service" >> $LOG_FILE
                    echo "Process $pid for $service terminated successfully."
                else
                    echo "$(date): Failed to terminate process $pid for $service" >> $LOG_FILE
                    echo "Failed to terminate process $pid for $service."
                fi
            else
                echo "$(date): Skipped process $pid for $service" >> $LOG_FILE
                echo "Skipped termination for process $pid of $service."
            fi
        done
    else
        echo "No active port-forward processes found for $service."
        echo "$(date): No active port-forward processes found for $service" >> $LOG_FILE
    fi
done

echo "Port-forward cleanup complete. Check $LOG_FILE for details."
