# backend/app/api/v1/auth.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.core.security import verify_password, create_access_token, verify_token
from app.services.data_store import data_store

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(request: LoginRequest):
    """
    Login endpoint for admin panel
    """
    user = data_store.get_user_by_email(request.email)
    
    if not user or not verify_password(request.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    token = create_access_token(data={"sub": user["email"], "role": user["role"]})
    
    return {
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }

@router.get("/verify")
async def verify_token_endpoint(token: str):
    """Verify token endpoint"""
    try:
        payload = verify_token(token)
        email = payload.get("sub")
        
        if not email:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        user = data_store.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        
        return {
            "valid": True,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")
