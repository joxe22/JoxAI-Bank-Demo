"""
Base repository with common CRUD operations.
"""

from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, func

from app.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """
    Base repository with generic CRUD operations.
    All repositories inherit from this class.
    """

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get(self, id: int) -> Optional[ModelType]:
        """Get a single record by ID"""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_by(self, **filters) -> Optional[ModelType]:
        """Get a single record by arbitrary filters"""
        query = self.db.query(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.first()

    def get_all(
        self, skip: int = 0, limit: int = 100, **filters
    ) -> List[ModelType]:
        """Get all records with optional pagination and filters"""
        query = self.db.query(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.offset(skip).limit(limit).all()

    def count(self, **filters) -> int:
        """Count records with optional filters"""
        query = self.db.query(func.count(self.model.id))
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.scalar()

    def create(self, **data) -> ModelType:
        """
        Create a new record.
        Note: Does NOT commit - commit should be handled by service layer.
        """
        instance = self.model(**data)
        self.db.add(instance)
        self.db.flush()
        self.db.refresh(instance)
        return instance

    def update(self, id: int, **data) -> Optional[ModelType]:
        """
        Update a record by ID.
        Note: Does NOT commit - commit should be handled by service layer.
        """
        instance = self.get(id)
        if not instance:
            return None

        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        self.db.flush()
        self.db.refresh(instance)
        return instance

    def delete(self, id: int) -> bool:
        """
        Delete a record by ID.
        Note: Does NOT commit - commit should be handled by service layer.
        """
        instance = self.get(id)
        if not instance:
            return False

        self.db.delete(instance)
        self.db.flush()
        return True

    def bulk_create(self, items: List[Dict[str, Any]]) -> List[ModelType]:
        """
        Bulk create multiple records.
        Note: Does NOT commit - commit should be handled by service layer.
        """
        instances = [self.model(**item) for item in items]
        self.db.add_all(instances)
        self.db.flush()
        for instance in instances:
            self.db.refresh(instance)
        return instances

    def exists(self, **filters) -> bool:
        """Check if a record exists with given filters"""
        query = self.db.query(self.model.id)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.first() is not None
