# backend/app/core/audit.py
from typing import Optional
from fastapi import Request
from sqlalchemy.orm import Session
from app.repositories.audit_log_repository import AuditLogRepository
from app.database import SessionLocal


def log_audit(
    db: Session,  # Kept for API compatibility, not used internally
    action: str,
    request: Optional[Request] = None,
    user_id: Optional[int] = None,
    user_email: Optional[str] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    status: str = "SUCCESS",
    details: Optional[dict] = None,
    error_message: Optional[str] = None
):
    """
    Helper function to log audit events.
    
    IMPORTANT: This function uses an independent database session to ensure
    audit logs are persisted even when the main operation fails and its
    transaction is rolled back. This prevents loss of security audit trails.
    
    Only primitive types (int, str, dict) should be passed - never ORM objects.
    
    Args:
        db: Database session (kept for API compatibility but not used)
        action: Action being performed (e.g., "LOGIN", "CREATE_TICKET")
        request: FastAPI Request object (optional)
        user_id: ID of user performing the action (primitive int, not ORM object)
        user_email: Email of user performing the action (primitive str)
        resource_type: Type of resource being acted upon
        resource_id: ID of the resource (as string)
        status: Status of the action (SUCCESS, FAILURE, ERROR)
        details: Additional metadata as dictionary
        error_message: Error message if action failed
    """
    # Extract request metadata if available
    ip_address = None
    user_agent = None
    endpoint = None
    method = None
    
    if request:
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        endpoint = str(request.url.path)
        method = request.method
    
    # Use independent session to ensure audit logs persist even on failure
    audit_db = SessionLocal()
    try:
        audit_repo = AuditLogRepository(audit_db)
        audit_repo.create_log(
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
            error_message=error_message
        )
        audit_db.commit()
    except Exception as e:
        # Don't fail the main operation if audit logging fails
        print(f"⚠️ Audit logging failed: {str(e)}")
        audit_db.rollback()
    finally:
        audit_db.close()
