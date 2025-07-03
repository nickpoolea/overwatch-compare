#!/bin/bash
# Startup script for Railway deployment

echo "🚀 Starting Overwatch Comparison App..."

# Check if we need to change to backend directory
if [ -d "backend" ]; then
    echo "📁 Changing to backend directory..."
    cd backend
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
