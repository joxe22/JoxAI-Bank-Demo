#!/usr/bin/env python3
"""
🔍 Sistema de Verificación Completa - Banking Chatbot
Ubicación: /verify_system.py

Script para verificar que todos los imports funcionan correctamente
y que el sistema está operativo end-to-end.
"""

import sys
import os
import asyncio
import importlib
from pathlib import Path
from datetime import datetime

# Colores para output
class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_status(message):
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {message}")

def print_success(message):
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {message}")

def print_warning(message):
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {message}")

def print_error(message):
    print(f"{Colors.RED}[ERROR]{Colors.NC} {message}")

def setup_python_path():
    """Configurar PYTHONPATH para imports correctos"""
    current_dir = Path(__file__).parent
    backend_dir = current_dir / "backend"

    # Agregar directorios al path
    paths_to_add = [
        str(current_dir),
        str(backend_dir),
        str(backend_dir / "api"),
        str(backend_dir / "services"),
        str(backend_dir / "utils")
    ]

    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)

    print_success(f"PYTHONPATH configurado con {len(paths_to_add)} directorios")

def test_imports():
    """Verificar que todos los imports críticos funcionan"""
    print_status("🔍 Verificando imports críticos...")

    import_tests = [
        # Core FastAPI
        ("fastapi", "FastAPI core"),
        ("pydantic", "Pydantic models"),
        ("uvicorn", "ASGI server"),

        # Intentar imports del proyecto
        ("api.main", "API main module"),
        ("api.routers.health", "Health router"),
        ("api.routers.chat", "Chat router"),
    ]

    results = []

    for module_name, description in import_tests:
        try:
            module = importlib.import_module(module_name)
            print_success(f"✓ {description}: {module_name}")
            results.append((module_name, True, None))
        except ImportError as e:
            print_error(f"✗ {description}: {module_name} - {str(e)}")
            results.append((module_name, False, str(e)))
        except Exception as e:
            print_warning(f"⚠ {description}: {module_name} - {str(e)}")
            results.append((module_name, False, str(e)))

    return results

def test_optional_imports():
    """Verificar imports opcionales (servicios avanzados)"""
    print_status("🔍 Verificando imports opcionales...")

    optional_imports = [
        ("services.chat.chat_service", "ChatService"),
        ("services.llm.llm_service", "LLM Service"),
        ("services.rag.rag_service", "RAG Service"),
        ("services.tickets.ticket_service", "Ticket Service"),
        ("utils.session_manager", "Session Manager"),
    ]

    results = []

    for module_name, description in optional_imports:
        try:
            module = importlib.import_module(module_name)
            print_success(f"✓ {description}: {module_name}")
            results.append((module_name, True, None))
        except ImportError as e:
            print_warning(f"⚠ {description}: {module_name} - {str(e)}")
            results.append((module_name, False, str(e)))

    return results

async def test_chat_service():
    """Test específico del ChatService"""
    print_status("🤖 Testing ChatService...")

    try:
        from services.chat.chat_service import ChatService

        chat_service = ChatService()

        # Test mensaje básico
        response = await chat_service.process_message(
            message="Hola, ¿cómo estás?",
            session_id="test_verification",
            user_id="test_user"
        )

        required_fields = ["message", "confidence", "confidence_score"]
        missing_fields = [field for field in required_fields if field not in response]

        if missing_fields:
            print_error(f"ChatService respuesta incompleta. Faltan: {missing_fields}")
            return False

        print_success(f"ChatService funcionando - Respuesta: {response['message'][:50]}...")
        return True

    except Exception as e:
        print_error(f"Error testing ChatService: {str(e)}")
        return False

def test_api_structure():
    """Verificar estructura de la API"""
    print_status("🏗️ Verificando estructura de la API...")

    try:
        from api.main import app

        # Verificar que la app se puede crear
        if not app:
            print_error("FastAPI app no se pudo crear")
            return False

        # Verificar rutas básicas
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/api/v1/health", "/api/v1/chat"]

        missing_routes = [route for route in expected_routes if not any(route in r for r in routes)]

        if missing_routes:
            print_warning(f"Rutas faltantes: {missing_routes}")
        else:
            print_success("Todas las rutas básicas están configuradas")

        print_success(f"API app creada exitosamente con {len(routes)} rutas")
        return True

    except Exception as e:
        print_error(f"Error verificando API: {str(e)}")
        return False

def test_file_structure():
    """Verificar que todos los archivos necesarios existen"""
    print_status("📁 Verificando estructura de archivos...")

    required_files = [
        "backend/api/main.py",
        "backend/api/__init__.py",
        "backend/api/routers/__init__.py",
        "backend/api/routers/health.py",
        "backend/api/routers/chat.py",
        "backend/api/models/schemas.py",
        "backend/services/chat/chat_service.py",
        "backend/utils/session_manager.py",
        "backend/requirements.txt",
        ".env.example",
        "README.md"
    ]

    missing_files = []
    existing_files = []

    for file_path in required_files:
        if Path(file_path).exists():
            existing_files.append(file_path)
        else:
            missing_files.append(file_path)

    if missing_files:
        print_error(f"Archivos faltantes: {len(missing_files)}")
        for file in missing_files:
            print_error(f"  ✗ {file}")

    print_success(f"Archivos existentes: {len(existing_files)}/{len(required_files)}")

    return len(missing_files) == 0

async def test_end_to_end():
    """Test end-to-end simulado"""
    print_status("🔄 Ejecutando test end-to-end...")

    try:
        # Test 1: Crear una sesión mock
        session_id = f"test_e2e_{datetime.now().timestamp()}"

        # Test 2: Procesar mensaje
        success = await test_chat_service()
        if not success:
            return False

        # Test 3: Verificar que los servicios están disponibles
        try:
            from services.chat.chat_service import ChatService
            chat_service = ChatService()

            health = await chat_service.get_service_health()
            print_success(f"Health check: {health.get('chat_service', 'unknown')}")

        except Exception as e:
            print_warning(f"Health check falló: {e}")

        print_success("Test end-to-end completado exitosamente")
        return True

    except Exception as e:
        print_error(f"Test end-to-end falló: {str(e)}")
        return False

def generate_report(test_results):
    """Generar reporte de verificación"""
    print("\n" + "="*60)
    print(f"{Colors.BLUE}📋 REPORTE DE VERIFICACIÓN{Colors.NC}")
    print("="*60)

    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results if result[1])

    print(f"📊 Tests ejecutados: {total_tests}")
    print(f"✅ Tests exitosos: {passed_tests}")
    print(f"❌ Tests fallidos: {total_tests - passed_tests}")
    print(f"📈 Porcentaje de éxito: {(passed_tests/total_tests*100):.1f}%")

    if passed_tests == total_tests:
        print(f"\n{Colors.GREEN}🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!{Colors.NC}")
        print("✅ Todos los imports están resueltos")
        print("✅ La API está lista para ejecutar")
        print("✅ Los servicios están operativos")
        return True
    else:
        print(f"\n{Colors.YELLOW}⚠️  SISTEMA PARCIALMENTE FUNCIONAL{Colors.NC}")
        print("🔧 Algunos componentes necesitan atención")

        failed_tests = [test for test in test_results if not test[1]]
        print("\n❌ Tests fallidos:")
        for test_name, success, error in failed_tests:
            print(f"   • {test_name}: {error}")

        return False

async def main():
    """Función principal de verificación"""
    print(f"{Colors.BLUE}🏦 Banking Chatbot - Verificación Completa{Colors.NC}")
    print("="*60)

    # Setup inicial
    setup_python_path()

    # Lista para recopilar resultados
    all_results = []

    # 1. Verificar estructura de archivos
    files_ok = test_file_structure()
    all_results.append(("file_structure", files_ok, None))

    # 2. Verificar imports críticos
    import_results = test_imports()
    all_results.extend(import_results)

    # 3. Verificar imports opcionales
    optional_results = test_optional_imports()
    all_results.extend(optional_results)

    # 4. Verificar estructura API
    api_ok = test_api_structure()
    all_results.append(("api_structure", api_ok, None))

    # 5. Test end-to-end
    e2e_ok = await test_end_to_end()
    all_results.append(("end_to_end", e2e_ok, None))

    # 6. Generar reporte
    system_healthy = generate_report(all_results)

    # 7. Instrucciones finales
    print(f"\n{Colors.BLUE}📋 PRÓXIMOS PASOS:{Colors.NC}")
    if system_healthy:
        print("🚀 Sistema listo para ejecutar:")
        print("   python run_dev.py")
        print("   O usar: make dev")
    else:
        print("🔧 Revisar los errores mostrados arriba")
        print("📚 Consultar README.md para troubleshooting")

    return 0 if system_healthy else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)