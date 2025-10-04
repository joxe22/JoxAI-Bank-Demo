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
  - Comprehensive audit logging system tracks all critical operations (logins, ticket management, conversation escalations) with full request metadata (IP, user-agent, endpoint, method). Audit logs use independent database sessions to ensure persistence even when main operations fail, maintaining complete security audit trails for compliance.

### Feature Specifications
- **Authentication**: Secure login, role-based access.
- **Chat API**: Initiate conversations, send messages, get AI responses, escalate to agents.
- **Tickets API**: CRUD operations for tickets, assignment, status/priority management, conversation history.
- **Conversations API**: Manage and view customer conversations.
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