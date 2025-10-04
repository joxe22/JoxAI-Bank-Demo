"""
User model for database storage.
"""

from sqlalchemy import Column, String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class UserRole(str, enum.Enum):
    """User roles in the system"""

    ADMIN = "ADMIN"
    SUPERVISOR = "SUPERVISOR"
    AGENT = "AGENT"


class DBUser(BaseModel):
    """
    User model for authentication and authorization.
    Replaces hardcoded users in DataStore.
    """

    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.AGENT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_online = Column(Boolean, default=False, nullable=False)

    tickets = relationship("DBTicket", back_populates="agent", foreign_keys="DBTicket.agent_id")
    assigned_tickets = relationship("DBTicket", back_populates="assigned_by_user", foreign_keys="DBTicket.assigned_by")
    notifications = relationship("Notification", back_populates="user", foreign_keys="Notification.user_id")

    def __repr__(self):
        return f"<DBUser(id={self.id}, email={self.email}, role={self.role})>"
