# 🚀 Makefile para Banking Chatbot
# Ubicación: /Makefile (raíz del proyecto)

.PHONY: help install dev build clean test docker

# Colores para output
RED=\033[0;31m
GREEN=\033[0;32m
YELLOW=\033[1;33m
BLUE=\033[0;34m
NC=\033[0m # No Color

help: ## 📋 Mostrar ayuda
	@echo "$(BLUE)🏦 Banking Chatbot - Comandos Disponibles$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## 📦 Instalar todas las dependencias
	@echo "$(YELLOW)📦 Instalando dependencias del backend...$(NC)"
	cd backend && pip install -r requirements.txt
	@echo "$(YELLOW)📦 Instalando dependencias del frontend...$(NC)"
	cd frontend/chat-widget && npm install
	@echo "$(GREEN)✅ Dependencias instaladas correctamente$(NC)"

dev-backend: ## 🚀 Ejecutar backend en modo desarrollo
	@echo "$(YELLOW)🚀 Iniciando backend en modo desarrollo...$(NC)"
	cd backend && python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## 🎨 Ejecutar frontend en modo desarrollo
	@echo "$(YELLOW)🎨 Iniciando frontend en modo desarrollo...$(NC)"
	cd frontend/chat-widget && npm run dev

dev: ## 🔄 Ejecutar backend y frontend simultáneamente
	@echo "$(YELLOW)🔄 Iniciando desarrollo completo...$(NC)"
	@echo "$(BLUE)Abriendo terminales para backend y frontend$(NC)"
	@if command -v tmux >/dev/null 2>&1; then \
		tmux new-session -d -s banking-chatbot; \
		tmux split-window -h; \
		tmux send-keys -t 0 'make dev-backend' C-m; \
		tmux send-keys -t 1 'make dev-frontend' C-m; \
		tmux attach-session -s banking-chatbot; \
	else \
		echo "$(RED)❌ tmux no está instalado. Ejecuta 'make dev-backend' y 'make dev-frontend' en terminales separadas$(NC)"; \
	fi

build-frontend: ## 🏗️ Construir frontend para producción
	@echo "$(YELLOW)🏗️ Construyendo frontend...$(NC)"
	cd frontend/chat-widget && npm run build
	@echo "$(GREEN)✅ Frontend construido en frontend/chat-widget/dist$(NC)"

test-backend: ## 🧪 Ejecutar tests del backend
	@echo "$(YELLOW)🧪 Ejecutando tests del backend...$(NC)"
	cd backend && python -m pytest tests/ -v

test-frontend: ## 🧪 Ejecutar tests del frontend
	@echo "$(YELLOW)🧪 Ejecutando tests del frontend...$(NC)"
	cd frontend/chat-widget && npm run test

test: ## 🧪 Ejecutar todos los tests
	@echo "$(YELLOW)🧪 Ejecutando todos los tests...$(NC)"
	make test-backend
	make test-frontend

lint-backend: ## 🔍 Verificar código del backend
	@echo "$(YELLOW)🔍 Verificando código del backend...$(NC)"
	cd backend && python -m flake8 . --max-line-length=100 --exclude=__pycache__,migrations

lint-frontend: ## 🔍 Verificar código del frontend
	@echo "$(YELLOW)🔍 Verificando código del frontend...$(NC)"
	cd frontend/chat-widget && npm run lint

lint: ## 🔍 Verificar todo el código
	make lint-backend
	make lint-frontend

clean: ## 🧹 Limpiar archivos temporales
	@echo "$(YELLOW)🧹 Limpiando archivos temporales...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf backend/.pytest_cache
	rm -rf frontend/chat-widget/node_modules/.cache
	rm -rf frontend/chat-widget/dist
	@echo "$(GREEN)✅ Limpieza completada$(NC)"

docker-build: ## 🐳 Construir imágenes Docker
	@echo "$(YELLOW)🐳 Construyendo imágenes Docker...$(NC)"
	docker build -t banking-chatbot-api ./backend
	docker build -t banking-chatbot-frontend ./frontend/chat-widget
	@echo "$(GREEN)✅ Imágenes Docker construidas$(NC)"

docker-up: ## 🐳 Ejecutar con Docker Compose
	@echo "$(YELLOW)🐳 Iniciando servicios con Docker Compose...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ Servicios iniciados$(NC)"
	@echo "$(BLUE)🌐 Frontend: http://localhost:3000$(NC)"
	@echo "$(BLUE)📡 Backend API: http://localhost:8000$(NC)"
	@echo "$(BLUE)📚 API Docs: http://localhost:8000/docs$(NC)"

docker-down: ## 🐳 Detener servicios Docker
	@echo "$(YELLOW)🐳 Deteniendo servicios Docker...$(NC)"
	docker-compose down
	@echo "$(GREEN)✅ Servicios detenidos$(NC)"

logs: ## 📋 Ver logs de la aplicación
	@echo "$(YELLOW)📋 Mostrando logs...$(NC)"
	docker-compose logs -f

setup: install ## 🎯 Setup inicial completo del proyecto
	@echo "$(YELLOW)🎯 Setup inicial del proyecto...$(NC)"
	mkdir -p data/documents data/models logs
	cp config/secrets.yaml.template config/secrets.yaml || true
	@echo "$(GREEN)✅ Setup inicial completado$(NC)"
	@echo "$(BLUE)📝 Recuerda configurar las variables en config/secrets.yaml$(NC)"

status: ## 📊 Ver estado de servicios
	@echo "$(BLUE)📊 Estado de los servicios:$(NC)"
	@echo ""
	@curl -s http://localhost:8000/api/v1/health 2>/dev/null | python -m json.tool || echo "$(RED)❌ Backend no disponible$(NC)"
	@echo ""
	@curl -s http://localhost:3000 2>/dev/null >/dev/null && echo "$(GREEN)✅ Frontend disponible en http://localhost:3000$(NC)" || echo "$(RED)❌ Frontend no disponible$(NC)"

quick-start: ## ⚡ Inicio rápido para desarrollo
	@echo "$(BLUE)⚡ Inicio rápido del proyecto$(NC)"
	@echo "$(YELLOW)1. Instalando dependencias...$(NC)"
	@make install
	@echo "$(YELLOW)2. Iniciando servicios de desarrollo...$(NC)"
	@make dev

# Comandos de producción
deploy-staging: ## 🚀 Deploy a staging
	@echo "$(YELLOW)🚀 Deploying a staging...$(NC)"
	# Aquí irían los comandos específicos de deploy

deploy-prod: ## 🌟 Deploy a producción
	@echo "$(RED)⚠️  Deploy a producción requiere confirmación$(NC)"
	@echo "$(YELLOW)Ejecuta: make deploy-prod-confirm$(NC)"

deploy-prod-confirm: ## 🌟 Confirmar deploy a producción
	@echo "$(RED)🌟 Deploying a PRODUCCIÓN...$(NC)"
	# Aquí irían los comandos específicos de deploy a prod