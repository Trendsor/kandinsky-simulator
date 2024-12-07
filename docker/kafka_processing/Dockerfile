# Base Python image
FROM python:3.10-slim

# Install necessary OS dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY docker/kafka_processing/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the processing script
COPY src/processing /app/processing

# Run the Kafka Consumer
CMD ["python", "processing/kafka_consumer_preprocessing.py"]
