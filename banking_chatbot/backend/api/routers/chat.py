"""
💬 Chat Router
Ubicación: backend/api/routers/chat.py

Endpoints principales para la funcionalidad del chatbot.
Maneja conversaciones, autenticación y escalación a humanos.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, List
import uuid
from datetime import datetime
import logging

# Importar modelos y servicios
from ..models.schemas import (
    ChatRequest, ChatResponse, ChatAnalytics,
    Source, ConfidenceLevel, ChatAction
)
from ...services.chat.chat_service import ChatService
from ...utils.session_manager import SessionManager

# Configurar logging
logger = logging.getLogger(__name__)

# Crear router
router = APIRouter()

# Instancias de servicios (en producción usaremos dependency injection)
chat_service = ChatService()
session_manager = SessionManager()

@router.post("/chat", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """
    💬 Endpoint principal del chatbot

    Procesa mensajes del usuario y retorna respuestas del chatbot.
    Incluye RAG, NLU, y manejo de contexto conversacional.
    """

    try:
        start_time = datetime.now()

        logger.info(f"💬 Nueva conversación - Session: {request.session_id}")
        logger.info(f"📝 Mensaje: {request.message[:50]}...")

        # 1. Validar y obtener sesión
        session = await session_manager.get_or_create_session(request.session_id)

        # 2. Agregar mensaje del usuario al historial
        await session_manager.add_message(
            session_id=request.session_id,
            role="user",
            content=request.message,
            user_id=request.user_id
        )

        # 3. Procesar mensaje con el ChatService
        response_data = await chat_service.process_message(
            message=request.message,
            session_id=request.session_id,
            user_id=request.user_id,
            context=request.context
        )

        # 4. Calcular tiempo de respuesta
        response_time = (datetime.now() - start_time).total_seconds() * 1000

        # 5. Crear respuesta
        response = ChatResponse(
            session_id=request.session_id,
            message=response_data["message"],
            confidence=response_data["confidence"],
            confidence_score=response_data["confidence_score"],
            sources=response_data.get("sources", []),
            suggested_actions=response_data.get("suggested_actions", []),
            requires_auth=response_data.get("requires_auth", False),
            escalate_to_human=response_data.get("escalate_to_human", False),
            response_time_ms=int(response_time),
            metadata=response_data.get("metadata")
        )

        # 6. Agregar respuesta al historial
        await session_manager.add_message(
            session_id=request.session_id,
            role="assistant",
            content=response.message
        )

        logger.info(f"✅ Respuesta generada - Tiempo: {response_time:.0f}ms")

        return response

    except Exception as e:
        logger.error(f"❌ Error procesando chat: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando mensaje: {str(e)}"
        )

@router.get("/chat/session/{session_id}/history")
async def get_chat_history(session_id: str, limit: int = 50):
    """
    📚 Obtener historial de conversación

    Retorna los últimos mensajes de una sesión específica.
    Útil para cargar contexto cuando el usuario regresa.
    """

    try:
        history = await session_manager.get_session_history(session_id, limit)

        return {
            "session_id": session_id,
            "message_count": len(history),
            "messages": history,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"❌ Error obteniendo historial: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error obteniendo historial"
        )

@router.get("/chat/analytics", response_model=ChatAnalytics)
async def get_chat_analytics():
    """
    📊 Obtener analytics del chatbot en tiempo real

    Métricas para el dashboard administrativo:
    - Sesiones activas
    - Mensajes del día
    - Tiempo promedio de respuesta
    - Score de satisfacción
    """

    try:
        analytics = await chat_service.get_analytics()

        return ChatAnalytics(
            active_sessions=analytics.get("active_sessions", 0),
            total_messages_today=analytics.get("total_messages_today", 0),
            avg_response_time=analytics.get("avg_response_time", 0.0),
            satisfaction_score=analytics.get("satisfaction_score", 0.0),
            resolution_rate=analytics.get("resolution_rate", 0.0),
            top_intents=analytics.get("top_intents", [])
        )

    except Exception as e:
        logger.error(f"❌ Error obteniendo analytics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error obteniendo analytics"
        )

@router.post("/chat/session/{session_id}/feedback")
async def submit_feedback(session_id: str, rating: int, comment: str = None):
    """
    ⭐ Enviar feedback de satisfacción

    Permite al usuario calificar la interacción con el chatbot.
    Usado para métricas CSAT y mejora continua.
    """

    if rating < 1 or rating > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El rating debe estar entre 1 y 5"
        )

    try:
        await session_manager.save_feedback(session_id, rating, comment)

        return {
            "success": True,
            "message": "¡Gracias por tu feedback!",
            "session_id": session_id,
            "rating": rating
        }

    except Exception as e:
        logger.error(f"❌ Error guardando feedback: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error guardando feedback"
        )

@router.delete("/chat/session/{session_id}")
async def clear_session(session_id: str):
    """
    🗑️ Limpiar sesión de chat

    Elimina el historial de conversación y datos de sesión.
    Útil para "empezar nueva conversación".
    """

    try:
        await session_manager.clear_session(session_id)

        return {
            "success": True,
            "message": "Sesión limpiada exitosamente",
            "session_id": session_id
        }

    except Exception as e:
        logger.error(f"❌ Error limpiando sesión: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error limpiando sesión"
        )