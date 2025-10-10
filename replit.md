# JoxAI Banking Chatbot - Compressed replit.md

## Overview
The JoxAI Banking Chatbot is an AI-powered customer service solution for the banking sector, designed for production environments. It features a React-based admin panel, an embeddable chat widget, and a FastAPI backend. Its purpose is to handle customer inquiries, provide intelligent responses, and seamlessly escalate complex issues to human agents. The project is fully deployable to Replit Autoscale and ready for commercial use, aiming to revolutionize customer interaction in banking.

## User Preferences
I prefer simple language and clear explanations. I want iterative development with frequent, small updates. Ask before making major architectural changes or introducing new external dependencies. I prefer to use modern Python (3.11+) and JavaScript (ES6+) features where appropriate. Ensure all code is well-documented and follows best practices. Do not make changes to the folder `banking_chatbot/frontend/chat-widget/` unless explicitly instructed.

## System Architecture

### UI/UX Decisions
The project uses React for both the admin panel and the chat widget, focusing on a modern, responsive, and conversational user experience. The admin panel includes a dashboard, ticket management, and real-time updates for agents and supervisors.

### Technical Implementations
- **Backend**: FastAPI for high performance, asynchronous capabilities, API requests, WebSockets, and AI integrations.
- **Frontend**: React and Vite for the admin panel and an embeddable, lightweight chat widget.
- **Real-time Communication**: WebSockets for instant updates in the admin panel and chat widget.
- **Authentication**: JWT-based authentication with role-based access control (Admin, Supervisor, Agent), backed by PostgreSQL and bcrypt.
- **AI Capabilities**: Intelligent responses for banking inquiries (balance, credit cards, transfers) and smart escalation to human agents.
- **Data Storage**: PostgreSQL (Neon) with SQLAlchemy ORM and Alembic migrations, using a repository pattern for data access. Includes timestamp defaults for data integrity.
- **Security**: Rate limiting on critical endpoints, comprehensive audit logging (logins, ticket management, escalations) with independent database sessions, and centralized secrets management.
- **Knowledge Base Management**: Full CRUD system for banking knowledge articles, including full-text search, category filtering, and audit logging.
- **Customer Management (CRM)**: Comprehensive Customer model with full CRUD REST API, search/filter capabilities, soft-delete, and audit logging.
- **Settings Management**: Dynamic configuration system supporting SYSTEM (app-wide) and USER (per-user) settings with JSONB value storage, role-based access, and audit logging.
- **Analytics & Metrics**: Comprehensive system providing dashboard overview, conversation/ticket/customer statistics, agent performance, activity timelines, and audit statistics via REST API.
- **Notification System**: Multi-channel (EMAIL, SMS) notification infrastructure with database tracking, SMTP-based email service, and an extensible architecture.
- **WebSocket Real-time Updates**: JWT-authenticated WebSocket endpoint for live admin panel updates, targeted notification delivery, and connection statistics.
- **Automated Testing Suite**: Comprehensive test infrastructure with pytest: 8 passing unit tests (96% security coverage), 9 integration tests (auth, tickets, conversations APIs), 3 E2E workflow tests (chat-to-ticket, assignment, knowledge search). Complete test documentation and CI/CD ready.

### Feature Specifications
- **APIs**: Comprehensive RESTful APIs for Chat, Tickets, Conversations, Knowledge Base, Customer Management, Settings, Analytics, and Notifications.
- **WebSocket API**: Real-time updates with JWT authentication, role-based message routing, and automatic broadcasting of lifecycle events.
- **AI Chat**: Intelligent responses and smart escalation to human agents.
- **Admin Panel**: Dashboard, ticket management, real-time updates, and role-based views.
- **Chat Widget**: Conversational UI, real-time messaging, and escalation flow.

### System Design Choices
- **Microservice-oriented**: Clear separation between frontend applications (admin panel, chat widget) and a unified backend API.
- **API-first approach**: All functionalities exposed via well-defined RESTful APIs.
- **Scalability**: Designed for future scalability using FastAPI and React.
- **Deployment**: Configured for Replit Autoscale, serving the React frontend statically and the FastAPI backend (including WebSockets) from a single port.

## External Dependencies
- **FastAPI**: Python web framework.
- **React**: JavaScript library for UIs.
- **Vite**: Frontend build tool.
- **uvicorn**: ASGI server.
- **python-jose**: JWT library.
- **bcrypt**: Password hashing.
- **httpx**: Python HTTP client.
- **SQLAlchemy**: Python ORM.
- **Alembic**: Database migration tool.
- **PostgreSQL**: Relational database (Neon hosted).
- **slowapi**: Rate limiting for FastAPI.
- **Anthropic Claude API**: For AI conversational responses.
- **OpenAI GPT API**: For AI conversational responses.
- **wsproto**: WebSocket protocol implementation.
- **websockets**: WebSocket client library.