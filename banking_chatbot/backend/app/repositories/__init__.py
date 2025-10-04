"""
Repositories package for data access layer.
"""

from app.repositories.base import BaseRepository
from app.repositories.user_repository import UserRepository
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.ticket_repository import TicketRepository
from app.repositories.audit_log_repository import AuditLogRepository
from app.repositories.knowledge_base_repository import KnowledgeBaseRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.setting_repository import SettingRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "ConversationRepository",
    "MessageRepository",
    "TicketRepository",
    "AuditLogRepository",
    "KnowledgeBaseRepository",
    "CustomerRepository",
    "SettingRepository",
]
