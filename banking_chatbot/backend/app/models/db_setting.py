from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
import enum

from .base import BaseModel


class SettingType(str, enum.Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"


class Setting(BaseModel):
    __tablename__ = "settings"
    
    key = Column(String(255), nullable=False, index=True)
    value = Column(JSONB, nullable=False)
    setting_type = Column(SQLEnum(SettingType, name="setting_type"), nullable=False, default=SettingType.SYSTEM, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    category = Column(String(100), nullable=True, index=True)
    description = Column(Text, nullable=True)
    is_public = Column(Boolean, default=False, nullable=False)
    
    user = relationship("DBUser", foreign_keys=[user_id])
    
    def __repr__(self):
        return f"<Setting(key='{self.key}', type='{self.setting_type}', user_id={self.user_id})>"
