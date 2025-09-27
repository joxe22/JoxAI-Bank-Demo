"""
📋 Banking Chatbot - Pydantic Schemas
Ubicación: backend/api/models/schemas.py

Define los modelos de datos para requests y responses.
Estos esquemas validan automáticamente los datos de entrada y salida.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# 🎯 Enums para tipos específicos
class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatAction(str, Enum):
    SEND_MESSAGE = "send_message"
    CHECK_BALANCE = "check_balance"
    VIEW_TRANSACTIONS = "view_transactions"
    CREATE_TICKET = "create_ticket"
    TRANSFER_AGENT = "transfer_agent"

class ConfidenceLevel(str, Enum):
    HIGH = "high"      # > 0.8
    MEDIUM = "medium"  # 0.5 - 0.8
    LOW = "low"        # < 0.5

# 💬 Modelos para Chat
class ChatMessage(BaseModel):
    """Mensaje individual en la conversación"""
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = None

class ChatRequest(BaseModel):
    """Request para enviar mensaje al chatbot"""
    session_id: str = Field(..., description="ID único de la sesión")
    message: str = Field(..., min_length=1, max_length=1000, description="Mensaje del usuario")
    user_id: Optional[str] = Field(None, description="ID del usuario (si está autenticado)")
    context: Optional[Dict[str, Any]] = Field(None, description="Contexto adicional")

    @validator('message')
    def message_not_empty(cls, v):
        if not v.strip():
            raise ValueError('El mensaje no puede estar vacío')
        return v.strip()

class Source(BaseModel):
    """Fuente de información para la respuesta"""
    title: str
    content: str
    url: Optional[str] = None
    confidence: float = Field(..., ge=0.0, le=1.0)
    document_type: Optional[str] = None

class ChatResponse(BaseModel):
    """Response del chatbot"""
    session_id: str
    message: str
    confidence: ConfidenceLevel
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    sources: List[Source] = []
    suggested_actions: List[ChatAction] = []
    requires_auth: bool = False
    escalate_to_human: bool = False
    metadata: Optional[Dict[str, Any]] = None
    response_time_ms: Optional[int] = None

# 🔐 Modelos para Autenticación
class AuthRequest(BaseModel):
    """Request para autenticación"""
    document_id: str = Field(..., description="Número de documento")
    phone_last_digits: str = Field(..., description="Últimos 4 dígitos del teléfono")
    session_id: str

class AuthResponse(BaseModel):
    """Response de autenticación"""
    authenticated: bool
    user_id: Optional[str] = None
    permissions: List[str] = []
    expires_at: Optional[datetime] = None

# 📊 Modelos para Analytics
class SessionStats(BaseModel):
    """Estadísticas de sesión"""
    session_id: str
    total_messages: int
    start_time: datetime
    last_activity: datetime
    user_satisfaction: Optional[float] = None
    resolved: bool = False
    escalated: bool = False

class ChatAnalytics(BaseModel):
    """Analytics del chat en tiempo real"""
    active_sessions: int
    total_messages_today: int
    avg_response_time: float
    satisfaction_score: float
    resolution_rate: float
    top_intents: List[Dict[str, Any]]

# 🎫 Modelos para Tickets
class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class CreateTicketRequest(BaseModel):
    """Request para crear ticket"""
    session_id: str
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10, max_length=1000)
    priority: TicketPriority = TicketPriority.MEDIUM
    category: str
    user_id: Optional[str] = None

class TicketResponse(BaseModel):
    """Response de ticket creado"""
    ticket_id: str
    status: str
    estimated_response_time: str
    agent_assigned: Optional[str] = None

# ✅ Modelo genérico de respuesta exitosa
class SuccessResponse(BaseModel):
    """Respuesta genérica exitosa"""
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)

# ❌ Modelo de error
class ErrorResponse(BaseModel):
    """Respuesta de error"""
    success: bool = False
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)