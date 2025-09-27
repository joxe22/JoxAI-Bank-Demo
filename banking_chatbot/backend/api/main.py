"""
🏦 Banking Chatbot API - Main Application
Ubicación: backend/api/main.py

Este archivo es el punto de entrada principal de nuestra API.
Configura FastAPI, middlewares, CORS y rutas principales.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging
from datetime import datetime

# Importar routers (los crearemos después)
from .routers import chat, health

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="🏦 Banking Chatbot API",
    description="API para chatbot bancario con LLM/RAG",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# 🌐 Configurar CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:8080",  # Widget local
        "https://yourdomain.com"   # Producción
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📊 Middleware para logging de requests
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()

    logger.info(
        f"🔍 {request.method} {request.url} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    return response

# 🛣️ Incluir routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])

# 📁 Servir archivos estáticos (si necesario)
# app.mount("/static", StaticFiles(directory="static"), name="static")

# 🏠 Ruta raíz
@app.get("/")
async def root():
    return {
        "message": "🏦 Banking Chatbot API",
        "version": "1.0.0",
        "status": "🟢 Online",
        "docs": "/docs",
        "timestamp": datetime.now().isoformat()
    }

# 🚀 Función para ejecutar el servidor
def run_server():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Solo en desarrollo
        log_level="info"
    )

if __name__ == "__main__":
    run_server()