# backend/app/main.py
import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.limiter import limiter
from app.api.v1 import auth, tickets, conversations, chat, demo, knowledge, customers, settings

app = FastAPI(title="Banking ChatBot API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
app.include_router(knowledge.router, prefix="/api/v1/knowledge", tags=["knowledge"])
app.include_router(customers.router, prefix="/api/v1/customers", tags=["customers"])
app.include_router(settings.router, prefix="/api/v1/settings", tags=["settings"])
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
    async def serve_frontend_root():
        """Serve the frontend index.html for root"""
        return FileResponse(str(FRONTEND_DIST / "index.html"))
    
    # Catch-all route for SPA (must be last!)
    # This allows React Router to handle all client-side routes
    @app.get("/{full_path:path}")
    async def serve_frontend_spa(full_path: str):
        """Serve index.html for all non-API routes (SPA support)"""
        # Skip if it's an API route (they're already handled above)
        if full_path.startswith("api/"):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="API endpoint not found")
        # Serve index.html for all other routes (SPA routing)
        return FileResponse(str(FRONTEND_DIST / "index.html"))