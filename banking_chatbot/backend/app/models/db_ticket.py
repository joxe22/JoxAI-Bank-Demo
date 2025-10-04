"""
Ticket model for database storage.
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class TicketStatus(str, enum.Enum):
    """Ticket status types"""

    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class TicketPriority(str, enum.Enum):
    """Ticket priority types"""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class DBTicket(BaseModel):
    """
    Ticket model for customer support escalations.
    """

    __tablename__ = "tickets"

    ticket_id = Column(String(50), unique=True, index=True, nullable=False)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    customer_id = Column(String(255), nullable=False, index=True)
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=True)
    subject = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(SQLEnum(TicketStatus), default=TicketStatus.OPEN, nullable=False, index=True)
    priority = Column(SQLEnum(TicketPriority), default=TicketPriority.MEDIUM, nullable=False, index=True)
    category = Column(String(100), nullable=True, index=True)
    agent_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    assigned_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    assigned_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    resolution_notes = Column(Text, nullable=True)

    conversation = relationship("DBConversation", back_populates="ticket")
    agent = relationship("DBUser", back_populates="tickets", foreign_keys=[agent_id])
    assigned_by_user = relationship("DBUser", back_populates="assigned_tickets", foreign_keys=[assigned_by])

    def __repr__(self):
        return f"<DBTicket(id={self.id}, ticket_id={self.ticket_id}, status={self.status})>"
