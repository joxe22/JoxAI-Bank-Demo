"""
🎫 Tickets Service Module
Ubicación: backend/services/tickets/__init__.py

Sistema de tickets para escalación a agentes humanos.
"""

from .ticket_service import TicketService
from .ticket_manager import TicketManager
from .agent_service import AgentService

__all__ = ["TicketService", "TicketManager", "AgentService"]