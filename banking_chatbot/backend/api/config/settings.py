"""
⚙️ Settings de la Aplicación
Ubicación: backend/api/config/settings.py

Configuración centralizada usando variables de entorno.
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, validator

class Settings(BaseSettings):
    """Configuración de la aplicación"""

    # 🏗️ Configuración básica
    APP_NAME: str = "Banking Chatbot API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # 🌐 Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # 🗄️ Database
    DATABASE_URL: str = "sqlite:///./chatbot.db"
    DATABASE_ECHO: bool = True

    # 🔴 Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # 🔍 Vector DB
    VECTOR_DB_URL: str = "http://localhost:6333"
    VECTOR_COLLECTION_NAME: str = "banking_knowledge"

    # 🤖 LLM
    LLM_PROVIDER: str = "openai"  # openai, anthropic, local
    LLM_MODEL: str = "gpt-3.5-turbo"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 1000

    # 🔐 Seguridad
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # 🌐 CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000"
    ]

    # 📊 Monitoring
    LOG_LEVEL: str = "INFO"
    ENABLE_METRICS: bool = True

    # 🔑 API Keys (serán leídas desde variables de entorno)
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    @validator('CORS_ORIGINS', pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = ".env"
        case_sensitive = True

# Instancia global de configuración
settings = Settings()