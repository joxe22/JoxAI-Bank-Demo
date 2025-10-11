# Multi-stage Dockerfile: build frontend, run FastAPI backend with Gunicorn

# ---------- Frontend build ----------
FROM node:20-slim AS frontend-build
WORKDIR /app
COPY banking_chatbot/frontend/admin-panel/package*.json ./banking_chatbot/frontend/admin-panel/
WORKDIR /app/banking_chatbot/frontend/admin-panel
RUN npm ci
COPY banking_chatbot/frontend/admin-panel/ /app/banking_chatbot/frontend/admin-panel/
RUN npm run build

# ---------- Python runtime ----------
FROM python:3.11-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Create user
RUN useradd -m -u 10001 appuser

WORKDIR /app

# Install Python deps
COPY requirements.docker.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy app
COPY banking_chatbot /app/banking_chatbot

# Copy Alembic config lives under backend
ENV PYTHONPATH=/app/banking_chatbot/backend

# Inject built frontend into backend expected dist folder
COPY --from=frontend-build /app/banking_chatbot/frontend/admin-panel/dist /app/banking_chatbot/frontend/admin-panel/dist

# Runtime env
ENV HOST=0.0.0.0 \
    PORT=8000

# Expose API port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; import os; import sys; \
from urllib.error import URLError; \
url=f'http://127.0.0.1:{os.getenv("PORT","8000")}/health'; \
print('checking', url); \
urllib.request.urlopen(url).read()" || exit 1

# Entrypoint for migrations + server start
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]

# Default CMD: Gunicorn w/ Uvicorn workers, using existing config
WORKDIR /app/banking_chatbot/backend
USER appuser
CMD ["gunicorn", "app.main:app", "--config", "gunicorn_conf.py", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
