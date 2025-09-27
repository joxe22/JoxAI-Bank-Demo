# 🐳 Dockerfile para Backend FastAPI
# Ubicación: backend/Dockerfile

FROM python:3.11-slim

# Configurar directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero para aprovechar cache de Docker
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear usuario no-root para seguridad
RUN useradd --create-home --shell /bin/bash chatbot && \
    chown -R chatbot:chatbot /app
USER chatbot

# Configurar variables de entorno
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Exponer puerto
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Comando por defecto
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]