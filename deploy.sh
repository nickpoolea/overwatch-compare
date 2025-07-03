#!/bin/bash

# Simple deployment script for Docker
# Usage: ./deploy.sh [production|development]

ENV=${1:-development}

echo "🚀 Deploying Overwatch Comparison App for $ENV..."

if [ "$ENV" = "production" ]; then
    echo "📋 Production deployment"
    
    # Stop existing containers
    docker-compose down
    
    # Build and start with production settings
    DJANGO_SETTINGS_MODULE=overwatch_api.settings \
    DEBUG=False \
    docker-compose up --build -d
    
    echo "✅ Production deployment complete!"
    echo "🌐 App should be available at your domain"
    
elif [ "$ENV" = "development" ]; then
    echo "📋 Development deployment"
    
    # Stop existing containers
    docker-compose down
    
    # Build and start with development settings
    DEBUG=True \
    docker-compose up --build -d
    
    echo "✅ Development deployment complete!"
    echo "🌐 Frontend: http://localhost"
    echo "🔧 Backend: http://localhost:8000"
    
else
    echo "❌ Invalid environment. Use 'production' or 'development'"
    exit 1
fi

echo "📊 Container status:"
docker-compose ps
