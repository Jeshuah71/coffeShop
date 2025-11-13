FROM python:3.13-slim

# System deps (curl for healthcheck, psycopg needs libpq)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl libpq5 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps early for caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app

# Expose dev port
EXPOSE 8000
