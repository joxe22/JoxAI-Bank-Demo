"""
Message repository for database operations.
"""

from typing import List
from sqlalchemy.orm import Session

from app.models.db_message import DBMessage, MessageRole
from app.repositories.base import BaseRepository


class MessageRepository(BaseRepository[DBMessage]):
    """Repository for Message operations"""

    def __init__(self, db: Session):
        super().__init__(DBMessage, db)

    def get_by_conversation(
        self, conversation_id: int, skip: int = 0, limit: int = 100
    ) -> List[DBMessage]:
        """Get all messages for a conversation"""
        return (
            self.db.query(DBMessage)
            .filter(DBMessage.conversation_id == conversation_id)
            .order_by(DBMessage.created_at.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_user_messages(
        self, conversation_id: int, skip: int = 0, limit: int = 100
    ) -> List[DBMessage]:
        """Get only user messages"""
        return (
            self.db.query(DBMessage)
            .filter(
                DBMessage.conversation_id == conversation_id,
                DBMessage.role == MessageRole.USER,
            )
            .order_by(DBMessage.created_at.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_assistant_messages(
        self, conversation_id: int, skip: int = 0, limit: int = 100
    ) -> List[DBMessage]:
        """Get only assistant messages"""
        return (
            self.db.query(DBMessage)
            .filter(
                DBMessage.conversation_id == conversation_id,
                DBMessage.role == MessageRole.ASSISTANT,
            )
            .order_by(DBMessage.created_at.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_by_conversation(self, conversation_id: int) -> int:
        """Count messages in a conversation"""
        return self.count(conversation_id=conversation_id)

    def get_latest_message(self, conversation_id: int) -> DBMessage:
        """Get the latest message in a conversation"""
        return (
            self.db.query(DBMessage)
            .filter(DBMessage.conversation_id == conversation_id)
            .order_by(DBMessage.created_at.desc())
            .first()
        )

    def delete_by_conversation(self, conversation_id: int) -> int:
        """
        Delete all messages in a conversation.
        Note: Does NOT commit - commit should be handled by service layer.
        """
        result = (
            self.db.query(DBMessage)
            .filter(DBMessage.conversation_id == conversation_id)
            .delete()
        )
        self.db.flush()
        return result
