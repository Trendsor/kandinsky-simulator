Below is an updated README.md that incorporates instructions for starting a local Kubernetes cluster with minikube using the Docker driver, accessing the Dashboard via kubectl proxy (with an explanation of how the scripts integrate into the overall execution), and details on Docker Hub for image hosting.

---

# Kandinsky Simulator

Kandinsky Simulator is a modular, containerized platform designed to simulate complex trading scenarios. It integrates multiple microservices—including data ingestion, execution, processing, and model training—using modern technologies such as Docker, Kubernetes, and Kafka. This project provides a robust framework for simulating market conditions and testing trading strategies in a controlled environment.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Local Kubernetes Setup](#local-kubernetes-setup)
  - [Starting minikube with Docker](#starting-minikube-with-docker)
  - [Accessing the Kubernetes Dashboard](#accessing-the-kubernetes-dashboard)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Docker & Kubernetes Deployment](#docker--kubernetes-deployment)
- [Scripts and Utilities](#scripts-and-utilities)
- [Docker Hub](#docker-hub)
- [Tests](#tests)
- [Contributing](#contributing)
- [License](#license)

## Overview

Kandinsky Simulator is built to emulate real-world trading environments. Its key features include:
- **Microservice Architecture:** Separate modules for ingestion, execution, processing, and model training.
- **Containerization:** Dockerized components ensure consistent environments across development, testing, and production.
- **Orchestration:** Kubernetes manifests are provided for scaling and managing deployments.
- **Messaging:** Kafka is used for efficient, real-time data streaming between services.
- **Database Integration:** PostgreSQL is utilized for storing trading data and simulation results, with clear schema management.

## Project Structure

The repository is organized as follows:

```
├── Dockerfile                          # Root Dockerfile for project-wide tasks
├── LICENSE                             # License file
├── README.md                           # Project documentation (this file)
├── config                              # Environment-specific configuration files
│   ├── dev_config.yaml
│   └── prod_config.yaml
├── data                                # Sample data files and model artifacts
│   ├── historical_stock_data.csv
│   └── model
├── database                            # Database deployment and schema definitions
│   ├── postgres-deployment.yaml
│   ├── postgres-svc.yaml
│   ├── postgres-volume.yaml
│   └── schemas
│       ├── ingestion
│       │   ├── init.sql
│       │   └── schema.sql
│       └── processing
│           └── schema.sql
├── docker                              # Dockerfiles for each microservice
│   ├── kafka_consumer
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── kafka_execution
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── kafka_processing
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── kafka_producer
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── model_training
│       ├── Dockerfile
│       └── requirements.txt
├── env                                 # Environment variable files for dev and prod
│   ├── dev.env
│   └── prod.env
├── kafka                               # Kafka deployment and configuration files
│   ├── kafka-deployment.yaml
│   ├── kafka-svc.yaml
│   ├── topics-config.yaml
│   ├── zookeeper-deployment.yaml
│   └── zookeeper-svc.yaml
├── kubeconfig.yaml                     # Kubernetes config file for cluster access
├── kubernetes                          # Kubernetes manifests for deploying the services
│   ├── configmaps
│   │   ├── ingestion
│   │   │   ├── postgres-init-configmap.yaml
│   │   │   └── websocket-session-lock-configmap.yaml
│   │   └── training
│   │       └── minio-configmap.yaml
│   ├── cronjobs
│   │   └── model_training-cronjob.yaml
│   ├── deployments
│   │   ├── execution
│   │   │   └── kafka-consumer-inference.yaml
│   │   ├── ingestion
│   │   │   ├── kafka-consumer-deployment.yaml
│   │   │   └── kafka-producer-deployment.yaml
│   │   └── processing
│   │       └── kafka-data-processor.yaml
│   ├── jobs
│   │   ├── alembic-job.yaml
│   │   └── model-training-job.yaml
│   ├── namespaces
│   │   ├── trading-bot-execution.yaml
│   │   ├── trading-bot-inference.yaml
│   │   ├── trading-bot-ingestion.yaml
│   │   ├── trading-bot-model-training.yaml
│   │   ├── trading-bot-monitoring.yaml
│   │   └── trading-bot-processing.yaml
│   ├── role-bindings
│   │   └── role-binding.yaml
│   ├── roles
│   │   └── configmap-reader-role.yaml
│   ├── secrets
│   │   ├── dashboard-admin-sa-token.yaml
│   │   └── dashboard-admin-setup.yaml
│   └── services
│       └── bot_service.yaml
├── port-forward-cleanup.log
├── requirements.txt                    # Python dependencies for core services
├── scripts                             # Utility and automation scripts
│   ├── access                         # Scripts to access database and storage
│   ├── automation                     # Automation scripts for deployment and setup
│   ├── logs                           # Log files for various services
│   ├── misc                           # Miscellaneous utility scripts
│   ├── setup                          # Scripts to initialize namespaces, storage, etc.
│   ├── utils                          # Helper functions and logging utilities
│   └── validation                     # Scripts to validate service health and connectivity
├── src                                 # Application source code
│   ├── database                       # Database models and migrations
│   ├── execution                      # Execution engine and inference logic
│   ├── ingestion                      # Data ingestion services using Kafka
│   ├── model_training                 # Model training and evaluation routines
│   ├── processing                     # Data processing and feature engineering modules
│   └── utils                          # Shared utilities across modules
├── storage                             # MinIO deployment configuration
│   ├── minio-deployment.yaml
│   ├── minio-pvc.yaml
│   └── minio-svc.yaml
├── tests                               # Test suites for various components
│   └── kafka
├── train.py                            # Entry point for model training
└── worker-deployment.yaml              # Worker service deployment configuration
```

## Local Kubernetes Setup

For local development and testing, Kandinsky Simulator supports running a local Kubernetes cluster with minikube and accessing the Dashboard via a local proxy.

### Starting minikube with Docker

To launch a local Kubernetes cluster using minikube with Docker as the driver, run:

```bash
minikube start --driver=docker
```

This command sets up a local cluster that runs inside Docker containers. The Docker driver is configured to use your installed Docker engine, eliminating the need for a separate virtual machine. You can customize resource allocation (e.g., CPUs, memory) using additional flags if needed:

```bash
minikube start --driver=docker --cpus=2 --memory=4096
```

### Accessing the Kubernetes Dashboard

The Kubernetes Dashboard provides a graphical interface to monitor and manage your cluster. To access it locally:

1. **Start the Dashboard Proxy:**  
   Run the following command to create a proxy that forwards API requests from your local machine to the cluster:

   ```bash
   kubectl proxy --port=8001
   ```

2. **Access the Dashboard URL:**  
   Open your browser and navigate to:

   ```
   http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
   ```

   This URL routes through the proxy to the Dashboard service running in your cluster.

3. **Scripted Execution:**  
   Note that our automation scripts in the `scripts/` directory (such as those in `scripts/setup` or `scripts/automation`) include commands that launch both the minikube cluster and the proxy. These scripts are key to running the whole app seamlessly.

## Installation

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [minikube](https://minikube.sigs.k8s.io/docs/start/) (installed locally)
- [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/)
- [Python 3.8+](https://www.python.org/downloads/)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Trendsor/kandinsky-simulator.git
   cd kandinsky-simulator
   ```

2. **Install Python Dependencies**

   Install the core Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Build Docker Images**

   Navigate to the relevant service directories under the `docker/` folder and build images. For example:

   ```bash
   cd docker/kafka_consumer
   docker build -t kandinsky/kafka_consumer .
   ```

   Repeat for each service as needed.

## Configuration

- **Environment Variables:**  
  Configure your environment by editing the files in the `env/` directory. Use `dev.env` for development settings and `prod.env` for production.

- **Application Configs:**  
  The `config/` directory contains configuration files (`dev_config.yaml` and `prod_config.yaml`) that can be adjusted based on your environment requirements.

## Usage

- **Running the Simulation:**  
  Depending on your setup, you can run the simulation locally using Python scripts or deploy the services to Kubernetes. For local testing, you might start with:

  ```bash
  python train.py
  ```

- **Interacting with Services:**  
  The individual services are organized under `src/`. You can run them directly (for example, the ingestion service via `python src/ingestion/kafka_consumer.py`) or orchestrate them using Docker Compose/Kubernetes.

## Docker & Kubernetes Deployment

- **Docker Deployment:**  
  After building the Docker images, you can run containers locally:

  ```bash
  docker run -d --env-file env/dev.env kandinsky/kafka_consumer
  ```

- **Kubernetes Deployment:**  
  Apply the Kubernetes manifests provided in the `kubernetes/` directory to deploy the services:

  ```bash
  kubectl apply -f kubernetes/
  ```

  Ensure you have configured your kubeconfig (see `kubeconfig.yaml`) before deploying.

## Scripts and Utilities

The `scripts/` directory includes several helpful scripts to:

- Set up namespaces and storage
- Apply Kubernetes secrets and config maps
- Access and validate service connectivity (e.g., database, Kafka)
- Automate deployment tasks

Review the subdirectories (e.g., `scripts/setup`, `scripts/automation`) for detailed instructions.

## Docker Hub

Docker Hub is used as the centralized registry for the Docker images used in this project. The images are hosted under the [Trendsor organization on Docker Hub](https://hub.docker.com/r/Trendsor) (or a similarly designated account). To pull an image for a specific service, use:

```bash
docker pull trendsor/kafka_consumer
```

Repeat for other services (e.g., `kafka_producer`, `model_training`, etc.). You can also push your local builds to Docker Hub if you make changes or updates:

```bash
docker tag kandinsky/kafka_consumer trendsor/kafka_consumer:latest
docker push trendsor/kafka_consumer:latest
```

For more information, visit the [Docker Hub documentation](https://docs.docker.com/docker-hub/).

## Tests

The `tests/` directory contains integration tests, particularly for Kafka-based components. Run the tests using your preferred testing framework:

```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Ensure your code adheres to the project’s style guidelines.
4. Submit a pull request with a detailed description of your changes.

For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the terms specified in the [LICENSE](./LICENSE) file.

---

Feel free to adjust sections or commands as needed to best fit your project's requirements.