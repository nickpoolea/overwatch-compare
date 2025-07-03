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

# Make startup script executable
echo "🔧 Making startup script executable..."
chmod +x start.sh

# Note: collectstatic will be run by Django when needed in production

echo "✅ Build complete!"
