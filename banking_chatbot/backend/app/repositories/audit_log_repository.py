# backend/app/repositories/audit_log_repository.py
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import desc
from app.repositories.base import BaseRepository
from app.models.db_audit_log import AuditLog


class AuditLogRepository(BaseRepository[AuditLog]):
    """Repository for audit log operations"""
    
    def __init__(self, db):
        super().__init__(AuditLog, db)
    
    def create_log(
        self,
        action: str,
        status: str = "SUCCESS",
        user_id: Optional[int] = None,
        user_email: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        endpoint: Optional[str] = None,
        method: Optional[str] = None,
        details: Optional[dict] = None,
        error_message: Optional[str] = None
    ) -> AuditLog:
        """Create a new audit log entry"""
        log = AuditLog(
            action=action,
            status=status,
            user_id=user_id,
            user_email=user_email,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            endpoint=endpoint,
            method=method,
            details=details,
            error_message=error_message,
            timestamp=datetime.utcnow()
        )
        self.db.add(log)
        self.db.flush()
        return log
    
    def get_by_user(self, user_id: int, limit: int = 100) -> List[AuditLog]:
        """Get audit logs for a specific user"""
        return (
            self.db.query(AuditLog)
            .filter(AuditLog.user_id == user_id)
            .order_by(desc(AuditLog.timestamp))
            .limit(limit)
            .all()
        )
    
    def get_by_action(self, action: str, limit: int = 100) -> List[AuditLog]:
        """Get audit logs for a specific action"""
        return (
            self.db.query(AuditLog)
            .filter(AuditLog.action == action)
            .order_by(desc(AuditLog.timestamp))
            .limit(limit)
            .all()
        )
    
    def get_recent(self, hours: int = 24, limit: int = 100) -> List[AuditLog]:
        """Get recent audit logs within specified hours"""
        since = datetime.utcnow() - timedelta(hours=hours)
        return (
            self.db.query(AuditLog)
            .filter(AuditLog.timestamp >= since)
            .order_by(desc(AuditLog.timestamp))
            .limit(limit)
            .all()
        )
    
    def get_failed_attempts(self, hours: int = 24, limit: int = 100) -> List[AuditLog]:
        """Get failed login/authentication attempts"""
        since = datetime.utcnow() - timedelta(hours=hours)
        return (
            self.db.query(AuditLog)
            .filter(
                AuditLog.timestamp >= since,
                AuditLog.status == "FAILURE"
            )
            .order_by(desc(AuditLog.timestamp))
            .limit(limit)
            .all()
        )
