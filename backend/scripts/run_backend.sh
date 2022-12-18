#!/bin/bash

python ./manage.py collectstatic --noinput
python ./manage.py migrate  # Apply database migrations

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3