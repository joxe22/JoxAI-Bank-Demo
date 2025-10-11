#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Starting Banking ChatBot container..."

# Defaults suitable for production
export ENVIRONMENT=${ENVIRONMENT:-production}
export LOG_LEVEL=${LOG_LEVEL:-info}

# Validate required envs
if [[ -z "${DATABASE_URL:-}" ]]; then
  echo "❌ DATABASE_URL is not set" >&2
  exit 1
fi

# Run DB migrations (retry while DB becomes ready)
if [[ "${AUTO_MIGRATE:-true}" == "true" ]]; then
  echo "📦 Applying database migrations (alembic upgrade head)"
  attempt=0
  until alembic -c /app/banking_chatbot/backend/alembic.ini upgrade head; do
    attempt=$((attempt+1))
    if [[ $attempt -ge 20 ]]; then
      echo "❌ Failed to run migrations after $attempt attempts" >&2
      exit 1
    fi
    echo "⏳ DB not ready yet, retrying in 3s (attempt $attempt)"
    sleep 3
  done
fi

# Exec passed CMD (Gunicorn by default from Dockerfile)
exec "$@"
