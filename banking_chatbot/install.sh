#!/bin/bash

# 📦 Script de Instalación Banking Chatbot
# Ubicación: /install.sh

set -e  # Salir si algún comando falla

echo "🏦 Banking Chatbot - Instalación"
echo "=================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes coloreados
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar Python
check_python() {
    print_status "Verificando Python..."

    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python encontrado: $PYTHON_VERSION"

        # Verificar que sea Python 3.9+
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
            print_success "Versión de Python compatible"
        else
            print_error "Se requiere Python 3.9 o superior"
            exit 1
        fi
    else
        print_error "Python3 no encontrado. Por favor instálalo primero."
        exit 1
    fi
}

# Verificar Node.js
check_node() {
    print_status "Verificando Node.js..."

    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_success "Node.js encontrado: $NODE_VERSION"
    else
        print_warning "Node.js no encontrado. Se instalará solo el backend."
        return 1
    fi

    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        print_success "NPM encontrado: v$NPM_VERSION"
        return 0
    else
        print_error "NPM no encontrado"
        return 1
    fi
}

# Crear directorios necesarios
create_directories() {
    print_status "Creando directorios necesarios..."

    directories=(
        "backend/api/config"
        "backend/api/models"
        "backend/api/routers"
        "backend/services"
        "backend/services/chat"
        "backend/utils"
        "frontend/chat-widget/src/components"
        "frontend/chat-widget/src/styles"
        "frontend/chat-widget/src/utils"
        "frontend/chat-widget/public"
        "config"
        "data/documents"
        "data/models"
        "data/uploads"
        "logs"
        "tests"
    )

    for dir in "${directories[@]}"; do
        mkdir -p "$dir"
        print_success "Directorio creado: $dir"
    done
}

# Instalar dependencias del backend
install_backend() {
    print_status "Instalando dependencias del backend..."

    cd backend

    # Crear virtual environment si no existe
    if [ ! -d "venv" ]; then
        print_status "Creando virtual environment..."
        python3 -m venv venv
    fi

    # Activar virtual environment
    source venv/bin/activate

    # Actualizar pip
    pip install --upgrade pip

    # Instalar dependencias
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Dependencias del backend instaladas"
    else
        print_error "❌ requirements.txt no encontrado en backend/"
        exit 1
    fi

    cd ..
}

# Instalar dependencias del frontend
install_frontend() {
    if ! check_node; then
        print_warning "Saltando instalación del frontend (Node.js no disponible)"
        return
    fi

    print_status "Instalando dependencias del frontend..."

    if [ ! -f "frontend/chat-widget/package.json" ]; then
        print_error "❌ package.json no encontrado en frontend/chat-widget/"
        return 1
    fi

    cd frontend/chat-widget
    npm install
    print_success "Dependencias del frontend instaladas"
    cd ../..
}

# Configurar archivos de configuración
setup_config() {
    print_status "Configurando archivos de configuración..."

    # Crear .env desde .env.example si no existe
    if [ ! -f ".env" ] && [ -f ".env.example" ]; then
        cp .env.example .env
        print_success "Archivo .env creado desde .env.example"
        print_warning "⚠️  IMPORTANTE: Edita .env con tus claves reales"
    fi

    # Copiar template de secrets si no existe
    if [ ! -f "config/secrets.yaml" ] && [ -f "config/secrets.yaml.template" ]; then
        cp config/secrets.yaml.template config/secrets.yaml
        print_success "Template de secrets copiado a config/secrets.yaml"
        print_warning "⚠️  IMPORTANTE: Edita config/secrets.yaml con tus claves reales"
    fi
}

# Verificar que todos los archivos críticos existen
verify_files() {
    print_status "Verificando archivos críticos..."

    critical_files=(
        "backend/api/main.py"
        "backend/api/__init__.py"
        "backend/api/routers/__init__.py"
        "backend/api/routers/health.py"
        "backend/api/routers/chat.py"
        "backend/api/models/__init__.py"
        "backend/api/models/schemas.py"
        "backend/services/chat/chat_service.py"
        "backend/utils/session_manager.py"
        "backend/requirements.txt"
    )

    for file in "${critical_files[@]}"; do
        if [ -f "$file" ]; then
            print_success "✓ $file"
        else
            print_error "✗ FALTA: $file"
            return 1
        fi
    done

    # Verificar frontend si Node está disponible
    if command -v node &> /dev/null; then
        frontend_files=(
            "frontend/chat-widget/package.json"
            "frontend/chat-widget/src/main.jsx"
            "frontend/chat-widget/src/components/ChatWidget.jsx"
            "frontend/chat-widget/index.html"
        )

        for file in "${frontend_files[@]}"; do
            if [ -f "$file" ]; then
                print_success "✓ $file"
            else
                print_error "✗ FALTA: $file"
                return 1
            fi
        done
    fi

    return 0
}

# Verificar instalación
verify_installation() {
    print_status "Verificando instalación..."

    # Verificar que se pueda importar la app
    cd backend
    source venv/bin/activate

    if python -c "from api.main import app; print('✅ Backend OK')" 2>/dev/null; then
        print_success "Backend verificado correctamente"
    else
        print_error "Error en la verificación del backend"
        print_error "Intenta ejecutar manualmente: cd backend && source venv/bin/activate && python -c 'from api.main import app'"
        return 1
    fi

    cd ..
    return 0
}

# Mostrar instrucciones finales
show_instructions() {
    echo ""
    echo "🎉 ¡Instalación completada!"
    echo "=========================="
    echo ""
    echo "📋 Próximos pasos:"
    echo ""
    echo "1. Configurar variables en .env (si usas OpenAI, etc.)"
    echo "2. Ejecutar el proyecto:"
    echo ""
    echo "   🚀 Opción A - Desarrollo directo (RECOMENDADO):"
    echo "   $ python run_dev.py"
    echo ""
    echo "   🔧 Opción B - Manual:"
    echo "   $ cd backend && source venv/bin/activate && python -m uvicorn api.main:app --reload"
    echo ""
    echo "   🎨 Opción C - Frontend (en otra terminal):"
    echo "   $ cd frontend/chat-widget && npm run dev"
    echo ""
    echo "🌐 URLs importantes:"
    echo "   - Backend API: http://localhost:8000"
    echo "   - API Docs: http://localhost:8000/docs"
    echo "   - Health Check: http://localhost:8000/api/v1/health"
    echo "   - Frontend: http://localhost:3000 (si instalaste Node.js)"
    echo ""
    echo "🧪 Para probar:"
    echo "   curl http://localhost:8000/api/v1/health"
    echo ""
}

# Función principal
main() {
    # Verificar prerrequisitos
    check_python

    # Crear directorios
    create_directories

    # Verificar archivos críticos
    if ! verify_files; then
        print_error "Faltan archivos críticos. Asegúrate de tener todos los archivos del proyecto."
        exit 1
    fi

    # Instalar dependencias
    install_backend
    install_frontend

    # Configurar archivos
    setup_config

    # Verificar instalación
    if verify_installation; then
        show_instructions
    else
        print_error "La instalación falló en la verificación"
        print_warning "Intenta ejecutar manualmente el backend para ver el error específico"
        exit 1
    fi
}

# Ejecutar si es llamado directamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi