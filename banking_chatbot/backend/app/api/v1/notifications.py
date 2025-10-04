from fastapi import APIRouter, Depends, Request, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

from app.database import get_db
from app.core.security import verify_token
from app.core.limiter import limiter
from app.repositories import NotificationRepository
from app.models.db_notification import NotificationType, NotificationStatus, NotificationCategory

router = APIRouter()


def get_current_user(request: Request) -> dict:
    """Extract user info from JWT token"""
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    try:
        payload = verify_token(token)
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")


class NotificationResponse(BaseModel):
    id: int
    user_id: Optional[int]
    recipient_email: Optional[str]
    notification_type: str
    category: str
    status: str
    subject: Optional[str]
    body: str
    resource_type: Optional[str]
    resource_id: Optional[str]
    sent_at: Optional[int]
    delivery_attempts: int
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


@router.get("/me", response_model=List[NotificationResponse])
@limiter.limit("30/minute")
async def get_my_notifications(
    request: Request,
    category: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(50, ge=1, le=200, description="Number of notifications to return"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get notifications for the current user.
    Supports filtering by category and status.
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token: user_id missing")
    
    notification_repo = NotificationRepository(db)
    
    # Parse filters
    category_filter = NotificationCategory(category) if category else None
    status_filter = NotificationStatus(status) if status else None
    
    notifications = notification_repo.get_user_notifications(
        user_id=user_id,
        category=category_filter,
        status=status_filter,
        limit=limit
    )
    
    return [NotificationResponse.model_validate(n) for n in notifications]


@router.get("/stats")
@limiter.limit("30/minute")
async def get_notification_stats(
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get notification statistics.
    Admin/Supervisor only.
    """
    if current_user.get("role") not in ["ADMIN", "SUPERVISOR"]:
        raise HTTPException(status_code=403, detail="Not authorized to view notification statistics")
    
    notification_repo = NotificationRepository(db)
    return notification_repo.get_notification_stats()


@router.get("/{notification_id}", response_model=NotificationResponse)
@limiter.limit("30/minute")
async def get_notification(
    notification_id: int,
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific notification by ID.
    Users can only access their own notifications.
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token: user_id missing")
    
    notification_repo = NotificationRepository(db)
    notification = notification_repo.get_by_id(notification_id)
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    # Check ownership (unless admin/supervisor)
    if current_user.get("role") not in ["ADMIN", "SUPERVISOR"]:
        if notification.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this notification")
    
    return NotificationResponse.model_validate(notification)


@router.post("/{notification_id}/retry")
@limiter.limit("10/minute")
async def retry_notification(
    notification_id: int,
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retry sending a failed notification.
    Admin/Supervisor only.
    """
    if current_user.get("role") not in ["ADMIN", "SUPERVISOR"]:
        raise HTTPException(status_code=403, detail="Not authorized to retry notifications")
    
    notification_repo = NotificationRepository(db)
    notification = notification_repo.get_by_id(notification_id)
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    if notification.status != NotificationStatus.FAILED:
        raise HTTPException(status_code=400, detail="Can only retry failed notifications")
    
    # Reset status to pending for retry
    notification.status = NotificationStatus.PENDING
    db.commit()
    
    return {"message": "Notification queued for retry", "notification_id": notification_id}
