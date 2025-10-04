from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.models.base import BaseModel


class CustomerType(str, enum.Enum):
    INDIVIDUAL = "INDIVIDUAL"
    BUSINESS = "BUSINESS"


class CustomerStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class Customer(BaseModel):
    __tablename__ = "customers"

    full_name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(50), nullable=True, index=True)
    account_number = Column(String(100), unique=True, nullable=True, index=True)
    
    customer_type = Column(
        SQLAEnum(CustomerType, name="customer_type_enum"),
        nullable=False,
        default=CustomerType.INDIVIDUAL,
        server_default=CustomerType.INDIVIDUAL.value
    )
    
    status = Column(
        SQLAEnum(CustomerStatus, name="customer_status_enum"),
        nullable=False,
        default=CustomerStatus.ACTIVE,
        server_default=CustomerStatus.ACTIVE.value,
        index=True
    )
    
    preferences = Column(JSONB, nullable=True, default={})
    tags = Column(ARRAY(String), nullable=True, default=[])
    notes = Column(Text, nullable=True)
    
    assigned_agent_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    assigned_agent = relationship("DBUser", foreign_keys=[assigned_agent_id])
    created_by = relationship("DBUser", foreign_keys=[created_by_id])
    updated_by = relationship("DBUser", foreign_keys=[updated_by_id])
    
    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.full_name}', email='{self.email}', status='{self.status}')>"
