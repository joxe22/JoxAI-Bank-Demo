"""
Base models and mixins for SQLAlchemy.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declared_attr

from app.database import Base


class TimestampMixin:
    """
    Mixin que agrega created_at y updated_at a los modelos.
    Uses server_default for consistency with database-level defaults.
    """
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class BaseModel(Base, TimestampMixin):
    """
    Modelo base abstracto con ID y timestamps.
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    def dict(self):
        """Convert model to dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"
