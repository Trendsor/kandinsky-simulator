# Base Python image
FROM python:3.10-slim

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy the processing script
COPY src/kafka_processing/consumer_preprocessing.py /app/consumer_preprocessing.py

WORKDIR /app

# Run the Kafka Consumer
CMD ["python", "consumer_preprocessing.py"]
