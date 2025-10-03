# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, tickets, conversations

app = FastAPI(title="Banking ChatBot API")

# CORS para admin-panel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(tickets.router, prefix="/api/v1/tickets", tags=["tickets"])
app.include_router(conversations.router, prefix="/api/v1/conversations", tags=["conversations"])

@app.get("/")
def root():
    return {"message": "Banking ChatBot API v1.0"}