# Base Python image
FROM python:3.10-slim

# Install necessary OS dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY docker/kafka_processing/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire `src` directory
COPY src /app/src

# Set PYTHONPATH to include `/app/src`
ENV PYTHONPATH=/app

# Run the Kafka Consumer
CMD ["python", "src/processing/kafka_consumer_preprocessing.py"]
