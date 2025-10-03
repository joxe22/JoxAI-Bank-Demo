# backend/app/api/v1/auth.py
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/login")
async def login(credentials: dict):
    """
    Minimal login endpoint for testing
    """
    return {
        "token": "test-jwt-token",
        "user": {
            "id": 1,
            "name": "Test User",
            "email": "test@example.com",
            "role": "admin"
        }
    }

@router.get("/verify")
async def verify_token():
    """Verify token endpoint"""
    return {"valid": True, "user": {"id": 1, "name": "Test User"}}
