FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && pip install --no-cache-dir psycopg2-binary alembic

# Set the working directory
WORKDIR /app

# Copy project files, including src and migrations
COPY src /app/src
COPY src/database/migrations/alembic /app/alembic
COPY src/database/migrations/alembic.ini /app/alembic.ini
COPY src/database/migrations/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install -r requirements.txt

# Set PYTHONPATH for Alembic to find src
ENV PYTHONPATH="/app:$PYTHONPATH"

# Default command
CMD ["alembic", "upgrade", "head"]
