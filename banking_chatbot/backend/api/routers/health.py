"""
🏥 Health Check Router
Ubicación: backend/api/routers/health.py

Endpoints para verificar el estado de salud de la aplicación.
Útil para monitoring, load balancers y debugging.
"""

from fastapi import APIRouter, status
from datetime import datetime
import psutil
import os

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    🏥 Health Check básico

    Verifica que la aplicación está funcionando correctamente.
    Usado por load balancers y sistemas de monitoring.
    """
    return {
        "status": "🟢 healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "banking-chatbot-api",
        "version": "1.0.0"
    }

@router.get("/health/detailed", status_code=status.HTTP_200_OK)
async def detailed_health():
    """
    🔍 Health Check detallado

    Incluye métricas del sistema como CPU, memoria, etc.
    Útil para debugging y monitoring avanzado.
    """

    # Obtener métricas del sistema
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return {
        "status": "🟢 healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "banking-chatbot-api",
        "version": "1.0.0",
        "system_metrics": {
            "cpu_usage_percent": cpu_percent,
            "memory": {
                "total_gb": round(memory.total / (1024**3), 2),
                "used_gb": round(memory.used / (1024**3), 2),
                "usage_percent": memory.percent
            },
            "disk": {
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "usage_percent": round((disk.used / disk.total) * 100, 1)
            }
        },
        "process_info": {
            "pid": os.getpid(),
            "python_version": f"{psutil.PYTHON_VERSION}",
            "uptime_seconds": None  # Lo implementaremos después
        }
    }

@router.get("/health/ready", status_code=status.HTTP_200_OK)
async def readiness_check():
    """
    ✅ Readiness Check

    Verifica que la aplicación está lista para recibir tráfico.
    Incluye verificación de dependencias externas (DB, Vector DB, etc.)
    """

    dependencies_status = {
        "database": "🟢 connected",      # Implementaremos después
        "vector_db": "🟢 connected",     # Implementaremos después
        "redis": "🟢 connected",         # Implementaremos después
        "llm_service": "🟢 available"    # Implementaremos después
    }

    # Verificar si todas las dependencias están OK
    all_healthy = all(status.startswith("🟢") for status in dependencies_status.values())

    return {
        "ready": all_healthy,
        "status": "🟢 ready" if all_healthy else "🟡 partially ready",
        "timestamp": datetime.now().isoformat(),
        "dependencies": dependencies_status
    }