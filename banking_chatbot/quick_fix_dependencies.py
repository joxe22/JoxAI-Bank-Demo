#!/usr/bin/env python3
"""
🔧 Quick Fix - Dependencias RAG System
Ubicación: /quick_fix_dependencies.py

Arreglo rápido para instalar las dependencias faltantes del sistema RAG.
Específicamente para el error "No module named 'openai'".
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description=""):
    """Ejecuta comando con output visible."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, check=True, text=True, capture_output=False)
        print(f"✅ {description} - OK")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Error: {e}")
        return False

def main():
    print("🔧 ARREGLO RÁPIDO - DEPENDENCIAS RAG SYSTEM")
    print("=" * 50)

    # Verificar que estamos en venv
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  No estás en un entorno virtual. Se recomienda usar venv.")
        response = input("¿Continuar de todos modos? (y/N): ")
        if response.lower() != 'y':
            return

    print("📦 Instalando dependencias críticas faltantes...")

    # Lista de dependencias críticas en orden de instalación
    critical_deps = [
        # Core framework
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.5.0",

        # OpenAI y LLM
        "openai>=1.3.0",
        "tiktoken>=0.5.0",

        # LangChain essentials
        "langchain>=0.0.300",
        "langchain-openai>=0.0.2",

        # ML y NLP básicos
        "sentence-transformers>=2.2.0",
        "transformers>=4.35.0",

        # Vector DB
        "qdrant-client>=1.7.0",

        # Databases
        "redis>=5.0.0",
        "psycopg2-binary>=2.9.0",
        "sqlalchemy>=2.0.0",

        # HTTP y async
        "httpx>=0.25.0",
        "aioredis>=2.0.0",

        # Utils
        "python-dotenv>=1.0.0",
        "python-multipart>=0.0.6",
        "PyPDF2>=3.0.0",
        "pandas>=2.0.0",
        "nltk>=3.8.0"
    ]

    print(f"Instalando {len(critical_deps)} paquetes críticos...")

    # Instalar en lotes pequeños para evitar conflictos
    batch_size = 3
    for i in range(0, len(critical_deps), batch_size):
        batch = critical_deps[i:i + batch_size]
        cmd = [sys.executable, "-m", "pip", "install", "--upgrade"] + batch

        batch_desc = f"Lote {i//batch_size + 1}: {', '.join([p.split('>=')[0] for p in batch])}"
        success = run_command(cmd, batch_desc)

        if not success:
            print(f"❌ Error en {batch_desc}")
            print("Intentando instalar uno por uno...")

            # Instalar individualmente si falla el lote
            for package in batch:
                single_cmd = [sys.executable, "-m", "pip", "install", "--upgrade", package]
                run_command(single_cmd, f"Individual: {package.split('>=')[0]}")

    print("\n🧪 Verificando instalación...")

    # Verificar imports críticos
    test_imports = [
        ("fastapi", "import fastapi"),
        ("openai", "import openai"),
        ("langchain", "import langchain"),
        ("qdrant_client", "import qdrant_client"),
        ("sentence_transformers", "import sentence_transformers"),
        ("redis", "import redis"),
        ("httpx", "import httpx"),
        ("dotenv", "from dotenv import load_dotenv")
    ]

    failed_imports = []
    for name, import_cmd in test_imports:
        try:
            exec(import_cmd)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name}")
            failed_imports.append(name)

    if failed_imports:
        print(f"\n⚠️  Aún faltan: {', '.join(failed_imports)}")
        print("Ejecuta: pip install " + " ".join(failed_imports))
    else:
        print(f"\n🎉 ¡Todas las dependencias críticas instaladas correctamente!")
        print("\nPróximos pasos:")
        print("1. Configurar OPENAI_API_KEY en .env:")
        print("   echo 'OPENAI_API_KEY=sk-tu-api-key-aqui' >> .env")
        print("2. Probar el sistema:")
        print("   python start_rag_system.py --mode docker")

if __name__ == "__main__":
    main()