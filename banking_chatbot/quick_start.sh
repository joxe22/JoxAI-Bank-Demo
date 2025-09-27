#!/bin/bash

# 🚀 Quick Start Script - Banking Chatbot
# Ubicación: /quick_start.sh
#
# Script para iniciar el proyecto de forma rápida sin configuración compleja

echo "🏦 Banking Chatbot - Quick Start"
echo "================================"

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Paso 1: Verificar Python
print_step "1. Verificando Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python3 no encontrado. Instálalo primero."
    exit 1
fi
print_success "Python3 encontrado: $(python3 --version)"

# Paso 2: Crear .env básico
print_step "2. Creando configuración básica..."
if [ ! -f ".env" ]; then
    cat > .env << EOF
# Configuración básica para desarrollo
DEBUG=True
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000
DATABASE_URL=sqlite:///./chatbot.db
SECRET_KEY=dev-secret-key-change-in-production
LOG_LEVEL=INFO
EOF
    print_success "Archivo .env creado con configuración básica"
else
    print_success "Archivo .env ya existe"
fi

# Paso 3: Instalar dependencias backend
print_step "3. Instalando dependencias del backend..."
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment creado"
fi

source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
print_success "Dependencias del backend instaladas"

cd ..

# Paso 4: Verificar instalación
print_step "4. Verificando instalación..."
cd backend
source venv/bin/activate

if python -c "from api.main import app" 2>/dev/null; then
    print_success "Backend verificado correctamente"
else
    print_error "Error en verificación del backend"
    exit 1
fi

cd ..

# Paso 5: Instrucciones finales
echo ""
echo "✅ ¡Listo para usar!"
echo "==================="
echo ""
echo "🚀 Para iniciar el backend:"
echo "   cd backend && source venv/bin/activate && python -m uvicorn api.main:app --reload --port 8000"
echo ""
echo "📱 O usa el script directo:"
echo "   python run_dev.py"
echo ""
echo "🌐 URLs:"
echo "   - API: http://localhost:8000"
echo "   - Docs: http://localhost:8000/docs"
echo "   - Health: http://localhost:8000/api/v1/health"
echo ""
echo "🧪 Test rápido:"
echo '   curl -X POST http://localhost:8000/api/v1/chat -H "Content-Type: application/json" -d '\''{"session_id":"test","message":"Hola"}'\'''
echo ""