# backend/app/schemas/auth.py
from pydantic import BaseModel

class Token(BaseModel):
    token: str
    user: dict

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
