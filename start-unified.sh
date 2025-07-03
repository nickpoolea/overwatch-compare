#!/bin/bash

# Start Django in background
echo "Starting Django backend..."
python manage.py migrate --noinput
python manage.py runserver 127.0.0.1:8000 &

# Start Nginx in foreground
echo "Starting Nginx frontend server..."
nginx -g "daemon off;"
