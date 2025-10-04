# backend/app/models/db_audit_log.py
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from datetime import datetime
from app.models.base import BaseModel


class AuditLog(BaseModel):
    """
    Audit log model for tracking all critical operations in the system.
    Used for compliance, security monitoring, and debugging.
    
    Inherits from BaseModel to get standard id, created_at, updated_at fields.
    The 'timestamp' field specifically captures when the audited action occurred.
    """
    __tablename__ = "audit_logs"
    
    # Who performed the action
    user_id = Column(Integer, nullable=True, index=True)
    user_email = Column(String, nullable=True)
    
    # What action was performed
    action = Column(String, nullable=False, index=True)  # e.g., "LOGIN", "CREATE_TICKET", "UPDATE_CONVERSATION"
    resource_type = Column(String, nullable=True)  # e.g., "USER", "TICKET", "CONVERSATION"
    resource_id = Column(String, nullable=True)  # ID of the affected resource
    
    # When and where
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    # Additional context
    status = Column(String, nullable=False, default="SUCCESS")  # SUCCESS, FAILURE, ERROR
    details = Column(JSON, nullable=True)  # Additional metadata as JSON
    error_message = Column(Text, nullable=True)
    
    # Request context
    endpoint = Column(String, nullable=True)
    method = Column(String, nullable=True)  # GET, POST, PUT, DELETE
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action='{self.action}', user={self.user_email}, timestamp={self.timestamp})>"
