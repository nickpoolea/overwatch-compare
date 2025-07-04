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


# Copy backend code (preserve directory structure)
COPY backend ./backend

# Copy startup script
COPY railway_start.py ./

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/build ./frontend/build/

# Expose port
EXPOSE 8000

# Start the application
CMD ["python", "railway_start.py"]
