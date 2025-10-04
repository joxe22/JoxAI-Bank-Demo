# backend/app/api/v1/knowledge.py
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.knowledge_base_repository import KnowledgeBaseRepository
from app.core.security import verify_token
from app.core.audit import log_audit
from app.repositories import UserRepository

router = APIRouter()


class KnowledgeBaseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1, max_length=100)
    tags: List[str] = Field(default_factory=list)
    is_active: bool = Field(default=True)


class KnowledgeBaseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class KnowledgeBaseResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: List[str]
    is_active: bool
    created_by_id: Optional[int]
    updated_by_id: Optional[int]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


def get_current_user_id(request: Request) -> int:
    """Extract user ID from JWT token"""
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    try:
        payload = verify_token(token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload.get("user_id", 1)  # Default to 1 if not in token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/", response_model=List[KnowledgeBaseResponse])
async def list_knowledge_base(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """List all knowledge base articles with optional filtering"""
    kb_repo = KnowledgeBaseRepository(db)
    
    if category:
        articles = kb_repo.get_by_category(category, active_only)
    else:
        if active_only:
            articles = kb_repo.get_all_active(skip, limit)
        else:
            articles = kb_repo.get_all(skip, limit)
    
    return [
        KnowledgeBaseResponse(
            id=article.id,
            title=article.title,
            content=article.content,
            category=article.category,
            tags=article.tags or [],
            is_active=article.is_active,
            created_by_id=article.created_by_id,
            updated_by_id=article.updated_by_id,
            created_at=article.created_at.isoformat() if article.created_at else "",
            updated_at=article.updated_at.isoformat() if article.updated_at else ""
        )
        for article in articles
    ]


@router.get("/search", response_model=List[KnowledgeBaseResponse])
async def search_knowledge_base(
    q: str,
    category: Optional[str] = None,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Search knowledge base by text in title, content, or tags"""
    kb_repo = KnowledgeBaseRepository(db)
    articles = kb_repo.search(q, category, active_only)
    
    return [
        KnowledgeBaseResponse(
            id=article.id,
            title=article.title,
            content=article.content,
            category=article.category,
            tags=article.tags or [],
            is_active=article.is_active,
            created_by_id=article.created_by_id,
            updated_by_id=article.updated_by_id,
            created_at=article.created_at.isoformat() if article.created_at else "",
            updated_at=article.updated_at.isoformat() if article.updated_at else ""
        )
        for article in articles
    ]


@router.get("/{article_id}", response_model=KnowledgeBaseResponse)
async def get_knowledge_base(article_id: int, db: Session = Depends(get_db)):
    """Get a specific knowledge base article by ID"""
    kb_repo = KnowledgeBaseRepository(db)
    article = kb_repo.get(article_id)
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return KnowledgeBaseResponse(
        id=article.id,
        title=article.title,
        content=article.content,
        category=article.category,
        tags=article.tags or [],
        is_active=article.is_active,
        created_by_id=article.created_by_id,
        updated_by_id=article.updated_by_id,
        created_at=article.created_at.isoformat() if article.created_at else "",
        updated_at=article.updated_at.isoformat() if article.updated_at else ""
    )


@router.post("/", response_model=KnowledgeBaseResponse, status_code=201)
async def create_knowledge_base(
    request: Request,
    data: KnowledgeBaseCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a new knowledge base article"""
    kb_repo = KnowledgeBaseRepository(db)
    
    article = kb_repo.create_article(
        title=data.title,
        content=data.content,
        category=data.category,
        tags=data.tags,
        created_by_id=user_id,
        is_active=data.is_active
    )
    db.commit()
    
    # Audit log
    log_audit(
        db=db,
        action="KB_CREATE",
        request=request,
        user_id=user_id,
        resource_type="KNOWLEDGE_BASE",
        resource_id=str(article.id),
        status="SUCCESS",
        details={"title": article.title, "category": article.category}
    )
    
    return KnowledgeBaseResponse(
        id=article.id,
        title=article.title,
        content=article.content,
        category=article.category,
        tags=article.tags or [],
        is_active=article.is_active,
        created_by_id=article.created_by_id,
        updated_by_id=article.updated_by_id,
        created_at=article.created_at.isoformat() if article.created_at else "",
        updated_at=article.updated_at.isoformat() if article.updated_at else ""
    )


@router.put("/{article_id}", response_model=KnowledgeBaseResponse)
async def update_knowledge_base(
    request: Request,
    article_id: int,
    data: KnowledgeBaseUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update an existing knowledge base article"""
    kb_repo = KnowledgeBaseRepository(db)
    
    article = kb_repo.update_article(
        article_id=article_id,
        updated_by_id=user_id,
        title=data.title,
        content=data.content,
        category=data.category,
        tags=data.tags,
        is_active=data.is_active
    )
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    db.commit()
    
    # Audit log
    log_audit(
        db=db,
        action="KB_UPDATE",
        request=request,
        user_id=user_id,
        resource_type="KNOWLEDGE_BASE",
        resource_id=str(article.id),
        status="SUCCESS",
        details={"title": article.title, "category": article.category}
    )
    
    return KnowledgeBaseResponse(
        id=article.id,
        title=article.title,
        content=article.content,
        category=article.category,
        tags=article.tags or [],
        is_active=article.is_active,
        created_by_id=article.created_by_id,
        updated_by_id=article.updated_by_id,
        created_at=article.created_at.isoformat() if article.created_at else "",
        updated_at=article.updated_at.isoformat() if article.updated_at else ""
    )


@router.delete("/{article_id}", status_code=204)
async def delete_knowledge_base(
    article_id: int,
    *,
    request: Request,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Delete a knowledge base article"""
    kb_repo = KnowledgeBaseRepository(db)
    article = kb_repo.get(article_id)
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    title = article.title
    category = article.category
    
    kb_repo.delete(article_id)
    db.commit()
    
    # Audit log
    log_audit(
        db=db,
        action="KB_DELETE",
        request=request,
        user_id=user_id,
        resource_type="KNOWLEDGE_BASE",
        resource_id=str(article_id),
        status="SUCCESS",
        details={"title": title, "category": category}
    )
    
    return None
