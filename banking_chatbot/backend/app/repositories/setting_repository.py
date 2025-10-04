from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.db_setting import Setting, SettingType
from app.repositories.base import BaseRepository


class SettingRepository(BaseRepository[Setting]):
    def __init__(self, db: Session):
        super().__init__(Setting, db)
    
    def get_system_setting(self, key: str, default: Any = None) -> Any:
        setting = self.db.query(Setting).filter(
            and_(
                Setting.key == key,
                Setting.setting_type == SettingType.SYSTEM
            )
        ).first()
        
        if setting:
            return setting.value
        return default
    
    def get_user_setting(self, user_id: int, key: str, default: Any = None) -> Any:
        setting = self.db.query(Setting).filter(
            and_(
                Setting.key == key,
                Setting.user_id == user_id,
                Setting.setting_type == SettingType.USER
            )
        ).first()
        
        if setting:
            return setting.value
        return default
    
    def set_system_setting(
        self,
        key: str,
        value: Any,
        category: Optional[str] = None,
        description: Optional[str] = None,
        is_public: bool = False
    ) -> Setting:
        setting = self.db.query(Setting).filter(
            and_(
                Setting.key == key,
                Setting.setting_type == SettingType.SYSTEM
            )
        ).first()
        
        if setting:
            setting.value = value
            if category is not None:
                setting.category = category
            if description is not None:
                setting.description = description
            setting.is_public = is_public
        else:
            setting = Setting(
                key=key,
                value=value,
                setting_type=SettingType.SYSTEM,
                category=category,
                description=description,
                is_public=is_public
            )
            self.db.add(setting)
        
        self.db.commit()
        self.db.refresh(setting)
        return setting
    
    def set_user_setting(
        self,
        user_id: int,
        key: str,
        value: Any,
        category: Optional[str] = None,
        description: Optional[str] = None
    ) -> Setting:
        setting = self.db.query(Setting).filter(
            and_(
                Setting.key == key,
                Setting.user_id == user_id,
                Setting.setting_type == SettingType.USER
            )
        ).first()
        
        if setting:
            setting.value = value
            if category is not None:
                setting.category = category
            if description is not None:
                setting.description = description
        else:
            setting = Setting(
                key=key,
                value=value,
                setting_type=SettingType.USER,
                user_id=user_id,
                category=category,
                description=description,
                is_public=False
            )
            self.db.add(setting)
        
        self.db.commit()
        self.db.refresh(setting)
        return setting
    
    def get_all_system_settings(self, category: Optional[str] = None) -> List[Setting]:
        query = self.db.query(Setting).filter(Setting.setting_type == SettingType.SYSTEM)
        
        if category:
            query = query.filter(Setting.category == category)
        
        return query.all()
    
    def get_all_user_settings(self, user_id: int, category: Optional[str] = None) -> List[Setting]:
        query = self.db.query(Setting).filter(
            and_(
                Setting.user_id == user_id,
                Setting.setting_type == SettingType.USER
            )
        )
        
        if category:
            query = query.filter(Setting.category == category)
        
        return query.all()
    
    def delete_system_setting(self, key: str) -> bool:
        setting = self.db.query(Setting).filter(
            and_(
                Setting.key == key,
                Setting.setting_type == SettingType.SYSTEM
            )
        ).first()
        
        if setting:
            self.db.delete(setting)
            self.db.commit()
            return True
        return False
    
    def delete_user_setting(self, user_id: int, key: str) -> bool:
        setting = self.db.query(Setting).filter(
            and_(
                Setting.key == key,
                Setting.user_id == user_id,
                Setting.setting_type == SettingType.USER
            )
        ).first()
        
        if setting:
            self.db.delete(setting)
            self.db.commit()
            return True
        return False
    
    def get_public_settings(self) -> List[Setting]:
        return self.db.query(Setting).filter(
            and_(
                Setting.setting_type == SettingType.SYSTEM,
                Setting.is_public == True
            )
        ).all()
