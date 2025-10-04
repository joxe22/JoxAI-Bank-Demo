# JoxAI Banking Chatbot - Complete Integration

## Overview
A fully integrated banking chatbot application with AI capabilities, featuring a React admin panel, chat widget, and FastAPI backend. The chatbot can handle customer inquiries and escalate to human agents when needed.

## Project Structure
- **Backend API**: FastAPI server in `banking_chatbot/backend/`
- **Admin Panel**: React admin interface in `banking_chatbot/frontend/admin-panel/`
- **Chat Widget**: Embeddable widget in `banking_chatbot/frontend/chat-widget/`
- **Demo Page**: Widget demo at `banking_chatbot/frontend/widget-demo.html`

## Port Configuration
- **Frontend (dev)**: Port 5000 (configured for Replit proxy)
- **Backend (dev)**: Port 8000 (localhost only)
- **Production**: Port 5000 (unified deployment)

## Features Implemented

### ✅ Backend API (FastAPI)
- **Authentication**: Login with JWT tokens, role-based access (admin, supervisor, agent)
- **Chat API**: Start conversations, send messages, get AI responses, escalate to agents
- **Tickets API**: Full CRUD, assignment, status/priority management, conversation history
- **Conversations API**: View and manage all customer conversations
- **WebSocket**: Real-time updates for admin panel (new tickets, status changes, messages)
- **Demo API**: Endpoints to populate and clear demo data for testing

### ✅ AI Chat Capabilities
The chatbot provides intelligent responses about:
- **💰 Balance Inquiries**: Account balance and transaction history
- **💳 Credit Cards**: Recommendations based on customer needs
- **🔄 Transfers**: Step-by-step guidance for SPEI and traditional transfers
- **💼 Financial Plans**: Savings and investment options
- **🤝 Agent Escalation**: Smart escalation when human help is needed

### ✅ Admin Panel Features
- **Login System**: Secure authentication with JWT
- **Dashboard**: Overview of tickets, conversations, and metrics
- **Tickets View**: Manage escalated conversations with full history
- **Real-time Updates**: WebSocket integration for live ticket notifications
- **Role-based Access**: Different views for admin, supervisor, agent

### ✅ Chat Widget
- **Conversational UI**: Modern chat interface with typing indicators
- **Real-time Messaging**: Instant responses from AI assistant
- **Escalation Flow**: Seamless handoff to human agents
- **Demo Page**: Standalone demo at http://localhost:8000/widget-demo

## Quick Start

### Access Points
1. **Admin Panel**: http://localhost:5000/
   - Login: admin@joxai.com / admin123
   - Or: agent@joxai.com / admin123
   - Or: supervisor@joxai.com / admin123

2. **Widget Demo**: http://localhost:8000/widget-demo
   - Interactive chat widget demonstration
   - Test AI responses and escalation

3. **API Docs**: http://localhost:8000/docs
   - Interactive FastAPI documentation
   - Test all endpoints directly

### Demo Data
Populate test data with:
```bash
curl -X POST http://localhost:8000/api/v1/demo/populate-demo-data
```

This creates:
- 5 sample conversations
- 3 escalated tickets (open, assigned, in-progress)
- Sample messages and conversation history

Clear demo data with:
```bash
curl -X POST http://localhost:8000/api/v1/demo/clear-demo-data
```

## Development

### Installed Dependencies
- **Python 3.11**: FastAPI, uvicorn, pydantic, python-jose, passlib, httpx
- **Node.js 20**: React, react-dom, react-router-dom, Vite

### Running Workflows
Both workflows are configured and running:
- **Backend API**: FastAPI on localhost:8000
- **Frontend**: Vite dev server on 0.0.0.0:5000

### API Endpoints

#### Authentication
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/verify` - Verify token validity

#### Chat (Widget Integration)
- `POST /api/v1/chat/start` - Start new conversation
- `POST /api/v1/chat/message` - Send message and get AI response
- `POST /api/v1/chat/escalate` - Escalate to human agent (creates ticket)
- `GET /api/v1/chat/history/{id}` - Get conversation history
- `GET /api/v1/chat/config` - Get widget configuration

#### Tickets (Admin Panel)
- `GET /api/v1/tickets` - List all tickets (with filters)
- `GET /api/v1/tickets/{id}` - Get ticket details
- `POST /api/v1/tickets` - Create new ticket
- `PUT /api/v1/tickets/{id}` - Update ticket
- `POST /api/v1/tickets/{id}/assign` - Assign to agent
- `PATCH /api/v1/tickets/{id}/status` - Change status
- `POST /api/v1/tickets/{id}/messages` - Add message to ticket
- `GET /api/v1/tickets/statistics` - Get ticket statistics

#### Conversations
- `GET /api/v1/conversations` - List all conversations
- `GET /api/v1/conversations/{id}` - Get conversation with messages
- `WS /api/v1/conversations/ws/admin` - WebSocket for real-time updates

#### Demo
- `POST /api/v1/demo/populate-demo-data` - Create test data
- `POST /api/v1/demo/clear-demo-data` - Clear all data
- `GET /api/v1/demo/stats` - Get data statistics

## Integration Flow

### Customer → Chatbot → Agent
1. **Customer** opens chat widget on website
2. **AI Chatbot** answers questions about banking services
3. **Smart Escalation** when chatbot detects need for human assistance
4. **Ticket Creation** with full conversation history
5. **Real-time Notification** to admin panel via WebSocket
6. **Agent Assignment** and response through admin panel
7. **Conversation History** preserved and accessible

## Technical Architecture

### Data Flow
```
Chat Widget → Backend API → Data Store → WebSocket → Admin Panel
     ↑                                           ↓
     └────────── Ticket Escalation ─────────────┘
```

### Components
- **In-Memory Data Store**: Stores conversations, tickets, users for demo
- **WebSocket Manager**: Real-time bidirectional communication
- **JWT Authentication**: Secure token-based auth
- **Role-Based Access**: Different permissions for admin/supervisor/agent

## Deployment

### ✅ Configuración de Despliegue Completada

El proyecto está configurado para **Replit Autoscale Deployment**:

1. **Build Process**: Construye el frontend de React con Vite
   - Comando: `cd banking_chatbot/frontend/admin-panel && npm install && npm run build`
   - Genera archivos estáticos en `dist/`

2. **Run Process**: Sirve la aplicación completa desde FastAPI
   - Comando: `cd banking_chatbot/backend && uvicorn app.main:app --host 0.0.0.0 --port 5000`
   - Puerto 5000 (requerido por Replit)
   - Sirve frontend estático + API + WebSocket

3. **Deployment Type**: Autoscale
   - Escala automáticamente según el tráfico
   - Solo paga cuando hay requests
   - Ideal para aplicaciones web con tráfico variable

### 📦 Qué Incluye el Despliegue

- ✅ Admin Panel (React SPA)
- ✅ Chat Widget Demo
- ✅ API REST completa
- ✅ WebSocket para actualizaciones en tiempo real
- ✅ Autenticación JWT
- ✅ Sistema de tickets y conversaciones

### 🚀 Cómo Publicar

1. Haz clic en el botón **"Deploy"** en la parte superior de Replit
2. Selecciona **"Autoscale"** como tipo de despliegue
3. Revisa la configuración (ya está preconfigurada)
4. Haz clic en **"Deploy"** para publicar

Tu aplicación estará disponible en una URL pública de Replit en pocos minutos.

## Users
- **Admin**: admin@joxai.com / admin123 - Full access
- **Supervisor**: supervisor@joxai.com / admin123 - Manage agents
- **Agent**: agent@joxai.com / admin123 - Handle tickets

## Next Steps for Production

### Database Integration
Replace in-memory store with:
- PostgreSQL for structured data (users, tickets, conversations)
- Redis for sessions and caching
- Vector DB (Qdrant/Milvus) for RAG embeddings

### AI Integration
- Connect to OpenAI/Anthropic/Claude API
- Implement RAG (Retrieval Augmented Generation) with vector search
- Add NLU for intent classification and entity extraction
- Train on banking knowledge base

### Banking Integration
- Connect to Core Banking APIs
- Implement secure authentication flow
- Add transaction capabilities
- PII detection and redaction

### Security Enhancements
- Implement proper password hashing with salt
- Add rate limiting
- Enable HTTPS/TLS
- Add audit logging
- Implement data encryption

### Features to Add
- File upload support
- Voice input/output
- Multi-language support
- Advanced analytics dashboard
- A/B testing framework
- CSAT/NPS collection

---
Last updated: October 4, 2025

**Status**: ✅ Full integration complete - All core features working
**Mode**: Demo/Development (in-memory storage)

## Recent Fixes (October 4, 2025)

### URLs & Connectivity
- Fixed dynamic URL detection for API and WebSocket in frontend
- Changed URLs to auto-detect production vs development environments
- Fixed WebSocket endpoint path to `/api/v1/conversations/ws/admin`
- Widget-demo.html now uses dynamic URL detection

### Configuration
- Fixed Pydantic config types: `CORS_ORIGINS` and `ALLOWED_FILE_TYPES` now use `List[str]`
- Cleaned up `requirements.txt` to include only necessary dependencies
- Removed unused dependencies that caused compilation errors in Python 3.13

### Testing Status
- ✅ Authentication working (Admin, Agent, Supervisor roles)
- ✅ Chat API working (start conversation, send messages)
- ✅ Escalation working (chat → ticket creation)
- ✅ Tickets API working (CRUD operations) - **Note: Use trailing slash in URL**
- ✅ Conversations API working (list and details)
- ✅ Widget-demo accessible and functional
- ✅ Frontend build successful with dynamic URLs
- ✅ Demo data population working correctly

### API Endpoint Notes
- Always use trailing slashes for list endpoints (e.g., `/api/v1/tickets/`, not `/api/v1/tickets`)
- FastAPI will return 307 redirect if trailing slash is missing
- Frontend automatically handles this, but important for direct API testing
