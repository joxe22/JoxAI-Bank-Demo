#!/usr/bin/env python3
"""
🔧 Banking Chatbot - Setup Completo de Desarrollo
Ubicación: /setup_dev.py

Script que instala, configura y verifica todo el entorno de desarrollo.
Detecta y soluciona automáticamente problemas comunes.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import List, Tuple, Optional
import json


class Colors:
    """Códigos ANSI para colores en terminal."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'


class DevSetup:
    """Configurador automático del entorno de desarrollo."""

    def __init__(self):
        self.root_dir = Path(__file__).parent.absolute()
        self.backend_dir = self.root_dir / "backend"
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def print_step(self, message: str):
        """Imprime paso actual."""
        print(f"\n{Colors.CYAN}🔄 {message}{Colors.END}")

    def print_success(self, message: str):
        """Imprime mensaje de éxito."""
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")

    def print_error(self, message: str):
        """Imprime mensaje de error."""
        print(f"{Colors.RED}❌ {message}{Colors.END}")

    def print_warning(self, message: str):
        """Imprime mensaje de advertencia."""
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

    def run_command(self, cmd: List[str], cwd: Optional[Path] = None) -> Tuple[bool, str]:
        """Ejecuta comando y devuelve (success, output)."""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=cwd or self.root_dir,
                timeout=300  # 5 minutos timeout
            )
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, "Comando timeout"
        except Exception as e:
            return False, str(e)

    def check_python_version(self) -> bool:
        """Verifica versión de Python."""
        self.print_step("Verificando versión de Python")

        version = sys.version_info
        if version.major != 3 or version.minor < 8:
            self.print_error(f"Python 3.8+ requerido. Actual: {version.major}.{version.minor}")
            return False

        self.print_success(f"Python {version.major}.{version.minor}.{version.micro} ✓")
        return True

    def check_system_deps(self) -> bool:
        """Verifica dependencias del sistema."""
        self.print_step("Verificando dependencias del sistema")

        deps = ['git', 'docker', 'make']
        optional_deps = ['postgresql', 'redis-server']

        all_good = True
        for dep in deps:
            if shutil.which(dep):
                self.print_success(f"{dep} encontrado")
            else:
                self.print_error(f"{dep} no encontrado (requerido)")
                all_good = False

        for dep in optional_deps:
            if shutil.which(dep):
                self.print_success(f"{dep} encontrado")
            else:
                self.print_warning(f"{dep} no encontrado (opcional, puede usar Docker)")

        return all_good

    def setup_virtual_env(self) -> bool:
        """Configura entorno virtual."""
        self.print_step("Configurando entorno virtual")

        venv_path = self.root_dir / "venv"

        if not venv_path.exists():
            success, output = self.run_command([sys.executable, "-m", "venv", "venv"])
            if not success:
                self.print_error(f"Error creando venv: {output}")
                return False
            self.print_success("Entorno virtual creado")
        else:
            self.print_success("Entorno virtual ya existe")

        return True

    def activate_and_install(self) -> bool:
        """Activa venv e instala dependencias."""
        self.print_step("Instalando dependencias de Python")

        # Detectar ejecutable de Python en venv
        if sys.platform.startswith("win"):
            python_exe = self.root_dir / "venv" / "Scripts" / "python.exe"
            pip_exe = self.root_dir / "venv" / "Scripts" / "pip.exe"
        else:
            python_exe = self.root_dir / "venv" / "bin" / "python"
            pip_exe = self.root_dir / "venv" / "bin" / "pip"

        if not python_exe.exists():
            self.print_error(f"Python en venv no encontrado: {python_exe}")
            return False

        # Actualizar pip
        success, output = self.run_command([str(pip_exe), "install", "--upgrade", "pip"])
        if not success:
            self.print_warning(f"Error actualizando pip: {output}")

        # Instalar requirements
        req_file = self.root_dir / "requirements.txt"
        if req_file.exists():
            success, output = self.run_command([
                str(pip_exe), "install", "-r", "requirements.txt"
            ])
            if not success:
                self.print_error(f"Error instalando requirements: {output}")
                return False
            self.print_success("Dependencias instaladas")
        else:
            self.print_warning("requirements.txt no encontrado")

        return True

    def setup_env_file(self) -> bool:
        """Configura archivo .env.development."""
        self.print_step("Configurando variables de entorno")

        env_example = self.root_dir / ".env.development.example"
        env_dev = self.root_dir / ".env.development"

        if not env_dev.exists() and env_example.exists():
            shutil.copy(env_example, env_dev)
            self.print_success("Archivo .env.development creado desde example")
            self.print_warning("⚠️  RECUERDA: Actualizar OPENAI_API_KEY en .env.development")
        elif env_dev.exists():
            self.print_success("Archivo .env.development ya existe")
        else:
            self.print_warning("No hay archivo .env example para copiar")

        return True

    def setup_directories(self) -> bool:
        """Crea directorios necesarios."""
        self.print_step("Creando estructura de directorios")

        dirs = [
            "logs",
            "data",
            "data/knowledge",
            "data/vector_store",
            "backend/models",
            "tests/fixtures"
        ]

        for dir_name in dirs:
            dir_path = self.root_dir / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)

        self.print_success("Directorios creados")
        return True

    def verify_imports(self) -> bool:
        """Verifica que los imports funcionen."""
        self.print_step("Verificando imports críticos")

        # Usar Python del venv
        if sys.platform.startswith("win"):
            python_exe = self.root_dir / "venv" / "Scripts" / "python.exe"
        else:
            python_exe = self.root_dir / "venv" / "bin" / "python"

        test_imports = [
            "import fastapi",
            "import uvicorn",
            "import openai",
            "import langchain",
            "import sentence_transformers",
            "import redis",
            "import sqlalchemy",
            "from backend.api.main import app"
        ]

        all_good = True
        for import_stmt in test_imports:
            success, output = self.run_command([
                str(python_exe), "-c", import_stmt
            ])
            if success:
                self.print_success(f"✓ {import_stmt}")
            else:
                self.print_error(f"✗ {import_stmt}")
                self.print_error(f"  Error: {output}")
                all_good = False

        return all_good

    def start_services(self) -> bool:
        """Intenta iniciar servicios de desarrollo."""
        self.print_step("Verificando servicios disponibles")

        services_status = {}

        # Check PostgreSQL
        success, _ = self.run_command(["pg_isready", "-h", "localhost", "-p", "5432"])
        services_status["PostgreSQL"] = success

        # Check Redis
        success, _ = self.run_command(["redis-cli", "-h", "localhost", "-p", "6379", "ping"])
        services_status["Redis"] = success

        # Check Qdrant (HTTP)
        try:
            import httpx
            with httpx.Client() as client:
                response = client.get("http://localhost:6333/health", timeout=5)
                services_status["Qdrant"] = response.status_code == 200
        except:
            services_status["Qdrant"] = False

        for service, status in services_status.items():
            if status:
                self.print_success(f"{service} disponible")
            else:
                self.print_warning(f"{service} no disponible (usa Docker si es necesario)")

        return True

    def create_makefile_if_missing(self) -> bool:
        """Crea Makefile básico si no existe."""
        makefile_path = self.root_dir / "Makefile"
        if makefile_path.exists():
            return True

        self.print_step("Creando Makefile básico")

        makefile_content = '''# Banking Chatbot - Makefile
.PHONY: help install dev test clean

help:
	@echo "Comandos disponibles:"
	@echo "  make install  - Instalar dependencias"
	@echo "  make dev      - Ejecutar en modo desarrollo"
	@echo "  make test     - Ejecutar tests"
	@echo "  make clean    - Limpiar archivos temporales"

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

dev:
	python run_dev.py

test:
	pytest tests/ -v

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf .pytest_cache
'''

        with open(makefile_path, 'w') as f:
            f.write(makefile_content)

        self.print_success("Makefile creado")
        return True

    def run_setup(self) -> bool:
        """Ejecuta setup completo."""
        print(f"{Colors.BOLD}{Colors.CYAN}")
        print("=" * 60)
        print("🚀 BANKING CHATBOT - SETUP DE DESARROLLO")
        print("=" * 60)
        print(f"{Colors.END}")

        steps = [
            ("Versión de Python", self.check_python_version),
            ("Dependencias del sistema", self.check_system_deps),
            ("Entorno virtual", self.setup_virtual_env),
            ("Instalación de paquetes", self.activate_and_install),
            ("Configuración de entorno", self.setup_env_file),
            ("Estructura de directorios", self.setup_directories),
            ("Makefile", self.create_makefile_if_missing),
            ("Verificación de imports", self.verify_imports),
            ("Estado de servicios", self.start_services),
        ]

        results = []
        for step_name, step_func in steps:
            try:
                success = step_func()
                results.append((step_name, success))
            except Exception as e:
                self.print_error(f"Error en {step_name}: {str(e)}")
                results.append((step_name, False))

        # Resumen
        print(f"\n{Colors.BOLD}📊 RESUMEN DEL SETUP{Colors.END}")
        print("-" * 40)

        success_count = 0
        for step_name, success in results:
            status = "✅" if success else "❌"
            print(f"{status} {step_name}")
            if success:
                success_count += 1

        print(f"\n{Colors.BOLD}Resultado: {success_count}/{len(results)} pasos completados{Colors.END}")

        if success_count == len(results):
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 SETUP COMPLETADO EXITOSAMENTE{Colors.END}")
            print("\nPróximos pasos:")
            print("1. Actualizar OPENAI_API_KEY en .env.development")
            print("2. Iniciar servicios: make dev")
            print("3. Probar API: http://localhost:8000/docs")
            return True
        else:
            print(f"\n{Colors.YELLOW}⚠️  Setup completado con advertencias{Colors.END}")
            print("Revisa los errores arriba y ejecuta de nuevo si es necesario.")
            return False


if __name__ == "__main__":
    setup = DevSetup()
    success = setup.run_setup()
    sys.exit(0 if success else 1)