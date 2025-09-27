"""
🗂️ Session Manager
Ubicación: backend/utils/session_manager.py

Maneja las sesiones de chat, historial de conversaciones y estado de usuario.
En producción usará Redis para persistencia.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import uuid
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    """
    🗂️ Manejador de sesiones de chat

    Responsabilidades:
    - Crear y gestionar sesiones
    - Almacenar historial de conversaciones
    - Manejar timeouts de sesión
    - Guardar feedback del usuario
    """

    def __init__(self):
        # Por ahora usamos memoria. En producción usaremos Redis
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.session_timeout = timedelta(hours=2)  # 2 horas de inactividad

    async def get_or_create_session(self, session_id: str) -> Dict[str, Any]:
        """
        📋 Obtener sesión existente o crear nueva
        """

        if session_id not in self.sessions:
            # Crear nueva sesión
            self.sessions[session_id] = {
                "id": session_id,
                "created_at": datetime.now(),
                "last_activity": datetime.now(),
                "messages": [],
                "user_id": None,
                "authenticated": False,
                "metadata": {},
                "feedback": None
            }
            logger.info(f"📋 Nueva sesión creada: {session_id}")
        else:
            # Actualizar última actividad
            self.sessions[session_id]["last_activity"] = datetime.now()

        return self.sessions[session_id]

    async def add_message(
            self,
            session_id: str,
            role: str,
            content: str,
            user_id: Optional[str] = None,
            metadata: Optional[Dict[str, Any]] = None
    ):
        """
        💬 Agregar mensaje al historial de la sesión
        """

        session = await self.get_or_create_session(session_id)

        message = {
            "id": str(uuid.uuid4()),
            "role": role,  # "user" | "assistant" | "system"
            "content": content,
            "timestamp": datetime.now(),
            "user_id": user_id,
            "metadata": metadata or {}
        }

        session["messages"].append(message)

        # Actualizar user_id en sesión si se proporciona
        if user_id and not session["user_id"]:
            session["user_id"] = user_id

        logger.info(f"💬 Mensaje agregado - Session: {session_id}, Role: {role}")

    async def get_session_history(
            self,
            session_id: str,
            limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        📚 Obtener historial de conversación
        """

        if session_id not in self.sessions:
            return []

        messages = self.sessions[session_id]["messages"]

        # Retornar los últimos 'limit' mensajes
        return messages[-limit:] if len(messages) > limit else messages

    async def clear_session(self, session_id: str):
        """
        🗑️ Limpiar sesión (nueva conversación)
        """

        if session_id in self.sessions:
            # Mantener info básica pero limpiar mensajes
            session = self.sessions[session_id]
            session["messages"] = []
            session["last_activity"] = datetime.now()
            session["authenticated"] = False
            session["metadata"] = {}

            logger.info(f"🗑️ Sesión limpiada: {session_id}")

    async def authenticate_session(
            self,
            session_id: str,
            user_id: str,
            permissions: List[str] = None
    ):
        """
        🔐 Autenticar sesión para operaciones bancarias
        """

        session = await self.get_or_create_session(session_id)
        session["authenticated"] = True
        session["user_id"] = user_id
        session["permissions"] = permissions or []
        session["auth_timestamp"] = datetime.now()

        logger.info(f"🔐 Sesión autenticada: {session_id} - Usuario: {user_id}")

    async def is_authenticated(self, session_id: str) -> bool:
        """
        ✅ Verificar si sesión está autenticada
        """

        if session_id not in self.sessions:
            return False

        session = self.sessions[session_id]

        if not session.get("authenticated", False):
            return False

        # Verificar timeout de autenticación (15 minutos)
        auth_time = session.get("auth_timestamp")
        if auth_time and datetime.now() - auth_time > timedelta(minutes=15):
            session["authenticated"] = False
            return False

        return True

    async def save_feedback(
            self,
            session_id: str,
            rating: int,
            comment: Optional[str] = None
    ):
        """
        ⭐ Guardar feedback del usuario
        """

        session = await self.get_or_create_session(session_id)
        session["feedback"] = {
            "rating": rating,
            "comment": comment,
            "timestamp": datetime.now()
        }

        logger.info(f"⭐ Feedback guardado - Session: {session_id}, Rating: {rating}")

    async def cleanup_expired_sessions(self):
        """
        🧹 Limpiar sesiones expiradas

        Debe ejecutarse periódicamente para liberar memoria.
        """

        now = datetime.now()
        expired_sessions = []

        for session_id, session in self.sessions.items():
            last_activity = session["last_activity"]
            if now - last_activity > self.session_timeout:
                expired_sessions.append(session_id)

        for session_id in expired_sessions:
            del self.sessions[session_id]
            logger.info(f"🧹 Sesión expirada eliminada: {session_id}")

        if expired_sessions:
            logger.info(f"🧹 {len(expired_sessions)} sesiones expiradas eliminadas")

    async def get_session_stats(self) -> Dict[str, Any]:
        """
        📊 Obtener estadísticas de sesiones
        """

        now = datetime.now()
        active_sessions = 0
        total_messages = 0
        authenticated_sessions = 0

        for session in self.sessions.values():
            # Sesiones activas (última actividad < 30 minutos)
            if now - session["last_activity"] < timedelta(minutes=30):
                active_sessions += 1

            total_messages += len(session["messages"])

            if session.get("authenticated", False):
                authenticated_sessions += 1

        return {
            "total_sessions": len(self.sessions),
            "active_sessions": active_sessions,
            "authenticated_sessions": authenticated_sessions,
            "total_messages": total_messages,
            "avg_messages_per_session": (
                total_messages / len(self.sessions)
                if self.sessions else 0
            )
        }