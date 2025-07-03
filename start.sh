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

echo "🔍 Checking for React build files..."
if [ -d "frontend/build" ]; then
    echo "✅ Found frontend/build directory"
    echo "📁 Contents of frontend/build:"
    ls -la frontend/build/
    if [ -f "frontend/build/index.html" ]; then
        echo "✅ Found index.html"
        echo "📄 First few lines of index.html:"
        head -10 frontend/build/index.html
    else
        echo "❌ index.html not found!"
    fi
    if [ -d "frontend/build/static" ]; then
        echo "✅ Found static directory"
        echo "📁 Contents of frontend/build/static:"
        ls -la frontend/build/static/
    else
        echo "❌ static directory not found!"
    fi
else
    echo "❌ frontend/build directory not found!"
    echo "📁 Looking for alternative paths..."
    find . -name "index.html" -type f 2>/dev/null || echo "No index.html files found"
fi

# Run migrations
echo "📋 Running Django migrations..."
python3 manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python3 manage.py collectstatic --noinput

# Check what was collected
echo "🔍 Checking collected static files..."
if [ -d "staticfiles" ]; then
    echo "✅ staticfiles directory exists"
    ls -la staticfiles/ | head -10
else
    echo "❌ staticfiles directory not found!"
fi

# Start the server
PORT=${PORT:-8000}
echo "🌐 Starting Django server on port $PORT"
python3 manage.py runserver "0.0.0.0:$PORT"
