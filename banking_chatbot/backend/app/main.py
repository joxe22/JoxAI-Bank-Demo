# backend/app/main.py
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.v1 import auth, tickets, conversations, chat, demo

app = FastAPI(title="Banking ChatBot API")

# Get the path to the frontend dist directory
FRONTEND_DIST = Path(__file__).parent.parent.parent / "frontend" / "admin-panel" / "dist"

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
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(tickets.router, prefix="/api/v1/tickets", tags=["tickets"])
app.include_router(conversations.router, prefix="/api/v1/conversations", tags=["conversations"])
app.include_router(demo.router, prefix="/api/v1/demo", tags=["demo"])

@app.get("/health")
def health():
    """Health check endpoint for API"""
    return {"status": "ok", "message": "Banking ChatBot API v1.0"}

@app.get("/widget-demo")
async def serve_widget_demo():
    """Serve the chat widget demo page"""
    widget_demo_path = Path(__file__).parent.parent.parent / "frontend" / "widget-demo.html"
    return FileResponse(str(widget_demo_path))

# Serve static files from frontend build (only if dist directory exists)
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="assets")
    
    @app.get("/")
    async def serve_frontend():
        """Serve the frontend index.html"""
        return FileResponse(str(FRONTEND_DIST / "index.html"))