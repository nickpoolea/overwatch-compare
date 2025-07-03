#!/bin/bash
# Startup script for Railway deployment

echo "🚀 Starting Overwatch Comparison App..."

# We're already in the right directory in Docker (/app)
# Backend files are copied directly to /app

# Run migrations
echo "📋 Running Django migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Start the server
echo "🌐 Starting Django server..."
python manage.py runserver 0.0.0.0:$PORT
