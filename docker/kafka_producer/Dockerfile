# Base image
FROM python:3.10-slim

# Install necessary OS dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy and install Python dependencies
COPY docker/kafka_producer/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Kafka producer script into the container
COPY src/ingestion/kafka_producer.py /app/kafka_producer.py

# Set the entry point to run the Kafka producer script
CMD ["python", "kafka_producer.py"]

