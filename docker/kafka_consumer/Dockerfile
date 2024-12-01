# Use a lightweight Python image
FROM python:3.10-slim

# Install necessary OS dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy and install Python dependencies
COPY  docker/kafka_consumer/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Kafka consumer script into the container
COPY src/ingestion/kafka_consumer.py /app/kafka_consumer.py

# Run the consumer script
CMD ["python", "kafka_consumer.py"]
