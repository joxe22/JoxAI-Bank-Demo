"""
Database models package.
Import all models here to ensure they are registered with SQLAlchemy.
"""

from app.models.base import BaseModel, TimestampMixin
from app.models.db_user import DBUser, UserRole
from app.models.db_conversation import DBConversation
from app.models.db_message import DBMessage, MessageRole
from app.models.db_ticket import DBTicket, TicketStatus, TicketPriority

__all__ = [
    "BaseModel",
    "TimestampMixin",
    "DBUser",
    "UserRole",
    "DBConversation",
    "DBMessage",
    "MessageRole",
    "DBTicket",
    "TicketStatus",
    "TicketPriority",
]
