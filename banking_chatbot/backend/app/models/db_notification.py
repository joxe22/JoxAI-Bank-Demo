from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from enum import Enum

from app.models.base import BaseModel


class NotificationType(str, Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH"


class NotificationStatus(str, Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"
    BOUNCED = "BOUNCED"


class NotificationCategory(str, Enum):
    TICKET_ASSIGNED = "TICKET_ASSIGNED"
    TICKET_STATUS_CHANGED = "TICKET_STATUS_CHANGED"
    TICKET_ESCALATED = "TICKET_ESCALATED"
    TICKET_RESOLVED = "TICKET_RESOLVED"
    NEW_MESSAGE = "NEW_MESSAGE"
    SYSTEM_ALERT = "SYSTEM_ALERT"


class Notification(BaseModel):
    """
    Notification model for tracking all sent notifications (email, SMS, push).
    Maintains delivery status and history for auditing.
    """
    __tablename__ = "notifications"
    
    # Recipient info
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    recipient_email = Column(String(255), nullable=True)
    recipient_phone = Column(String(50), nullable=True)
    
    # Notification details
    notification_type = Column(SQLEnum(NotificationType), nullable=False, index=True)
    category = Column(SQLEnum(NotificationCategory), nullable=False, index=True)
    status = Column(SQLEnum(NotificationStatus), default=NotificationStatus.PENDING, nullable=False, index=True)
    
    # Content
    subject = Column(String(500), nullable=True)
    body = Column(Text, nullable=False)
    html_body = Column(Text, nullable=True)
    
    # Related resources
    resource_type = Column(String(100), nullable=True)  # TICKET, CONVERSATION, USER
    resource_id = Column(String(100), nullable=True, index=True)
    
    # Delivery tracking
    sent_at = Column(Integer, nullable=True)  # Unix timestamp
    delivery_attempts = Column(Integer, default=0, nullable=False)
    last_attempt_at = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Additional data
    extra_data = Column(JSON, nullable=True)
    
    # Relationships
    user = relationship("DBUser", back_populates="notifications", foreign_keys=[user_id])
    
    def __repr__(self):
        return f"<Notification(id={self.id}, type={self.notification_type}, category={self.category}, status={self.status})>"
