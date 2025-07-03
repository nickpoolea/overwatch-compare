# Full-stack Overwatch Comparison App
# Builds React frontend and serves everything through Django

FROM node:18-alpine as frontend-builder

# Build React frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend/ .
RUN npm run build

# Main Python stage
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./

# Copy startup scripts
COPY start.sh ./
COPY railway_start.py ./

# Make startup script executable
RUN chmod +x start.sh

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/build ./frontend/build/

# Create a simple startup script that shows environment variables
RUN echo '#!/bin/bash' > /app/debug_start.sh && \
    echo 'echo "=== DOCKER ENVIRONMENT DEBUG ===" ' >> /app/debug_start.sh && \
    echo 'echo "PORT: ${PORT:-NOT SET}"' >> /app/debug_start.sh && \
    echo 'echo "ALLOWED_HOSTS: ${ALLOWED_HOSTS:-NOT SET}"' >> /app/debug_start.sh && \
    echo 'echo "DEBUG: ${DEBUG:-NOT SET}"' >> /app/debug_start.sh && \
    echo 'echo "================================="' >> /app/debug_start.sh && \
    echo 'exec bash start.sh' >> /app/debug_start.sh && \
    chmod +x /app/debug_start.sh

# Don't run migrations/collectstatic during build - do it at runtime
# RUN python manage.py migrate --noinput
# RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Use our debug startup script
CMD ["bash", "/app/debug_start.sh"]
