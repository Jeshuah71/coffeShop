FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl libpq5 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000
CMD ["bash", "-lc", "/app/entrypoint.sh gunicorn coffee_compass.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
