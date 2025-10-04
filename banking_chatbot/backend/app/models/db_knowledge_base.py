# backend/app/models/db_knowledge_base.py
from sqlalchemy import Column, Integer, String, Text, Boolean, ARRAY
from app.models.base import BaseModel


class KnowledgeBase(BaseModel):
    """
    Knowledge Base model for storing banking knowledge articles.
    Used by the AI chatbot to provide accurate, up-to-date information.
    """
    __tablename__ = "knowledge_base"

    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)  # e.g., "balance", "transfers", "loans", "cards"
    tags = Column(ARRAY(String), default=list)  # Searchable tags
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Track who created/updated
    created_by_id = Column(Integer, nullable=True)
    updated_by_id = Column(Integer, nullable=True)
    
    def __repr__(self):
        return f"<KnowledgeBase(id={self.id}, title='{self.title}', category='{self.category}')>"
