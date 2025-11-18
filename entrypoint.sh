#!/usr/bin/env bash
set -e

echo "POSTGRES_USER=${POSTGRES_USER}"
echo "POSTGRES_PASSWORD=${POSTGRES_PASSWORD}"
echo "POSTGRES_HOST=${POSTGRES_HOST}"
echo "POSTGRES_PORT=${POSTGRES_PORT}"
echo "POSTGRES_DB=${POSTGRES_DB}"

echo "Waiting for Postgres at ${POSTGRES_HOST}:${POSTGRES_PORT} ..."
until python - <<'PY'
import os, socket, sys
host=os.environ.get("POSTGRES_HOST","db")
port=int(os.environ.get("POSTGRES_PORT","5432"))
s=socket.socket()
try:
    s.connect((host,port)); sys.exit(0)
except Exception: sys.exit(1)
PY
do
  sleep 1
  echo "  still waiting..."
done
echo "DB up"

python manage.py migrate
exec "$@"
