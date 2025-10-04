"""
Message model for database storage.
"""

from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class MessageRole(str, enum.Enum):
    """Message role types"""

    USER = "USER"
    ASSISTANT = "ASSISTANT"
    SYSTEM = "SYSTEM"


class DBMessage(BaseModel):
    """
    Message model representing a single message in a conversation.
    """

    __tablename__ = "messages"

    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(SQLEnum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)
    message_metadata = Column(Text, nullable=True)
    is_internal = Column(Boolean, default=False, nullable=False)

    conversation = relationship("DBConversation", back_populates="messages")

    def __repr__(self):
        return f"<DBMessage(id={self.id}, conversation_id={self.conversation_id}, role={self.role})>"
