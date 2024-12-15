# Base Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary OS dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY docker/model_training/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model training source code into the container
COPY src /app/src

# Set PYTHONPATH to include `/app/src`
ENV PYTHONPATH=/app

# Set the default command to run the training script
CMD ["python", "src/model_training/train.py"]
