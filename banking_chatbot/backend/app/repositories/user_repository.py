"""
User repository for database operations.
"""

from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.db_user import DBUser, UserRole
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[DBUser]):
    """Repository for User operations"""

    def __init__(self, db: Session):
        super().__init__(DBUser, db)

    def get_by_email(self, email: str) -> Optional[DBUser]:
        """Get user by email"""
        return self.get_by(email=email)

    def get_by_username(self, username: str) -> Optional[DBUser]:
        """Get user by username"""
        return self.get_by(username=username)

    def get_by_role(self, role: UserRole, is_active: bool = True) -> List[DBUser]:
        """Get all users by role"""
        return self.get_all(role=role, is_active=is_active)

    def get_active_agents(self) -> List[DBUser]:
        """Get all active agents"""
        return self.db.query(DBUser).filter(
            DBUser.role == UserRole.AGENT,
            DBUser.is_active == True,
        ).all()

    def get_online_agents(self) -> List[DBUser]:
        """Get all online agents"""
        return self.db.query(DBUser).filter(
            DBUser.role == UserRole.AGENT,
            DBUser.is_active == True,
            DBUser.is_online == True,
        ).all()

    def set_online_status(self, user_id: int, is_online: bool) -> Optional[DBUser]:
        """Set user online/offline status"""
        return self.update(user_id, is_online=is_online)

    def deactivate(self, user_id: int) -> Optional[DBUser]:
        """Deactivate a user"""
        return self.update(user_id, is_active=False)

    def activate(self, user_id: int) -> Optional[DBUser]:
        """Activate a user"""
        return self.update(user_id, is_active=True)

    def email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        return self.exists(email=email)

    def username_exists(self, username: str) -> bool:
        """Check if username already exists"""
        return self.exists(username=username)
