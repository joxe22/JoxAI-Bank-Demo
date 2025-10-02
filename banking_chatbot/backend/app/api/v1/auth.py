# backend/app/api/v1/auth.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core import security, database
from app.models.user import User
from app.schemas.auth import Token, UserResponse

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(database.get_db)
):
    """
    Login endpoint - usado por authService.login()

    Frontend espera:
    {
        "token": "jwt_token_here",
        "user": {
            "id": 1,
            "name": "Admin User",
            "email": "admin@banco.com",
            "role": "admin"
        }
    }
    """
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = security.create_access_token(data={"sub": user.email, "role": user.role})

    return {
        "token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }

@router.get("/verify")
async def verify_token(current_user: User = Depends(security.get_current_user)):
    """Verifica si el token es válido"""
    return {"valid": True, "user": current_user}