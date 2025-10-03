# JoxAI Banking Chatbot - Replit Setup

## Overview
A banking chatbot application with AI/RAG capabilities, featuring a React admin panel and FastAPI backend.

## Project Structure
- **Frontend**: React admin panel in `banking_chatbot/frontend/admin-panel/`
- **Backend**: FastAPI server in `banking_chatbot/backend/`
- **Port Configuration**:
  - Frontend (dev): Port 5000 (configured for Replit proxy)
  - Backend (dev): Port 8000 (localhost only)
  - Production: Port 5000 (serves both frontend static files and API)

## Current Setup Status

### Installed Dependencies
- **Python 3.11**: Core backend dependencies (FastAPI, uvicorn, SQLAlchemy, pydantic, python-jose, passlib, httpx)
- **Node.js 20**: Frontend dependencies (React, react-dom, react-router-dom, Vite)

### Configured Workflows
1. **Backend API**: FastAPI server running on localhost:8000
2. **Frontend**: Vite dev server running on 0.0.0.0:5000

### Configuration Changes Made
1. **Vite Config**: Configured to accept all hosts and HMR for Replit proxy
2. **Backend CORS**: Set to allow all origins for development
3. **Deployment**: Configured autoscale deployment that builds frontend and serves via backend

## Development

### Running Locally
Both workflows are configured and running:
- Frontend: http://localhost:5000 (what users see)
- Backend API: http://localhost:8000/docs (FastAPI docs)

### Building for Production
```bash
cd banking_chatbot/frontend/admin-panel && npm run build
```

## Deployment
The deployment is configured to:
1. Build the frontend using npm
2. Serve the built static files and API endpoints via uvicorn on port 5000

## Notes
- Backend has minimal stub implementations for models and services
- Database integration is not yet fully configured
- Additional Python dependencies (LLM, NLP libraries) not installed to reduce complexity
- The app shows a login page - default credentials: admin@joxai.com / admin123

## Next Steps
To fully implement the chatbot:
1. Set up a PostgreSQL database using Replit's database tools
2. Install additional AI/ML dependencies (langchain, openai, anthropic, etc.)
3. Implement the RAG (Retrieval Augmented Generation) engine
4. Add the chat widget component
5. Configure authentication with real user management

## Architecture
- FastAPI backend serves both API endpoints (under `/api/v1/`) and static frontend files
- React SPA with routing for different admin panel views
- WebSocket support for real-time updates (conversations endpoint)

---
Last updated: October 3, 2025
