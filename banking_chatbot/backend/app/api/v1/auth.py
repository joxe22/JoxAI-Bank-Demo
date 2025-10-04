# backend/app/api/v1/auth.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token, verify_token
from app.database import get_db
from app.repositories import UserRepository

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login endpoint for admin panel.
    Now uses PostgreSQL instead of in-memory data_store.
    """
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(request.email)
    
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    token = create_access_token(data={"sub": user.email, "role": user.role.value})
    
    return {
        "token": token,
        "user": {
            "id": user.id,
            "name": user.full_name,
            "email": user.email,
            "role": user.role.value
        }
    }

@router.get("/verify")
async def verify_token_endpoint(token: str, db: Session = Depends(get_db)):
    """
    Verify token endpoint.
    Now uses PostgreSQL instead of in-memory data_store.
    """
    try:
        payload = verify_token(token)
        email = payload.get("sub")
        
        if not email:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        user_repo = UserRepository(db)
        user = user_repo.get_by_email(email)
        
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        
        return {
            "valid": True,
            "user": {
                "id": user.id,
                "name": user.full_name,
                "email": user.email,
                "role": user.role.value
            }
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")
