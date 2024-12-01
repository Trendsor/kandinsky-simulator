# Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the Alembic migration directory and related files
COPY database/migrations /app/migrations
COPY database/migrations/alembic.ini /app/alembic.ini
COPY src /app/src
COPY database/migrations/requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run Alembic migrations as the default command
CMD ["alembic", "upgrade", "head"]
