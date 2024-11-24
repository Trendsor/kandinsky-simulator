# Use an official Python runtime as a base image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY train.py .

# Define environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Run the Python training script
ENTRYPOINT ["python", "train.py"]
