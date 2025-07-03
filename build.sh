#!/bin/bash
# Build script for Railway deployment

echo "🚀 Building Overwatch Comparison App for Railway..."

# Build React frontend
echo "📦 Building React frontend..."
npm install --prefix frontend
npm run build --prefix frontend

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -r backend/requirements.txt

# Collect Django static files
echo "📁 Collecting static files..."
python backend/manage.py collectstatic --noinput

echo "✅ Build complete!"
