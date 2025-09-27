#!/usr/bin/env python3
"""
🚀 Script de Desarrollo Directo
Ubicación: /run_dev.py

Ejecuta el backend directamente sin Docker para desarrollo rápido.
Útil cuando no tienes Docker o quieres desarrollo más ágil.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Configurar PYTHONPATH
current_dir = Path(__file__).parent
backend_dir = current_dir / "backend"
sys.path.insert(0, str(backend_dir))

def check_dependencies():
    """Verificar que las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")

    try:
        import fastapi
        import uvicorn
        import pydantic
        print("✅ Dependencias básicas encontradas")
        return True
    except ImportError as e:
        print(f"❌ Falta dependencia: {e}")
        print("💡 Ejecuta: pip install -r backend/requirements.txt")
        return False

def setup_environment():
    """Configurar variables de entorno para desarrollo"""
    print("⚙️ Configurando entorno de desarrollo...")

    env_vars = {
        "PYTHONPATH": str(backend_dir),
        "DEBUG": "True",
        "ENVIRONMENT": "development",
        "LOG_LEVEL": "INFO"
    }

    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"  {key}={value}")

def run_backend():
    """Ejecutar el backend FastAPI"""
    print("\n🚀 Iniciando backend FastAPI...")
    print("📡 API disponible en: http://localhost:8000")
    print("📚 API Docs en: http://localhost:8000/docs")
    print("🏥 Health Check: http://localhost:8000/api/v1/health")
    print("\n" + "="*50)

    try:
        # Cambiar al directorio backend
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

        subprocess.run(cmd)

    except KeyboardInterrupt:
        print("\n\n🛑 Backend detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error ejecutando backend: {e}")

def main():
    """Función principal"""
    print("🏦 Banking Chatbot - Desarrollo Directo")
    print("=" * 40)

    # Verificar dependencias
    if not check_dependencies():
        return 1

    # Configurar entorno
    setup_environment()

    # Ejecutar backend
    run_backend()

    return 0

if __name__ == "__main__":
    sys.exit(main())