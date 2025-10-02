"""
Configuración centralizada del sistema usando Pydantic Settings.
Lee variables de entorno y provee configuración tipada.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional
import secrets


class Settings(BaseSettings):
    """
    Settings principales del sistema.
    Lee automáticamente de .env o variables de entorno.
    """

    # ==================== APPLICATION ====================
    APP_NAME: str = Field(default="Banking ChatBot API")
    APP_VERSION: str = Field(default="1.0.0")
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    API_V1_PREFIX: str = Field(default="/api/v1")

    # ==================== SERVER ====================
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    RELOAD: bool = Field(default=True)

    # ==================== DATABASE ====================
    DATABASE_URL: str = Field(
        default="postgresql://chatbot_user:password@localhost:5432/chatbot_db"
    )
    DATABASE_POOL_SIZE: int = Field(default=10)
    DATABASE_MAX_OVERFLOW: int = Field(default=20)

    # ==================== REDIS ====================
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    REDIS_CACHE_TTL: int = Field(default=3600)  # 1 hora

    # ==================== SECURITY ====================
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)

    # ==================== CORS ====================
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:5173"
    )

    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        """Convierte string separado por comas en lista"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # ==================== LLM - OPENAI ====================
    OPENAI_API_KEY: Optional[str] = Field(default=None)
    OPENAI_MODEL: str = Field(default="gpt-4-turbo-preview")
    OPENAI_TEMPERATURE: float = Field(default=0.7)
    OPENAI_MAX_TOKENS: int = Field(default=1000)

    # ==================== LLM - ANTHROPIC ====================
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None)
    ANTHROPIC_MODEL: str = Field(default="claude-3-sonnet-20240229")

    # ==================== VECTOR DB - QDRANT ====================
    QDRANT_HOST: str = Field(default="localhost")
    QDRANT_PORT: int = Field(default=6333)
    QDRANT_COLLECTION_NAME: str = Field(default="banking_knowledge")
    QDRANT_API_KEY: Optional[str] = Field(default=None)
    QDRANT_VECTOR_SIZE: int = Field(default=1536)  # OpenAI embeddings

    # ==================== NLP ====================
    SPACY_MODEL: str = Field(default="es_core_news_md")

    # ==================== LOGGING ====================
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FORMAT: str = Field(default="json")

    # ==================== SENTRY ====================
    SENTRY_DSN: Optional[str] = Field(default=None)

    # ==================== FILE UPLOAD ====================
    MAX_FILE_SIZE_MB: int = Field(default=10)
    ALLOWED_FILE_TYPES: str = Field(default="pdf,txt,docx,csv")

    @validator("ALLOWED_FILE_TYPES", pre=True)
    def parse_allowed_file_types(cls, v):
        """Convierte string en lista"""
        if isinstance(v, str):
            return [ft.strip() for ft in v.split(",")]
        return v

    # ==================== RATE LIMITING ====================
    RATE_LIMIT_PER_MINUTE: int = Field(default=60)

    # ==================== SESSION ====================
    SESSION_TIMEOUT_MINUTES: int = Field(default=30)

    # ==================== ADMIN DEFAULT ====================
    ADMIN_EMAIL: str = Field(default="admin@banco.com")
    ADMIN_PASSWORD: str = Field(default="admin123")
    ADMIN_NAME: str = Field(default="Admin User")


    # ==================== COMPUTED PROPERTIES ====================

    @property
    def is_production(self) -> bool:
        """Check si estamos en producción"""
        return self.ENVIRONMENT.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check si estamos en desarrollo"""
        return self.ENVIRONMENT.lower() == "development"

    @property
    def max_file_size_bytes(self) -> int:
        """Tamaño máximo de archivo en bytes"""
        return self.MAX_FILE_SIZE_MB * 1024 * 1024


    class Config:
        """Configuración de Pydantic"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# ==================== INSTANCIA GLOBAL ====================

settings = Settings()


# ==================== HELPERS ====================

def get_database_url() -> str:
    """Retorna la URL de la base de datos"""
    return settings.DATABASE_URL


def get_redis_url() -> str:
    """Retorna la URL de Redis"""
    return settings.REDIS_URL


def is_openai_configured() -> bool:
    """Check si OpenAI está configurado"""
    return settings.OPENAI_API_KEY is not None


def is_anthropic_configured() -> bool:
    """Check si Anthropic está configurado"""
    return settings.ANTHROPIC_API_KEY is not None


def get_cors_origins() -> List[str]:
    """Retorna lista de orígenes CORS permitidos"""
    if isinstance(settings.CORS_ORIGINS, str):
        return [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]
    return settings.CORS_ORIGINS