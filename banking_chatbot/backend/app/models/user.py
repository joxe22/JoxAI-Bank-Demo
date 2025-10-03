# backend/app/models/user.py
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    role: str
    hashed_password: str = ""
    
    class Config:
        from_attributes = True
