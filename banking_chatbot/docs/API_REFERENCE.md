# JoxAI Banking Chatbot - API Reference

## Overview

Complete REST API documentation for the JoxAI Banking Chatbot system. All endpoints require authentication unless otherwise specified.

**Base URL:** `https://your-app.replit.app/api/v1`

## Authentication

### Login
```http
POST /auth/login
```

**Request:**
```json
{
  "username": "agent@joxaibank.com",
  "password": "your-password"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "agent@joxaibank.com",
    "email": "agent@joxaibank.com",
    "full_name": "John Agent",
    "role": "AGENT"
  }
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Incorrect username or password"
}
```

### Get Current User
```http
GET /auth/me
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "agent@joxaibank.com",
  "email": "agent@joxaibank.com",
  "full_name": "John Agent",
  "role": "AGENT"
}
```

---

## Chat API

### Start Conversation
```http
POST /chat/start
```

**Request:**
```json
{
  "user_id": "customer_12345"
}
```

**Response (200 OK):**
```json
{
  "conversation_id": "conv_abc123",
  "message": "Chat session started successfully",
  "status": "ACTIVE"
}
```

### Send Message
```http
POST /chat/message
```

**Request:**
```json
{
  "conversation_id": "conv_abc123",
  "message": "What is my account balance?"
}
```

**Response (200 OK):**
```json
{
  "response": "I'd be happy to help you check your balance. To access your account information, I'll need to verify your identity first...",
  "conversation_id": "conv_abc123",
  "should_escalate": false
}
```

### Escalate to Human Agent
```http
POST /chat/escalate
```

**Request:**
```json
{
  "conversation_id": "conv_abc123",
  "reason": "Customer needs account assistance"
}
```

**Response (200 OK):**
```json
{
  "message": "Conversation escalated successfully",
  "ticket_id": "TKT-A1B2C3D4",
  "conversation_id": "conv_abc123"
}
```

---

## Tickets API

### List Tickets
```http
GET /tickets
Authorization: Bearer {token}
```

**Query Parameters:**
- `status` (optional): Filter by status (OPEN, IN_PROGRESS, RESOLVED, CLOSED)
- `priority` (optional): Filter by priority (LOW, MEDIUM, HIGH, URGENT)
- `assigned_to` (optional): Filter by agent ID

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "ticket_id": "TKT-A1B2C3D4",
    "customer_name": "John Doe",
    "subject": "Account Balance Inquiry",
    "status": "OPEN",
    "priority": "MEDIUM",
    "assigned_to": null,
    "created_at": "2025-10-10T10:30:00Z"
  }
]
```

### Get Ticket Details
```http
GET /tickets/{ticket_id}
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "ticket_id": "TKT-A1B2C3D4",
  "conversation_id": "conv_abc123",
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "subject": "Account Balance Inquiry",
  "description": "Customer wants to check account balance",
  "status": "OPEN",
  "priority": "MEDIUM",
  "category": "account_inquiry",
  "assigned_to": null,
  "assigned_to_name": null,
  "created_at": "2025-10-10T10:30:00Z",
  "updated_at": "2025-10-10T10:30:00Z"
}
```

### Create Ticket
```http
POST /tickets
Authorization: Bearer {token}
```

**Request:**
```json
{
  "subject": "Manual Support Ticket",
  "description": "Customer called requesting help",
  "priority": "high",
  "category": "general",
  "customer_name": "Jane Smith",
  "customer_email": "jane@example.com"
}
```

**Response (200 OK):**
```json
{
  "id": 2,
  "ticket_id": "TKT-B2C3D4E5",
  "status": "OPEN",
  "priority": "HIGH",
  "created_at": "2025-10-10T11:00:00Z"
}
```

### Assign Ticket
```http
POST /tickets/{ticket_id}/assign
Authorization: Bearer {token}
```

**Request:**
```json
{
  "agentId": 5
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "ticket_id": "TKT-A1B2C3D4",
  "assigned_to": 5,
  "assigned_to_name": "Agent Smith",
  "status": "IN_PROGRESS"
}
```

### Update Ticket Status
```http
PATCH /tickets/{ticket_id}/status
Authorization: Bearer {token}
```

**Request:**
```json
{
  "status": "RESOLVED",
  "resolution_notes": "Issue resolved - customer balance provided"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "ticket_id": "TKT-A1B2C3D4",
  "status": "RESOLVED",
  "updated_at": "2025-10-10T12:00:00Z"
}
```

### Update Ticket Priority
```http
PATCH /tickets/{ticket_id}/priority
Authorization: Bearer {token}
```

**Request:**
```json
{
  "priority": "HIGH"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "ticket_id": "TKT-A1B2C3D4",
  "priority": "HIGH",
  "updated_at": "2025-10-10T11:30:00Z"
}
```

---

## Knowledge Base API

### Search Articles
```http
GET /knowledge/search
Authorization: Bearer {token}
```

**Query Parameters:**
- `q` (required): Search query
- `category` (optional): Filter by category

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "How to Reset Your Password",
    "content": "To reset your password: 1. Click 'Forgot Password'...",
    "category": "account_management",
    "tags": ["password", "reset", "security"],
    "is_active": true,
    "created_at": "2025-10-01T00:00:00Z"
  }
]
```

### Create Article
```http
POST /knowledge
Authorization: Bearer {token}
```

**Request:**
```json
{
  "title": "Transfer Money Between Accounts",
  "content": "To transfer money: 1. Log in to your account...",
  "category": "transfers",
  "tags": ["transfer", "money", "accounts"]
}
```

**Response (201 Created):**
```json
{
  "id": 5,
  "title": "Transfer Money Between Accounts",
  "category": "transfers",
  "is_active": true,
  "created_at": "2025-10-10T13:00:00Z"
}
```

---

## Analytics API

### Dashboard Overview
```http
GET /analytics/dashboard
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "total_conversations": 1250,
  "active_conversations": 45,
  "total_tickets": 320,
  "open_tickets": 28,
  "in_progress_tickets": 12,
  "resolved_today": 15,
  "avg_response_time_minutes": 8.5,
  "customer_satisfaction": 4.6
}
```

### Conversation Statistics
```http
GET /analytics/conversations?days=7
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "total": 450,
  "active": 45,
  "escalated": 89,
  "avg_messages_per_conversation": 5.2,
  "escalation_rate": 0.198
}
```

---

## WebSocket API

### Connect to WebSocket
```
WS /ws?token={jwt_token}
```

**Connection Example (JavaScript):**
```javascript
const token = localStorage.getItem('token');
const ws = new WebSocket(`wss://your-app.replit.app/api/v1/ws?token=${token}`);

ws.onopen = () => {
  console.log('WebSocket connected');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

**Message Types:**
- `ticket_created` - New ticket created
- `ticket_assigned` - Ticket assigned to agent
- `ticket_status_changed` - Ticket status updated
- `new_message` - New message in conversation

**Example Message:**
```json
{
  "type": "ticket_assigned",
  "ticket_id": "TKT-A1B2C3D4",
  "assigned_to": 5,
  "assigned_to_name": "Agent Smith"
}
```

---

## Rate Limiting

Rate limits are enforced to ensure fair usage:

| Endpoint | Limit |
|----------|-------|
| `/auth/login` | 5 requests/minute |
| `/chat/*` | 20 requests/minute |
| `/tickets/*` | 30 requests/minute |
| `/analytics/*` | 30 requests/minute |

**Rate Limit Response (429):**
```json
{
  "detail": "Rate limit exceeded. Try again in 60 seconds."
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Invalid or missing token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found |
| 422 | Validation Error |
| 429 | Rate Limit Exceeded |
| 500 | Internal Server Error |

**Error Response Format:**
```json
{
  "detail": "Error message description"
}
```

---

## Pagination

List endpoints support pagination:

**Query Parameters:**
- `skip` (default: 0): Number of records to skip
- `limit` (default: 100): Maximum records to return

**Example:**
```http
GET /tickets?skip=0&limit=50
```

---

## Best Practices

1. **Always use HTTPS** in production
2. **Store tokens securely** (httpOnly cookies or secure storage)
3. **Refresh tokens** before expiration
4. **Handle rate limits** with exponential backoff
5. **Validate input** on client side before sending
6. **Use WebSockets** for real-time updates
7. **Implement error handling** for all API calls

---

**API Version:** 1.0.0  
**Last Updated:** October 10, 2025
