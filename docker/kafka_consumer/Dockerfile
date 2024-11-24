# Base Python image
FROM python:3.9-slim

# Install dependencies
RUN pip install --no-cache-dir confluent-kafka psycopg2-binary

# Set working directory
WORKDIR /app

# Copy consumer script into the container
COPY kafka_consumer.py .

# Run the consumer
CMD ["python", "kafka_consumer.py"]
