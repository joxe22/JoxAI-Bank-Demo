# 🐳 Dockerfile para Frontend React
# Ubicación: frontend/chat-widget/Dockerfile

# Etapa 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Copiar package files
COPY package*.json ./

# Instalar dependencias
RUN npm ci --only=production

# Copiar código fuente
COPY . .

# Build para producción
RUN npm run build

# Etapa 2: Servir con nginx
FROM nginx:alpine

# Instalar curl para healthcheck
RUN apk add --no-cache curl

# Copiar archivos build
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar configuración nginx personalizada
COPY nginx.conf /etc/nginx/nginx.conf

# Exponer puerto
EXPOSE 3000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

# Comando por defecto
CMD ["nginx", "-g", "daemon off;"]