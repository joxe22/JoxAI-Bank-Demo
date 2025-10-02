#!/usr/bin/env python3
"""
🚀 Script de Desarrollo - Banking Chatbot
Ubicación: /run_dev.py

ACTUALIZADO: Imports arreglados y manejo robusto de errores.
Script principal para ejecutar el backend sin Docker.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Configurar colores
class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def print_success(msg): print(f"{Colors.GREEN}✅ {msg}{Colors.NC}")
def print_error(msg): print(f"{Colors.RED}❌ {msg}{Colors.NC}")
def print_warning(msg): print(f"{Colors.YELLOW}⚠️  {msg}{Colors.NC}")
def print_info(msg): print(f"{Colors.BLUE}ℹ️  {msg}{Colors.NC}")

def setup_environment():
    """Configurar entorno con PYTHONPATH correcto"""
    print_info("Configurando entorno...")

    current_dir = Path(__file__).parent
    backend_dir = current_dir / "backend"

    # Configurar PYTHONPATH para evitar errores de import
    python_path = f"{current_dir}:{backend_dir}:{backend_dir}/api:{backend_dir}/services:{backend_dir}/utils"

    env_vars = {
        "PYTHONPATH": python_path,
        "DEBUG": "True",
        "ENVIRONMENT": "development",
        "LOG_LEVEL": "INFO",
        "AI_ENABLED": "False",  # Empezar seguro en modo fallback
        "FALLBACK_TO_MOCK": "True"
    }

    for key, value in env_vars.items():
        os.environ[key] = value

    print_success("Entorno configurado correctamente")

def check_dependencies():
    """Verificar dependencias básicas"""
    print_info("Verificando dependencias...")

    try:
        import fastapi
        import uvicorn
        import pydantic
        print_success("Dependencias básicas encontradas")
        return True
    except ImportError as e:
        print_error(f"Falta dependencia: {e}")
        print_info("Ejecuta: pip install -r backend/requirements.txt")
        return False

def create_basic_structure():
    """Crear estructura básica de archivos __init__.py"""
    print_info("Verificando estructura de archivos...")

    init_files = [
        "backend/__init__.py",
        "backend/api/__init__.py",
        "backend/services/__init__.py",
        "backend/utils/__init__.py"
    ]

    for init_file in init_files:
        path = Path(init_file)
        if not path.exists():
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# Auto-generated __init__.py\n")
                print_success(f"Creado: {init_file}")
            except Exception as e:
                print_warning(f"No se pudo crear {init_file}: {e}")

def test_basic_imports():
    """Probar imports básicos"""
    print_info("Probando imports...")

    # Agregar paths
    current_dir = Path(__file__).parent
    backend_dir = current_dir / "backend"

    sys.path.insert(0, str(current_dir))
    sys.path.insert(0, str(backend_dir))

    try:
        # Test import principal
        from api.main import app
        print_success("Import principal funciona")
        return True
    except ImportError as e:
        print_warning(f"Import falló: {e}")
        print_info("Continuando en modo robusto...")
        return True  # Continuar de todos modos

def main():
    """Función principal simplificada"""
    print(f"""
{Colors.BLUE}🏦 Banking Chatbot - Desarrollo{Colors.NC}
{'='*40}
""")

    # Setup
    setup_environment()

    if not check_dependencies():
        return 1

    create_basic_structure()
    test_basic_imports()

    # Información del servidor
    print_info("🚀 Iniciando servidor FastAPI...")
    print_info("📡 API: http://localhost:8000")
    print_info("📚 Docs: http://localhost:8000/docs")
    print_info("🏥 Health: http://localhost:8000/api/v1/health")
    print("")
    print_warning("🤖 IA en modo fallback (configurar .env para IA real)")
    print_info("⏹️  Para detener: Ctrl+C")
    print("="*50)

    try:
        # Cambiar a directorio backend
        backend_dir = Path("backend")
        original_dir = os.getcwd()
        os.chdir(backend_dir)

        # Ejecutar uvicorn
        cmd = [
            sys.executable, "-m", "uvicorn",
            "api.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
            "--log-level", "info"
        ]

        print_success("🟢 Servidor iniciado")
        return subprocess.run(cmd).returncode

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🛑 Servidor detenido{Colors.NC}")
        return 0
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return 1
    finally:
        try:
            os.chdir(original_dir)
        except:
            pass

if __name__ == "__main__":
    sys.exit(main())