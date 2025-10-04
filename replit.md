# JoxAI Banking Chatbot - Compressed replit.md

## Overview
The JoxAI Banking Chatbot is a comprehensive AI-powered customer service solution for the banking sector. It features a React-based admin panel, an embeddable chat widget, and a FastAPI backend. The system is designed to handle customer inquiries, provide intelligent responses, and seamlessly escalate complex issues to human agents. The project aims to improve customer support efficiency and satisfaction within banking operations.

## User Preferences
I prefer simple language and clear explanations. I want iterative development with frequent, small updates. Ask before making major architectural changes or introducing new external dependencies. I prefer to use modern Python (3.11+) and JavaScript (ES6+) features where appropriate. Ensure all code is well-documented and follows best practices. Do not make changes to the folder `banking_chatbot/frontend/chat-widget/` unless explicitly instructed.

## System Architecture

### UI/UX Decisions
The project utilizes React for both the admin panel and the chat widget, offering a modern, responsive, and conversational user interface. The admin panel provides a dashboard, ticket management, and real-time updates for agents and supervisors.

### Technical Implementations
- **Backend**: Built with FastAPI for high performance and asynchronous capabilities, handling API requests, WebSocket connections, and AI integrations.
- **Frontend**: Developed with React and Vite for a fast and efficient development experience, creating single-page applications for the admin panel and a lightweight, embeddable chat widget.
- **Real-time Communication**: Uses WebSockets for instant updates in the admin panel, such as new tickets or message notifications.
- **Authentication**: Implements JWT (JSON Web Token) based authentication with role-based access control (Admin, Supervisor, Agent). Users stored in PostgreSQL with bcrypt password hashing.
- **AI Capabilities**: The chatbot provides intelligent responses for banking-related inquiries (balance, credit cards, transfers, financial plans) and includes a smart escalation mechanism to human agents.
- **Data Storage**: PostgreSQL database (Neon) with SQLAlchemy ORM and Alembic migrations. All entities (users, conversations, messages, tickets) persist in database with repository pattern for data access.
- **Security**: 
  - Rate limiting implemented on critical endpoints (5/min for auth, 20/min for chat, 10/min for new conversations) using slowapi to prevent brute force attacks and API abuse.
  - Comprehensive audit logging system tracks all critical operations (logins, ticket management, conversation escalations, knowledge base modifications) with full request metadata (IP, user-agent, endpoint, method). Audit logs use independent database sessions to ensure persistence even when main operations fail, maintaining complete security audit trails for compliance.
  - Secrets management with centralized configuration and environment variables (no hardcoded keys).
- **Knowledge Base Management**: Full CRUD system for managing banking knowledge articles with PostgreSQL ARRAY support for tags, full-text search across title/content/tags, category filtering, and audit logging for all modifications (create, update, delete).
- **Customer Management (CRM)**: Complete customer relationship management with Customer model (full_name, email, phone, account_number, customer_type, status, preferences JSONB, tags ARRAY), full CRUD REST API, search/filter capabilities, soft-delete (status→INACTIVE), statistics endpoint, and comprehensive audit logging (CUSTOMER_CREATE, CUSTOMER_UPDATE, CUSTOMER_DELETE, CUSTOMER_VIEWED). JWT tokens include user_id for proper foreign key tracking.
- **Settings Management**: Dynamic configuration system with SYSTEM (app-wide) and USER (per-user) settings. JSONB value storage supports any data structure (AI models, business hours, user preferences, dashboard layouts). Role-based access: ADMIN/SUPERVISOR for system settings, authenticated users for their own settings, public settings accessible without authentication. Full CRUD REST API with audit logging and category organization.
- **Analytics & Metrics**: Comprehensive analytics system providing dashboard overview, conversation/ticket/customer statistics, agent performance metrics, activity timelines (daily aggregations), and audit statistics. REST API endpoints with configurable time periods, role-based access control, and optimized SQL queries with proper indexes for performance.
- **Notification System**: Multi-channel notification infrastructure supporting EMAIL and SMS delivery. Database tracking for all notifications (status, delivery attempts, timestamps), email service with SMTP configuration and professional HTML templates (ticket assigned, status changed, escalation alerts), notification repository for CRUD operations and batch processing, REST API for user notifications and admin statistics. Extensible architecture ready for future SMS/push notification integration.
- **WebSocket Real-time Updates**: Production-ready WebSocket infrastructure for live admin panel updates. JWT-authenticated WebSocket endpoint (/api/v1/ws) with role-based connection management (ADMIN, SUPERVISOR, AGENT), targeted notification delivery (ticket created/assigned/status changed, new messages, escalations), ping/pong keepalive, connection statistics monitoring, and automatic cleanup on disconnect. Integrated with all ticket operations for instant notifications to relevant users and roles.

### Feature Specifications
- **Authentication**: Secure login, role-based access (Admin, Supervisor, Agent).
- **Chat API**: Initiate conversations, send messages, get AI responses, escalate to agents.
- **Tickets API**: CRUD operations for tickets, assignment, status/priority management, conversation history.
- **Conversations API**: Manage and view customer conversations.
- **Knowledge Base API**: Complete REST API for managing knowledge articles (create, read, update, delete, search). Supports full-text search across title, content, and tags with category filtering. Authenticated endpoints for content management.
- **Customer Management API**: Full REST API for customer records (create, read, update, soft-delete, search, statistics). Supports filtering by status/type/agent, search by email/phone/account, pagination, and detailed customer profiles with preferences and tags.
- **Settings API**: REST endpoints for system, user, and public settings (GET/POST/PUT/DELETE). System settings require admin/supervisor role, user settings enforce JWT-based ownership, public settings accessible to all. Category filtering and flexible JSONB value storage.
- **Analytics API**: Dashboard metrics (GET /dashboard), conversation stats (GET /conversations?days=N), ticket stats (GET /tickets), agent performance (GET /agents/performance), customer stats (GET /customers), activity timeline (GET /timeline?days=N), and audit statistics (GET /audit?hours=N). All authenticated with rate limiting (30/min).
- **Notifications API**: User notifications (GET /me), notification details (GET /{id}), statistics (GET /stats, admin only), retry failed notifications (POST /{id}/retry, admin only). Supports filtering by category/status, ownership validation, and rate limiting (30/min).
- **WebSocket API**: Real-time updates endpoint (WS /api/v1/ws?token=JWT), connection statistics (GET /ws/stats). JWT authentication via query parameter, role-based message routing, ping/pong for keepalive, admin-only stats queries. Automatically broadcasts ticket lifecycle events (created, assigned, status changed) and new messages to connected clients based on their roles.
- **AI Chat**: Intelligent responses, smart escalation.
- **Admin Panel**: Login, dashboard, ticket management, real-time updates, role-based views.
- **Chat Widget**: Conversational UI, real-time messaging, escalation flow.

### System Design Choices
- **Microservice-oriented**: Clear separation between frontend applications (admin panel, chat widget) and a unified backend API.
- **API-first approach**: All functionalities are exposed via well-defined RESTful APIs.
- **Scalability**: Designed for future scalability with FastAPI and a component-based React architecture.
- **Deployment**: Configured for Replit Autoscale Deployment, serving the React frontend statically and the FastAPI backend, including WebSockets, from a single port (5000).

## External Dependencies
- **FastAPI**: Python web framework for the backend API.
- **React**: JavaScript library for building user interfaces.
- **Vite**: Frontend build tool for React applications.
- **uvicorn**: ASGI server for running FastAPI.
- **python-jose**: Python library for JWTs.
- **bcrypt**: Python library for secure password hashing.
- **httpx**: Python HTTP client.
- **SQLAlchemy**: Python SQL toolkit and ORM for database operations.
- **Alembic**: Database migration tool for SQLAlchemy.
- **PostgreSQL**: Production-grade relational database (Neon hosted).
- **slowapi**: Rate limiting library for FastAPI endpoints.
- **Anthropic Claude API**: For AI-powered conversational responses (configurable via environment variables).
- **OpenAI GPT API**: For AI-powered conversational responses (configurable via environment variables).
- **wsproto**: WebSocket protocol implementation for uvicorn server-side WebSocket support.
- **websockets**: WebSocket client library for testing and development.