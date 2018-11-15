#!/bin/sh

echo "Checking postgres is up..."
while ! nc -z service-types-database 5432; do
  sleep 0.1
done
echo "postgres running succesfully...."

echo "Starting app server..."
python manage.py run --host 0.0.0.0 --port 5000
