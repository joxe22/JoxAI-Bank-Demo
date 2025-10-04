"""
Conversation repository for database operations.
"""

from typing import Optional, List
from sqlalchemy.orm import Session, joinedload

from app.models.db_conversation import DBConversation
from app.repositories.base import BaseRepository


class ConversationRepository(BaseRepository[DBConversation]):
    """Repository for Conversation operations"""

    def __init__(self, db: Session):
        super().__init__(DBConversation, db)

    def get_by_conversation_id(self, conversation_id: str) -> Optional[DBConversation]:
        """Get conversation by conversation_id (UUID)"""
        return self.get_by(conversation_id=conversation_id)

    def get_with_messages(self, conversation_id: str) -> Optional[DBConversation]:
        """Get conversation with all messages loaded"""
        return (
            self.db.query(DBConversation)
            .options(joinedload(DBConversation.messages))
            .filter(DBConversation.conversation_id == conversation_id)
            .first()
        )

    def get_with_tickets(self, conversation_id: str) -> Optional[DBConversation]:
        """Get conversation with all tickets loaded"""
        return (
            self.db.query(DBConversation)
            .options(joinedload(DBConversation.tickets))
            .filter(DBConversation.conversation_id == conversation_id)
            .first()
        )

    def get_by_user(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[DBConversation]:
        """Get all conversations for a user"""
        return self.get_all(skip=skip, limit=limit, user_id=user_id)

    def get_active_conversations(
        self, skip: int = 0, limit: int = 100
    ) -> List[DBConversation]:
        """Get all active conversations"""
        return self.get_all(skip=skip, limit=limit, is_active=True)

    def get_escalated_conversations(
        self, skip: int = 0, limit: int = 100
    ) -> List[DBConversation]:
        """Get all escalated conversations"""
        return self.get_all(skip=skip, limit=limit, is_escalated=True)

    def escalate(
        self, conversation_id: str, reason: str
    ) -> Optional[DBConversation]:
        """Escalate a conversation"""
        conversation = self.get_by_conversation_id(conversation_id)
        if conversation:
            return self.update(
                conversation.id, is_escalated=True, escalation_reason=reason
            )
        return None

    def close(self, conversation_id: str) -> Optional[DBConversation]:
        """Close/deactivate a conversation"""
        conversation = self.get_by_conversation_id(conversation_id)
        if conversation:
            return self.update(conversation.id, is_active=False)
        return None

    def update_sentiment(
        self, conversation_id: str, sentiment_score: int
    ) -> Optional[DBConversation]:
        """Update conversation sentiment score"""
        conversation = self.get_by_conversation_id(conversation_id)
        if conversation:
            return self.update(conversation.id, sentiment_score=sentiment_score)
        return None
