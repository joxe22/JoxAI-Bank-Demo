from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from typing import Optional, Any, List, Dict
from pydantic import BaseModel
from datetime import datetime as dt

from app.database import get_db
from app.core.security import verify_token
from app.core.limiter import limiter
from app.core.audit import log_audit
from app.repositories import SettingRepository
from app.models.db_setting import SettingType

router = APIRouter()


def get_current_user(request: Request) -> dict:
    """Extract user info from JWT token"""
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    try:
        payload = verify_token(token)
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")


class SettingCreate(BaseModel):
    key: str
    value: Any
    category: Optional[str] = None
    description: Optional[str] = None
    is_public: bool = False


class SettingUpdate(BaseModel):
    value: Any
    category: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None


class SettingResponse(BaseModel):
    id: int
    key: str
    value: Any
    setting_type: str
    user_id: Optional[int]
    category: Optional[str]
    description: Optional[str]
    is_public: bool
    created_at: dt
    updated_at: dt

    class Config:
        from_attributes = True
        json_encoders = {
            dt: lambda v: v.isoformat()
        }


@router.get("/system", response_model=List[SettingResponse])
@limiter.limit("30/minute")
async def get_system_settings(
    request: Request,
    category: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] not in ["ADMIN", "SUPERVISOR"]:
        raise HTTPException(status_code=403, detail="Not authorized to view system settings")
    
    setting_repo = SettingRepository(db)
    settings = setting_repo.get_all_system_settings(category=category)
    
    log_audit(
        db=db,
        action="SETTINGS_VIEWED",
        request=request,
        user_id=current_user.get("user_id"),
        user_email=current_user["sub"],
        status="SUCCESS",
        details={"setting_type": "SYSTEM", "category": category}
    )
    
    return [SettingResponse.model_validate(s) for s in settings]


@router.get("/system/{key}")
@limiter.limit("30/minute")
async def get_system_setting(
    key: str,
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] not in ["ADMIN", "SUPERVISOR"]:
        raise HTTPException(status_code=403, detail="Not authorized to view system settings")
    
    setting_repo = SettingRepository(db)
    value = setting_repo.get_system_setting(key)
    
    if value is None:
        raise HTTPException(status_code=404, detail=f"Setting '{key}' not found")
    
    return {"key": key, "value": value}


@router.post("/system", response_model=SettingResponse, status_code=201)
@limiter.limit("20/minute")
async def create_system_setting(
    *,
    setting_data: SettingCreate,
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Only admins can create system settings")
    
    try:
        setting_repo = SettingRepository(db)
        setting = setting_repo.set_system_setting(
            key=setting_data.key,
            value=setting_data.value,
            category=setting_data.category,
            description=setting_data.description,
            is_public=setting_data.is_public
        )
        
        log_audit(
            db=db,
            action="SETTING_CREATE",
            request=request,
            user_id=current_user.get("user_id"),
            user_email=current_user["sub"],
            resource_type="SETTING",
            resource_id=setting.id,
            status="SUCCESS",
            details={"key": setting_data.key, "setting_type": "SYSTEM"}
        )
        
        return SettingResponse.model_validate(setting)
    except Exception as e:
        log_audit(
            db=db,
            action="SETTING_CREATE",
            request=request,
            user_id=current_user.get("user_id"),
            user_email=current_user["sub"],
            status="FAILURE",
            details={"key": setting_data.key},
            error_message=str(e)
        )
        raise HTTPException(status_code=500, detail=f"Failed to create setting: {str(e)}")


@router.put("/system/{key}", response_model=SettingResponse)
@limiter.limit("20/minute")
async def update_system_setting(
    *,
    key: str,
    setting_data: SettingUpdate,
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Only admins can update system settings")
    
    try:
        setting_repo = SettingRepository(db)
        
        kwargs = {"key": key, "value": setting_data.value}
        if setting_data.category is not None:
            kwargs["category"] = setting_data.category
        if setting_data.description is not None:
            kwargs["description"] = setting_data.description
        if setting_data.is_public is not None:
            kwargs["is_public"] = setting_data.is_public
        
        setting = setting_repo.set_system_setting(**kwargs)
        
        log_audit(
            db=db,
            action="SETTING_UPDATE",
            request=request,
            user_id=current_user.get("user_id"),
            user_email=current_user["sub"],
            resource_type="SETTING",
            resource_id=setting.id,
            status="SUCCESS",
            details={"key": key, "setting_type": "SYSTEM"}
        )
        
        return SettingResponse.model_validate(setting)
    except Exception as e:
        log_audit(
            db=db,
            action="SETTING_UPDATE",
            request=request,
            user_id=current_user.get("user_id"),
            user_email=current_user["sub"],
            status="FAILURE",
            details={"key": key},
            error_message=str(e)
        )
        raise HTTPException(status_code=500, detail=f"Failed to update setting: {str(e)}")


@router.delete("/system/{key}")
@limiter.limit("10/minute")
async def delete_system_setting(
    *,
    key: str,
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Only admins can delete system settings")
    
    setting_repo = SettingRepository(db)
    success = setting_repo.delete_system_setting(key)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"Setting '{key}' not found")
    
    log_audit(
        db=db,
        action="SETTING_DELETE",
        request=request,
        user_id=current_user.get("user_id"),
        user_email=current_user["sub"],
        resource_type="SETTING",
        status="SUCCESS",
        details={"key": key, "setting_type": "SYSTEM"}
    )
    
    return {"message": "Setting deleted successfully", "key": key}


@router.get("/user/me", response_model=List[SettingResponse])
@limiter.limit("30/minute")
async def get_my_settings(
    request: Request,
    category: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token: user_id missing")
    
    setting_repo = SettingRepository(db)
    settings = setting_repo.get_all_user_settings(user_id=user_id, category=category)
    
    return [SettingResponse.model_validate(s) for s in settings]


@router.get("/user/me/{key}")
@limiter.limit("30/minute")
async def get_my_setting(
    key: str,
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token: user_id missing")
    
    setting_repo = SettingRepository(db)
    value = setting_repo.get_user_setting(user_id=user_id, key=key)
    
    if value is None:
        raise HTTPException(status_code=404, detail=f"Setting '{key}' not found")
    
    return {"key": key, "value": value}


@router.post("/user/me/{key}", response_model=SettingResponse)
@limiter.limit("20/minute")
async def set_my_setting(
    *,
    key: str,
    setting_data: SettingUpdate,
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token: user_id missing")
    
    try:
        setting_repo = SettingRepository(db)
        setting = setting_repo.set_user_setting(
            user_id=user_id,
            key=key,
            value=setting_data.value,
            category=setting_data.category,
            description=setting_data.description
        )
        
        log_audit(
            db=db,
            action="SETTING_UPDATE",
            request=request,
            user_id=user_id,
            user_email=current_user["sub"],
            resource_type="SETTING",
            resource_id=setting.id,
            status="SUCCESS",
            details={"key": key, "setting_type": "USER"}
        )
        
        return SettingResponse.model_validate(setting)
    except Exception as e:
        log_audit(
            db=db,
            action="SETTING_UPDATE",
            request=request,
            user_id=user_id,
            user_email=current_user["sub"],
            status="FAILURE",
            details={"key": key},
            error_message=str(e)
        )
        raise HTTPException(status_code=500, detail=f"Failed to set user setting: {str(e)}")


@router.delete("/user/me/{key}")
@limiter.limit("10/minute")
async def delete_my_setting(
    *,
    key: str,
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token: user_id missing")
    
    setting_repo = SettingRepository(db)
    success = setting_repo.delete_user_setting(user_id=user_id, key=key)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"Setting '{key}' not found")
    
    log_audit(
        db=db,
        action="SETTING_DELETE",
        request=request,
        user_id=user_id,
        user_email=current_user["sub"],
        resource_type="SETTING",
        status="SUCCESS",
        details={"key": key, "setting_type": "USER"}
    )
    
    return {"message": "Setting deleted successfully", "key": key}


@router.get("/public", response_model=List[SettingResponse])
@limiter.limit("50/minute")
async def get_public_settings(
    request: Request,
    db: Session = Depends(get_db)
):
    setting_repo = SettingRepository(db)
    settings = setting_repo.get_public_settings()
    
    return [SettingResponse.model_validate(s) for s in settings]
