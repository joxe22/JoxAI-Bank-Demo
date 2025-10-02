#!/usr/bin/env python3
"""
🚀 Start RAG System - Banking Chatbot
Ubicación: /start_rag_system.py

Script de arranque completo del sistema RAG.
Incluye verificaciones, inicialización y arranque de servicios.
"""

import asyncio
import os
import sys
import subprocess
from pathlib import Path
import argparse

# Agregar paths
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "backend"))

# Configurar variables de entorno antes de imports
os.environ.setdefault("PYTHONPATH", str(current_dir))


class Colors:
    """Códigos ANSI para colores."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_banner():
    """Imprime banner de inicio."""
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("=" * 80)
    print("🚀 BANKING CHATBOT - SISTEMA RAG")
    print("=" * 80)
    print("Iniciando sistema completo con:")
    print("• Vector Database (Qdrant)")
    print("• Knowledge Ingestion Pipeline")
    print("• RAG System (LLM + Retrieval)")
    print("• FastAPI Backend")
    print("• Monitoring & Health Checks")
    print("=" * 80)
    print(f"{Colors.END}")


def print_step(message: str):
    """Imprime paso actual."""
    print(f"\n{Colors.BLUE}🔄 {message}{Colors.END}")


def print_success(message: str):
    """Imprime mensaje de éxito."""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")


def print_error(message: str):
    """Imprime mensaje de error."""
    print(f"{Colors.RED}❌ {message}{Colors.END}")


def print_warning(message: str):
    """Imprime advertencia."""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")


class SystemStarter:
    """Gestor de arranque del sistema RAG."""

    def __init__(self, mode: str = "local"):
        self.mode = mode  # local, docker, production
        self.root_dir = current_dir
        self.services_status = {}

    async def start_system(self):
        """Inicia el sistema completo."""
        print_banner()

        try:
            # 1. Verificaciones previas
            await self._pre_flight_checks()

            # 2. Configurar entorno
            await self._setup_environment()

            # 3. Iniciar servicios según modo
            if self.mode == "docker":
                await self._start_docker_services()
            else:
                await self._start_local_services()

            # 4. Verificar que todo esté funcionando
            await self._verify_system_health()

            # 5. Cargar conocimiento inicial
            await self._load_initial_knowledge()

            # 6. Iniciar API principal
            await self._start_main_api()

        except Exception as e:
            print_error(f"Error durante el arranque: {e}")
            await self._cleanup_on_error()
            raise

    async def _pre_flight_checks(self):
        """Verificaciones previas al arranque."""
        print_step("Verificaciones previas")

        # Verificar Python
        version = sys.version_info
        if version.major != 3 or version.minor < 8:
            raise Exception(f"Python 3.8+ requerido. Actual: {version.major}.{version.minor}")
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")

        # Verificar archivo .env
        env_files = [".env.development", ".env"]
        env_found = False
        for env_file in env_files:
            if (self.root_dir / env_file).exists():
                print_success(f"Archivo de configuración encontrado: {env_file}")
                env_found = True
                break

        if not env_found:
            print_warning("No se encontró archivo .env, usando configuración por defecto")

        # Verificar OPENAI_API_KEY
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key or openai_key.startswith("sk-your"):
            print_warning("OPENAI_API_KEY no configurada correctamente")
            print_warning("Algunas funcionalidades pueden no funcionar")
        else:
            print_success("OPENAI_API_KEY configurada")

        # Verificar dependencias instaladas
        try:
            import fastapi
            import uvicorn
            import qdrant_client
            import openai
            import langchain
            print_success("Dependencias principales instaladas")
        except ImportError as e:
            raise Exception(f"Dependencia faltante: {e}")

    async def _setup_environment(self):
        """Configura el entorno de ejecución."""
        print_step("Configurando entorno")

        # Crear directorios necesarios
        dirs = ["logs", "data", "data/knowledge", "data/vector_store"]
        for dir_name in dirs:
            (self.root_dir / dir_name).mkdir(parents=True, exist_ok=True)
        print_success("Directorios creados")

        # Cargar variables de entorno
        try:
            from dotenv import load_dotenv

            # Cargar .env.development primero, luego .env
            env_development = self.root_dir / ".env.development"
            env_default = self.root_dir / ".env"

            if env_development.exists():
                load_dotenv(env_development)
                print_success("Configuración de desarrollo cargada")
            elif env_default.exists():
                load_dotenv(env_default)
                print_success("Configuración por defecto cargada")

        except ImportError:
            print_warning("python-dotenv no instalado, saltando carga de .env")

    async def _start_local_services(self):
        """Inicia servicios locales necesarios."""
        print_step("Iniciando servicios locales")

        # Verificar si los servicios ya están corriendo
        services_to_check = [
            ("Qdrant", "http://localhost:6333/health"),
            ("Redis", "redis://localhost:6379"),
            ("PostgreSQL", "postgresql://postgres@localhost:5432")
        ]

        for service_name, service_url in services_to_check:
            if await self._check_service(service_name, service_url):
                print_success(f"{service_name} ya está ejecutándose")
                self.services_status[service_name] = "running"
            else:
                print_warning(f"{service_name} no disponible")
                self.services_status[service_name] = "unavailable"

        # Si no hay servicios, ofrecer iniciar con Docker
        unavailable = [k for k, v in self.services_status.items() if v == "unavailable"]
        if unavailable:
            print_warning(f"Servicios no disponibles: {', '.join(unavailable)}")
            print_warning("Considera usar: python start_rag_system.py --mode docker")

    async def _start_docker_services(self):
        """Inicia servicios usando Docker Compose."""
        print_step("Iniciando servicios con Docker")

        # Verificar que Docker esté disponible
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
            subprocess.run(["docker-compose", "--version"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            raise Exception("Docker o Docker Compose no están instalados")

        # Iniciar servicios básicos
        compose_file = self.root_dir / "docker-compose.rag.yml"
        if not compose_file.exists():
            raise Exception("docker-compose.rag.yml no encontrado")

        print_success("Iniciando servicios Docker...")
        try:
            # Solo servicios de infraestructura, no la API principal
            services = ["qdrant", "postgres", "redis"]
            cmd = ["docker-compose", "-f", str(compose_file), "up", "-d"] + services

            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print_success("Servicios Docker iniciados")

            # Esperar a que los servicios estén listos
            await self._wait_for_docker_services()

        except subprocess.CalledProcessError as e:
            print_error(f"Error iniciando Docker: {e}")
            print_error(f"Salida: {e.stdout}")
            print_error(f"Error: {e.stderr}")
            raise

    async def _wait_for_docker_services(self):
        """Espera a que los servicios Docker estén listos."""
        print_step("Esperando servicios Docker...")

        services = [
            ("Qdrant", "http://localhost:6333/health"),
            ("PostgreSQL", None),  # Se verifica con docker compose ps
            ("Redis", None)
        ]

        max_wait = 60  # segundos
        wait_time = 0

        while wait_time < max_wait:
            all_ready = True

            for service_name, health_url in services:
                if health_url:
                    if not await self._check_service(service_name, health_url):
                        all_ready = False
                        break
                else:
                    # Para servicios sin health check específico
                    if not await self._check_docker_service_health(service_name.lower()):
                        all_ready = False
                        break

            if all_ready:
                print_success("Todos los servicios Docker están listos")
                return

            print(f"Esperando servicios... ({wait_time}s/{max_wait}s)")
            await asyncio.sleep(5)
            wait_time += 5

        raise Exception("Timeout esperando servicios Docker")

    async def _check_service(self, service_name: str, url: str) -> bool:
        """Verifica si un servicio está disponible."""
        try:
            if url.startswith("http"):
                import httpx
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, timeout=5.0)
                    return response.status_code == 200
            elif url.startswith("redis"):
                import redis
                r = redis.from_url(url)
                r.ping()
                return True
            elif url.startswith("postgresql"):
                import psycopg2
                conn = psycopg2.connect(url)
                conn.close()
                return True
        except:
            pass
        return False

    async def _check_docker_service_health(self, service_name: str) -> bool:
        """Verifica salud de servicio Docker."""
        try:
            cmd = ["docker-compose", "-f", "docker-compose.rag.yml", "ps", service_name]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return "Up" in result.stdout
        except:
            return False

    async def _verify_system_health(self):
        """Verifica la salud del sistema completo."""
        print_step("Verificando salud del sistema")

        try:
            # Verificar componentes del sistema RAG
            from backend.core.vector_db import get_vector_db
            vector_db = await get_vector_db()
            print_success("Vector Database conectada")

            from backend.core.knowledge_ingestion import get_ingestion_pipeline
            pipeline = await get_ingestion_pipeline()
            print_success("Pipeline de ingesta inicializado")

            from backend.core.rag_system import get_rag_system
            rag_system = await get_rag_system()
            print_success("Sistema RAG inicializado")

        except Exception as e:
            print_error(f"Error en verificación de salud: {e}")
            raise

    async def _load_initial_knowledge(self):
        """Carga conocimiento inicial si es necesario."""
        print_step("Verificando conocimiento inicial")

        try:
            from backend.core.vector_db import get_vector_db
            vector_db = await get_vector_db()

            # Verificar si ya hay documentos indexados
            info = await vector_db.get_collection_info()
            doc_count = info.get('vectors_count', 0)

            if doc_count > 0:
                print_success(f"Base de conocimiento ya contiene {doc_count} documentos")
                return

            print_warning("Base de conocimiento vacía, cargando datos de ejemplo...")

            # Cargar conocimiento de ejemplo
            from backend.core.knowledge_ingestion import get_ingestion_pipeline
            pipeline = await get_ingestion_pipeline()

            # Buscar archivos de conocimiento
            knowledge_dir = self.root_dir / "data" / "knowledge"
            if knowledge_dir.exists():
                results = await pipeline.ingest_directory(knowledge_dir)
                if results['processed_files'] > 0:
                    print_success(f"Cargados {results['total_chunks']} chunks de conocimiento")
                    return

            # Si no hay archivos, crear conocimiento básico
            await self._create_sample_knowledge()

        except Exception as e:
            print_warning(f"Error cargando conocimiento inicial: {e}")

    async def _create_sample_knowledge(self):
        """Crea conocimiento de ejemplo."""
        print_step("Creando conocimiento de ejemplo")

        sample_content = """
        Banco Demo - Información General
        
        Horarios de Atención:
        • Sucursales: Lunes a Viernes 8:00 AM - 4:00 PM
        • Sábados: 8:00 AM - 12:00 PM  
        • Cajeros automáticos: Disponibles 24/7
        • Línea de atención: 123-456-7890 (24 horas)
        
        Productos Principales:
        
        Cuenta de Ahorro:
        • Apertura desde $50,000
        • Tasa de interés: 4.5% EA
        • Sin comisión de manejo
        • Tarjeta débito incluida
        
        Cuenta Corriente:
        • Apertura desde $100,000
        • Comisión: $15,000/mes
        • Chequera incluida
        • Sobregiro disponible
        
        Tarjeta de Crédito:
        • Cupo desde 2x ingresos mensuales
        • Tasa desde 1.9% mensual
        • Programa de puntos
        • Aceptación internacional
        
        Preguntas Frecuentes:
        
        P: ¿Cómo consulto mi saldo?
        R: Por banca online, app móvil, cajeros o llamando al 123-456-7890
        
        P: ¿Qué hago si pierdo mi tarjeta?
        R: Llama inmediatamente al 123-456-7890 para bloquearla
        
        P: ¿Cómo abro una cuenta?
        R: Visita cualquier sucursal con tu documento de identidad y comprobante de ingresos
        """

        from backend.core.knowledge_ingestion import get_ingestion_pipeline
        pipeline = await get_ingestion_pipeline()

        chunks = await pipeline.ingest_text_direct(
            text=sample_content,
            source="informacion_general.txt",
            metadata={
                "category": "general",
                "confidence_level": "high",
                "type": "sample_data"
            }
        )

        print_success(f"Creados {len(chunks)} chunks de conocimiento de ejemplo")

    async def _start_main_api(self):
        """Inicia la API principal."""
        print_step("Iniciando API principal")

        try:
            # Importar la aplicación
            from banking_chatbot.backend.app.api.main import app
            import uvicorn

            print_success("API cargada correctamente")
            print(f"\n{Colors.BOLD}{Colors.GREEN}")
            print("🎉 SISTEMA RAG INICIADO EXITOSAMENTE")
            print("=" * 50)
            print("📖 API Documentation: http://localhost:8000/docs")
            print("❤️  Health Check: http://localhost:8000/health")
            print("💬 Chat Endpoint: http://localhost:8000/v1/chat")
            print("🔍 Search Endpoint: http://localhost:8000/v1/search")
            print("=" * 50)
            print("Presiona Ctrl+C para detener el servidor")
            print(f"{Colors.END}")

            # Configuración del servidor
            config = uvicorn.Config(
                app=app,
                host=os.getenv("HOST", "0.0.0.0"),
                port=int(os.getenv("PORT", 8000)),
                reload=os.getenv("DEBUG", "false").lower() == "true",
                log_level=os.getenv("LOG_LEVEL", "info").lower()
            )

            server = uvicorn.Server(config)
            await server.serve()

        except KeyboardInterrupt:
            print_warning("\n🛑 Servidor detenido por el usuario")
        except Exception as e:
            print_error(f"Error iniciando API: {e}")
            raise

    async def _cleanup_on_error(self):
        """Limpia recursos en caso de error."""
        print_warning("Limpiando recursos...")

        # Aquí podrías agregar lógica para limpiar recursos
        # como cerrar conexiones, detener servicios Docker, etc.

        if self.mode == "docker":
            try:
                subprocess.run([
                    "docker-compose", "-f", "docker-compose.rag.yml", "down"
                ], capture_output=True)
                print_success("Servicios Docker detenidos")
            except:
                pass


async def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description="Inicia el sistema RAG del Banking Chatbot")
    parser.add_argument(
        "--mode",
        choices=["local", "docker", "production"],
        default="local",
        help="Modo de ejecución (default: local)"
    )
    parser.add_argument(
        "--skip-knowledge",
        action="store_true",
        help="Omitir carga de conocimiento inicial"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Puerto para la API (default: 8000)"
    )

    args = parser.parse_args()

    # Configurar variables de entorno desde argumentos
    os.environ["PORT"] = str(args.port)

    try:
        starter = SystemStarter(mode=args.mode)
        await starter.start_system()

    except KeyboardInterrupt:
        print_warning("\n🛑 Arranque interrumpido por el usuario")
    except Exception as e:
        print_error(f"Error durante el arranque: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())