#!/usr/bin/env python3
"""
🔧 Troubleshooting Tool - Banking Chatbot
Ubicación: /troubleshoot.py

Herramienta de diagnóstico para identificar y solucionar
problemas comunes de imports, configuración y dependencias.
"""

import sys
import os
import importlib
import subprocess
from pathlib import Path
from datetime import datetime

class Troubleshooter:
    def __init__(self):
        self.issues_found = []
        self.fixes_applied = []

    def log_issue(self, issue, severity="warning"):
        self.issues_found.append({"issue": issue, "severity": severity, "time": datetime.now()})

    def log_fix(self, fix):
        self.fixes_applied.append({"fix": fix, "time": datetime.now()})

    def print_header(self):
        print("""
🔧 BANKING CHATBOT TROUBLESHOOTER
==================================
Diagnosticando problemas comunes...
""")

    def check_python_version(self):
        """Verificar versión de Python"""
        print("1️⃣ Verificando Python...")

        version = sys.version_info
        if version.major < 3:
            self.log_issue("Python 2 detectado - Se requiere Python 3", "critical")
            print("❌ Python 2 no es compatible")
            return False
        elif version.minor < 9:
            self.log_issue(f"Python 3.{version.minor} - Se recomienda Python 3.9+", "warning")
            print(f"⚠️ Python 3.{version.minor} (se recomienda 3.9+)")
        else:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro}")

        return True

    def check_file_structure(self):
        """Verificar estructura de archivos"""
        print("\n2️⃣ Verificando estructura de archivos...")

        critical_files = [
            "backend/api/main.py",
            "backend/api/routers/chat.py",
            "backend/api/routers/health.py",
            "backend/requirements.txt"
        ]

        missing_files = []
        for file_path in critical_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
                self.log_issue(f"Archivo faltante: {file_path}", "critical")

        if missing_files:
            print(f"❌ {len(missing_files)} archivos críticos faltantes:")
            for file in missing_files:
                print(f"   • {file}")
            return False

        print("✅ Estructura de archivos correcta")
        return True

    def check_init_files(self):
        """Verificar archivos __init__.py"""
        print("\n3️⃣ Verificando archivos __init__.py...")

        init_files = [
            "backend/__init__.py",
            "backend/api/__init__.py",
            "backend/api/routers/__init__.py",
            "backend/api/models/__init__.py",
            "backend/services/__init__.py",
            "backend/services/chat/__init__.py",
            "backend/utils/__init__.py"
        ]

        missing_inits = []
        for init_file in init_files:
            if not Path(init_file).exists():
                missing_inits.append(init_file)

        if missing_inits:
            print(f"⚠️ {len(missing_inits)} archivos __init__.py faltantes")
            self.log_issue("Archivos __init__.py faltantes", "warning")

            # Intentar crearlos
            created = self.fix_init_files(missing_inits)
            if created:
                print(f"✅ {created} archivos __init__.py creados automáticamente")
                self.log_fix(f"Creados {created} archivos __init__.py")
        else:
            print("✅ Todos los __init__.py están presentes")

        return True

    def fix_init_files(self, missing_files):
        """Crear archivos __init__.py faltantes"""
        created = 0

        for init_file in missing_files:
            try:
                path = Path(init_file)
                path.parent.mkdir(parents=True, exist_ok=True)

                # Contenido básico según el directorio
                if "services" in init_file:
                    content = '"""Services module"""\n'
                elif "api" in init_file:
                    content = '"""API module"""\n'
                elif "utils" in init_file:
                    content = '"""Utils module"""\n'
                else:
                    content = "# Auto-generated __init__.py\n"

                path.write_text(content)
                created += 1

            except Exception as e:
                print(f"❌ Error creando {init_file}: {e}")

        return created

    def check_dependencies(self):
        """Verificar dependencias instaladas"""
        print("\n4️⃣ Verificando dependencias...")

        required_packages = {
            "fastapi": "FastAPI framework",
            "uvicorn": "ASGI server",
            "pydantic": "Data validation",
            "python-multipart": "Form data support",
            "python-dotenv": "Environment variables"
        }

        missing_packages = []
        installed_packages = []

        for package, description in required_packages.items():
            try:
                importlib.import_module(package.replace("-", "_"))
                installed_packages.append(package)
                print(f"✅ {package} ({description})")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package} ({description})")
                self.log_issue(f"Paquete faltante: {package}", "critical")

        if missing_packages:
            print(f"\n💡 Para instalar paquetes faltantes:")
            print("   pip install " + " ".join(missing_packages))
            return False

        print(f"✅ Todas las dependencias instaladas ({len(installed_packages)})")
        return True

    def check_imports(self):
        """Verificar imports del proyecto"""
        print("\n5️⃣ Verificando imports del proyecto...")

        # Configurar PYTHONPATH
        current_dir = Path.cwd()
        backend_dir = current_dir / "backend"

        paths_to_add = [str(current_dir), str(backend_dir)]
        for path in paths_to_add:
            if path not in sys.path:
                sys.path.insert(0, path)

        import_tests = [
            ("api.main", "FastAPI main app", "critical"),
            ("api.routers.health", "Health router", "critical"),
            ("api.routers.chat", "Chat router", "critical"),
            ("api.models.schemas", "Pydantic schemas", "warning"),
            ("services.chat.chat_service", "Chat services", "warning"),
            ("utils.session_manager", "Session manager", "warning")
        ]

        failed_imports = []
        successful_imports = []

        for module_name, description, severity in import_tests:
            try:
                importlib.import_module(module_name)
                successful_imports.append(module_name)
                print(f"✅ {description}")
            except ImportError as e:
                failed_imports.append((module_name, description, str(e)))
                print(f"❌ {description}: {str(e)[:60]}...")
                self.log_issue(f"Import falló: {module_name}", severity)

        if failed_imports:
            print(f"\n⚠️ {len(failed_imports)} imports fallaron")
            self.suggest_import_fixes(failed_imports)
            return len(failed_imports) < 3  # Tolerar algunos fallos

        print(f"✅ Todos los imports funcionan ({len(successful_imports)})")
        return True

    def suggest_import_fixes(self, failed_imports):
        """Sugerir soluciones para imports fallidos"""
        print("\n💡 Posibles soluciones:")

        for module_name, description, error in failed_imports:
            print(f"\n📌 {description} ({module_name}):")

            if "No module named" in error:
                print("   • Verificar que el archivo existe")
                print("   • Verificar que __init__.py está presente")
                print("   • Verificar PYTHONPATH")
            elif "relative import" in error:
                print("   • Usar imports absolutos en lugar de relativos")
                print("   • Ejecutar desde directorio correcto")
            elif "circular import" in error:
                print("   • Mover imports dentro de funciones")
                print("   • Reestructurar dependencias")
            else:
                print("   • Revisar sintaxis del módulo")
                print("   • Verificar dependencias del módulo")

    def check_environment_variables(self):
        """Verificar variables de entorno"""
        print("\n6️⃣ Verificando variables de entorno...")

        recommended_vars = {
            "PYTHONPATH": "Path de Python para imports",
            "DEBUG": "Modo debug",
            "LOG_LEVEL": "Nivel de logging"
        }

        env_issues = []

        for var, description in recommended_vars.items():
            value = os.environ.get(var)
            if value:
                print(f"✅ {var}={value[:50]}..." if len(value) > 50 else f"✅ {var}={value}")
            else:
                print(f"⚠️ {var} no configurada ({description})")
                env_issues.append(var)

        if env_issues:
            self.log_issue(f"Variables de entorno faltantes: {env_issues}", "warning")
            print("\n💡 Para configurar:")
            print("   export PYTHONPATH=$(pwd):$(pwd)/backend")
            print("   export DEBUG=True")
            print("   export LOG_LEVEL=INFO")

        return True

    def check_ports(self):
        """Verificar puertos disponibles"""
        print("\n7️⃣ Verificando puertos...")

        try:
            import socket

            ports_to_check = [8000, 3000, 6333, 5432, 6379]

            for port in ports_to_check:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', port))
                sock.close()

                if result == 0:
                    print(f"⚠️ Puerto {port} en uso")
                    self.log_issue(f"Puerto {port} ocupado", "warning")
                else:
                    print(f"✅ Puerto {port} disponible")

        except Exception as e:
            print(f"⚠️ Error verificando puertos: {e}")

        return True

    def test_basic_server(self):
        """Test básico del servidor"""
        print("\n8️⃣ Test básico del servidor...")

        try:
            # Intentar importar la app
            sys.path.insert(0, str(Path.cwd() / "backend"))
            from api.main import app

            print("✅ FastAPI app puede ser importada")

            # Verificar rutas básicas
            routes = [route.path for route in app.routes]
            expected_routes = ["/api/v1/health", "/api/v1/chat"]

            missing_routes = []
            for expected in expected_routes:
                if not any(expected in route for route in routes):
                    missing_routes.append(expected)

            if missing_routes:
                print(f"⚠️ Rutas faltantes: {missing_routes}")
                self.log_issue(f"Rutas faltantes: {missing_routes}", "warning")
            else:
                print("✅ Rutas básicas configuradas")

            return True

        except Exception as e:
            print(f"❌ Error con servidor: {str(e)[:60]}...")
            self.log_issue(f"Error del servidor: {str(e)}", "critical")
            return False

    def generate_report(self):
        """Generar reporte de diagnóstico"""
        print("\n" + "="*60)
        print("📋 REPORTE DE DIAGNÓSTICO")
        print("="*60)

        critical_issues = [i for i in self.issues_found if i["severity"] == "critical"]
        warning_issues = [i for i in self.issues_found if i["severity"] == "warning"]

        print(f"🔍 Issues encontrados: {len(self.issues_found)}")
        print(f"🔥 Críticos: {len(critical_issues)}")
        print(f"⚠️ Advertencias: {len(warning_issues)}")
        print(f"🔧 Fixes aplicados: {len(self.fixes_applied)}")

        if critical_issues:
            print("\n🚨 ISSUES CRÍTICOS:")
            for issue in critical_issues:
                print(f"   • {issue['issue']}")

        if warning_issues:
            print("\n⚠️ ADVERTENCIAS:")
            for issue in warning_issues[:5]:  # Mostrar solo las primeras 5
                print(f"   • {issue['issue']}")

            if len(warning_issues) > 5:
                print(f"   ... y {len(warning_issues) - 5} más")

        if self.fixes_applied:
            print("\n✅ FIXES APLICADOS:")
            for fix in self.fixes_applied:
                print(f"   • {fix['fix']}")

        # Recomendaciones finales
        print("\n💡 RECOMENDACIONES:")

        if len(critical_issues) > 0:
            print("   🔥 Resolver issues críticos antes de continuar")
            print("   📚 Consultar README.md para setup completo")
        elif len(warning_issues) > 3:
            print("   ⚠️ Revisar advertencias para mejor funcionamiento")
            print("   🔧 Ejecutar: python run_dev_fixed.py para inicio robusto")
        else:
            print("   🚀 Sistema listo para ejecutar")
            print("   ✅ Ejecutar: python run_dev.py")

        return len(critical_issues) == 0

    def run_full_diagnosis(self):
        """Ejecutar diagnóstico completo"""
        self.print_header()

        # Ejecutar todas las verificaciones
        checks = [
            self.check_python_version,
            self.check_file_structure,
            self.check_init_files,
            self.check_dependencies,
            self.check_imports,
            self.check_environment_variables,
            self.check_ports,
            self.test_basic_server
        ]

        results = []

        for check in checks:
            try:
                result = check()
                results.append(result)
            except Exception as e:
                print(f"❌ Error en verificación: {e}")
                self.log_issue(f"Error en verificación: {str(e)}", "critical")
                results.append(False)

        # Generar reporte final
        system_healthy = self.generate_report()

        return system_healthy

def main():
    """Función principal"""
    troubleshooter = Troubleshooter()

    try:
        system_healthy = troubleshooter.run_full_diagnosis()

        print("\n" + "="*60)
        if system_healthy:
            print("🎉 SISTEMA SALUDABLE - Listo para ejecutar")
            print("\n🚀 Comandos recomendados:")
            print("   python run_dev.py")
            print("   O: python run_dev_fixed.py (más robusto)")
            return 0
        else:
            print("⚠️ SISTEMA CON ISSUES - Revisar reporte arriba")
            print("\n🔧 Comandos de emergencia:")
            print("   python run_dev_fixed.py (intenta funcionar a pesar de errores)")
            print("   python verify_system.py (diagnóstico más profundo)")
            return 1

    except KeyboardInterrupt:
        print("\n\n🛑 Diagnóstico interrumpido")
        return 1
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())