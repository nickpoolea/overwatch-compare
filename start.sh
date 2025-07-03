#!/bin/bash
# Startup script for Railway deployment

echo "🚀 Starting Overwatch Comparison App..."
echo "📍 Current directory: $(pwd)"
echo "📁 Directory contents:"
ls -la

echo "=== ENVIRONMENT VARIABLES DEBUG ==="
echo "PORT: ${PORT:-NOT SET}"
echo "ALLOWED_HOSTS: ${ALLOWED_HOSTS:-NOT SET}"
echo "DEBUG: ${DEBUG:-NOT SET}"
echo "SECRET_KEY: $(if [ -n "$SECRET_KEY" ]; then echo "SET"; else echo "NOT SET"; fi)"
echo "CORS_ALLOWED_ORIGINS: ${CORS_ALLOWED_ORIGINS:-NOT SET}"
echo "==================================="

# Check if we need to change to backend directory
if [ -d "backend" ]; then
    echo "📁 Changing to backend directory..."
    cd backend
    echo "📁 Now in: $(pwd)"
fi

# Run migrations
echo "📋 Running Django migrations..."
python3 manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python3 manage.py collectstatic --noinput

# Start the server
PORT=${PORT:-8000}
echo "🌐 Starting Django server on port $PORT"
python3 manage.py runserver "0.0.0.0:$PORT"
