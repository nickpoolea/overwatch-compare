#!/bin/bash

# Simple deployment script
# Usage: ./deploy.sh [production|development]

ENV=${1:-development}

echo "🚀 Deploying Overwatch Comparison App for $ENV..."

if [ "$ENV" = "production" ]; then
    echo "📋 Production deployment"
    
    # Stop existing containers
    docker-compose down
    
    # Build and start with production settings
    SECRET_KEY=${SECRET_KEY:-$(openssl rand -base64 32)} \
    DEBUG=False \
    DOMAIN=${DOMAIN:-yourdomain.com} \
    docker-compose up --build -d
    
    echo "✅ Production deployment complete!"
    echo "🌐 App available at: http://localhost:8000"
    
elif [ "$ENV" = "development" ]; then
    echo "📋 Development deployment"
    
    # Stop existing containers
    docker-compose down
    
    # Build and start with development settings
    SECRET_KEY=dev-secret-key \
    DEBUG=True \
    DOMAIN=localhost \
    docker-compose up --build -d
    
    echo "✅ Development deployment complete!"
    echo "🌐 App available at: http://localhost:8000"
    
else
    echo "❌ Invalid environment. Use 'production' or 'development'"
    exit 1
fi

echo "📊 Container status:"
docker-compose ps
