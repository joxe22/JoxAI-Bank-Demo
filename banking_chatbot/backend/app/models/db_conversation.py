"""
Conversation model for database storage.
"""

from sqlalchemy import Column, String, Boolean, Text, Integer
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class DBConversation(BaseModel):
    """
    Conversation model representing a chat session.
    """

    __tablename__ = "conversations"

    conversation_id = Column(String(100), unique=True, index=True, nullable=False)
    user_id = Column(String(255), index=True, nullable=False)
    customer_name = Column(String(255), nullable=True)
    customer_email = Column(String(255), nullable=True)
    is_escalated = Column(Boolean, default=False, nullable=False)
    escalation_reason = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    sentiment_score = Column(Integer, default=0, nullable=True)

    messages = relationship("DBMessage", back_populates="conversation", cascade="all, delete-orphan")
    tickets = relationship("DBTicket", back_populates="conversation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<DBConversation(id={self.id}, conversation_id={self.conversation_id}, user_id={self.user_id})>"
