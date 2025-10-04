# backend/app/repositories/knowledge_base_repository.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models.db_knowledge_base import KnowledgeBase
from app.repositories.base import BaseRepository


class KnowledgeBaseRepository(BaseRepository[KnowledgeBase]):
    """Repository for Knowledge Base operations"""
    
    def __init__(self, db: Session):
        super().__init__(KnowledgeBase, db)
    
    def get_all_active(self, skip: int = 0, limit: int = 100) -> List[KnowledgeBase]:
        """Get all active knowledge base articles with pagination"""
        return self.db.query(self.model).filter(
            self.model.is_active == True
        ).offset(skip).limit(limit).all()
    
    def get_by_category(self, category: str, active_only: bool = True) -> List[KnowledgeBase]:
        """Get knowledge base articles by category"""
        query = self.db.query(self.model).filter(self.model.category == category)
        if active_only:
            query = query.filter(self.model.is_active == True)
        return query.all()
    
    def search(self, query: str, category: Optional[str] = None, active_only: bool = True) -> List[KnowledgeBase]:
        """
        Search knowledge base by text in title, content, or tags.
        Supports filtering by category.
        """
        from sqlalchemy import cast, String, func
        # Cast tags array to text and search within it
        search_filter = or_(
            self.model.title.ilike(f"%{query}%"),
            self.model.content.ilike(f"%{query}%"),
            cast(self.model.tags, String).ilike(f"%{query}%")  # Cast array to string for searching
        )
        
        filters = [search_filter]
        if active_only:
            filters.append(self.model.is_active == True)
        if category:
            filters.append(self.model.category == category)
        
        return self.db.query(self.model).filter(and_(*filters)).all()
    
    def get_by_tag(self, tag: str, active_only: bool = True) -> List[KnowledgeBase]:
        """Get knowledge base articles by specific tag"""
        query = self.db.query(self.model).filter(self.model.tags.contains([tag]))
        if active_only:
            query = query.filter(self.model.is_active == True)
        return query.all()
    
    def create_article(
        self,
        title: str,
        content: str,
        category: str,
        tags: List[str],
        created_by_id: int,
        is_active: bool = True
    ) -> KnowledgeBase:
        """Create a new knowledge base article"""
        article = KnowledgeBase(
            title=title,
            content=content,
            category=category,
            tags=tags,
            is_active=is_active,
            created_by_id=created_by_id
        )
        self.db.add(article)
        self.db.flush()
        return article
    
    def update_article(
        self,
        article_id: int,
        updated_by_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        is_active: Optional[bool] = None
    ) -> Optional[KnowledgeBase]:
        """Update an existing knowledge base article"""
        article = self.get(article_id)
        if not article:
            return None
        
        if title is not None:
            article.title = title
        if content is not None:
            article.content = content
        if category is not None:
            article.category = category
        if tags is not None:
            article.tags = tags
        if is_active is not None:
            article.is_active = is_active
        
        article.updated_by_id = updated_by_id
        self.db.flush()
        return article
