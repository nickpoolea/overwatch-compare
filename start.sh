#!/bin/bash
# Startup script for Railway deployment

echo "🚀 Starting Overwatch Comparison App..."

# Change to backend directory
cd backend

# Run migrations
echo "📋 Running Django migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Start the server
echo "🌐 Starting Django server..."
python manage.py runserver 0.0.0.0:$PORT
