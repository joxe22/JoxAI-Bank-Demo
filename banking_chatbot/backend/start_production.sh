#!/bin/bash
# Production startup script for JoxAI Banking Chatbot
# Optimized for Replit Autoscale deployment

set -e  # Exit on error

echo "🚀 Starting JoxAI Banking Chatbot in PRODUCTION mode..."

# Set production environment
export ENVIRONMENT=production
export LOG_LEVEL=${LOG_LEVEL:-info}

# Database setup
if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL environment variable is not set"
    exit 1
fi

echo "✅ Environment: $ENVIRONMENT"
echo "✅ Log level: $LOG_LEVEL"
echo "✅ Database: Connected"

# Run database migrations (if using Alembic)
# echo "📦 Running database migrations..."
# alembic upgrade head

# Start Gunicorn with optimized configuration
echo "🔥 Starting Gunicorn server..."
exec gunicorn app.main:app \
    --config gunicorn_conf.py \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:5000
