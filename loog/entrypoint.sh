#!/bin/sh

echo "Waiting for MySQL..."

while ! nc -z db 3306; do
  sleep 0.1
done

echo "MySQL started"

python init.py
python manage.py migrate
python manage.py collectstatic --no-input --clear
exec "$@"
