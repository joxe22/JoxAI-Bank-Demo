from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
import time

from app.models.db_notification import (
    Notification,
    NotificationType,
    NotificationStatus,
    NotificationCategory
)
from app.repositories.base import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    def __init__(self, db: Session):
        super().__init__(Notification, db)
    
    def create_notification(
        self,
        user_id: Optional[int],
        recipient_email: Optional[str],
        notification_type: NotificationType,
        category: NotificationCategory,
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        extra_data: Optional[dict] = None
    ) -> Notification:
        """Create a new notification record."""
        notification = Notification(
            user_id=user_id,
            recipient_email=recipient_email,
            notification_type=notification_type,
            category=category,
            status=NotificationStatus.PENDING,
            subject=subject,
            body=body,
            html_body=html_body,
            resource_type=resource_type,
            resource_id=resource_id,
            extra_data=extra_data,
            delivery_attempts=0
        )
        return self.create(notification)
    
    def mark_as_sent(self, notification_id: int) -> Optional[Notification]:
        """Mark notification as successfully sent."""
        notification = self.get_by_id(notification_id)
        if notification:
            notification.status = NotificationStatus.SENT
            notification.sent_at = int(time.time())
            self.db.commit()
            self.db.refresh(notification)
        return notification
    
    def mark_as_failed(
        self,
        notification_id: int,
        error_message: str
    ) -> Optional[Notification]:
        """Mark notification as failed with error message."""
        notification = self.get_by_id(notification_id)
        if notification:
            notification.status = NotificationStatus.FAILED
            notification.error_message = error_message
            notification.delivery_attempts += 1
            notification.last_attempt_at = int(time.time())
            self.db.commit()
            self.db.refresh(notification)
        return notification
    
    def increment_delivery_attempt(self, notification_id: int) -> Optional[Notification]:
        """Increment delivery attempt counter."""
        notification = self.get_by_id(notification_id)
        if notification:
            notification.delivery_attempts += 1
            notification.last_attempt_at = int(time.time())
            self.db.commit()
            self.db.refresh(notification)
        return notification
    
    def get_user_notifications(
        self,
        user_id: int,
        category: Optional[NotificationCategory] = None,
        status: Optional[NotificationStatus] = None,
        limit: int = 50
    ) -> List[Notification]:
        """Get notifications for a specific user."""
        query = self.db.query(Notification).filter(Notification.user_id == user_id)
        
        if category:
            query = query.filter(Notification.category == category)
        
        if status:
            query = query.filter(Notification.status == status)
        
        return query.order_by(Notification.created_at.desc()).limit(limit).all()
    
    def get_pending_notifications(self, limit: int = 100) -> List[Notification]:
        """Get all pending notifications for batch processing."""
        return self.db.query(Notification).filter(
            and_(
                Notification.status == NotificationStatus.PENDING,
                Notification.delivery_attempts < 3  # Max 3 attempts
            )
        ).order_by(Notification.created_at).limit(limit).all()
    
    def get_notifications_by_resource(
        self,
        resource_type: str,
        resource_id: str
    ) -> List[Notification]:
        """Get all notifications related to a specific resource."""
        return self.db.query(Notification).filter(
            and_(
                Notification.resource_type == resource_type,
                Notification.resource_id == resource_id
            )
        ).order_by(Notification.created_at.desc()).all()
    
    def get_notification_stats(self) -> dict:
        """Get notification statistics."""
        from sqlalchemy import func
        
        total = self.db.query(func.count(Notification.id)).scalar() or 0
        
        by_status = self.db.query(
            Notification.status,
            func.count(Notification.id).label('count')
        ).group_by(Notification.status).all()
        
        by_category = self.db.query(
            Notification.category,
            func.count(Notification.id).label('count')
        ).group_by(Notification.category).all()
        
        by_type = self.db.query(
            Notification.notification_type,
            func.count(Notification.id).label('count')
        ).group_by(Notification.notification_type).all()
        
        return {
            "total_notifications": total,
            "by_status": {status.value: count for status, count in by_status},
            "by_category": {category.value: count for category, count in by_category},
            "by_type": {ntype.value: count for ntype, count in by_type},
        }
