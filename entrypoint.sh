#!/usr/bin/env bash
set -e

echo "POSTGRES_USER=${POSTGRES_USER}"
if [ -n "${POSTGRES_PASSWORD}" ]; then
  echo "POSTGRES_PASSWORD=******"
else
  echo "POSTGRES_PASSWORD="
fi
echo "POSTGRES_HOST=${POSTGRES_HOST}"
echo "POSTGRES_PORT=${POSTGRES_PORT}"
echo "POSTGRES_DB=${POSTGRES_DB}"

export STATIC_ROOT="${STATIC_ROOT:-/app/staticfiles}"
echo "STATIC_ROOT=${STATIC_ROOT}"
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-coffee_compass.settings}"
mkdir -p "${STATIC_ROOT}"

python - <<'PY'
import os
from django.conf import settings
print("DJANGO_SETTINGS_MODULE=", os.environ.get("DJANGO_SETTINGS_MODULE"))
print("STATIC_ROOT setting=", settings.STATIC_ROOT, type(settings.STATIC_ROOT))
PY

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
python manage.py collectstatic --noinput
exec "$@"
