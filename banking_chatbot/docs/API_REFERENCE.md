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
  "user_id": "customer_12345",
  "metadata": {
    "email": "customer@example.com"
  }
}
```

**Response (200 OK):**
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "started",
  "messages": [
    {
      "id": 1,
      "role": "assistant",
      "content": "¡Hola! Soy el asistente virtual de JoxAI Bank. ¿En qué puedo ayudarte hoy?",
      "timestamp": "2025-10-10T10:30:00Z"
    }
  ]
}
```

### Send Message
```http
POST /chat/message
```

**Request:**
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "What is my account balance?",
  "context": {}
}
```

**Response (200 OK):**
```json
{
  "message": "I'd be happy to help you check your balance. To access your account information, I'll need to verify your identity first...",
  "metadata": {},
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Escalate to Human Agent
```http
POST /chat/escalate
```

**Request:**
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "category": "account_inquiry",
  "priority": "medium",
  "description": "Customer needs account assistance",
  "metadata": {}
}
```

**Response (200 OK):**
```json
{
  "message": "Conversation escalated to human agent",
  "ticket_id": "TKT-A1B2C3D4",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
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
  "customer_name": "Jane Smith",
  "status": "OPEN",
  "priority": "HIGH",
  "created_at": "2025-10-10T11:00:00Z"
}
```

**Note:** Priority values can be sent in lowercase (`"low"`, `"medium"`, `"high"`, `"urgent"`) and will be automatically converted to uppercase enums.

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
  "status": "resolved"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "ticket_id": "TKT-A1B2C3D4",
  "status": "RESOLVED",
  "assigned_to": 5
}
```

**Note:** Status values (`"open"`, `"in_progress"`, `"resolved"`, `"closed"`) are case-insensitive and will be converted to uppercase.

### Update Ticket Priority
```http
PATCH /tickets/{ticket_id}/priority
Authorization: Bearer {token}
```

**Request:**
```json
{
  "priority": "high"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "ticket_id": "TKT-A1B2C3D4",
  "priority": "HIGH"
}
```

**Note:** Priority values are case-insensitive (`"low"`, `"medium"`, `"high"`, `"urgent"`).

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

## Customers API

### List Customers
```http
GET /customers
Authorization: Bearer {token}
```

**Query Parameters:**
- `skip` (default: 0): Pagination offset
- `limit` (default: 100, max: 500): Number of results
- `status`: Filter by customer status (ACTIVE, INACTIVE, SUSPENDED)
- `customer_type`: Filter by type (INDIVIDUAL, BUSINESS)
- `assigned_agent_id`: Filter by assigned agent

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "account_number": "ACC-123456",
    "customer_type": "INDIVIDUAL",
    "status": "ACTIVE",
    "preferences": {},
    "tags": ["premium", "vip"],
    "notes": "Preferred customer",
    "assigned_agent_id": 5,
    "created_by_id": 1,
    "updated_by_id": 1,
    "created_at": "2025-10-01T00:00:00Z",
    "updated_at": "2025-10-10T10:00:00Z"
  }
]
```

### Create Customer
```http
POST /customers
Authorization: Bearer {token}
```

**Request:**
```json
{
  "full_name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "+1234567890",
  "account_number": "ACC-789012",
  "customer_type": "INDIVIDUAL",
  "status": "ACTIVE",
  "preferences": {"language": "en"},
  "tags": ["new"],
  "notes": "New customer from referral",
  "assigned_agent_id": 5
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "full_name": "Jane Smith",
  "email": "jane@example.com",
  "customer_type": "INDIVIDUAL",
  "status": "ACTIVE",
  "created_at": "2025-10-10T11:00:00Z"
}
```

### Search Customers
```http
GET /customers/search?q={query}
Authorization: Bearer {token}
```

**Query Parameters:**
- `q` (required): Search query (name, email, phone, account number, tags)
- `status`: Filter by status
- `customer_type`: Filter by type
- `skip`, `limit`: Pagination

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "full_name": "John Doe",
    "email": "john@example.com",
    "...": "..."
  }
]
```

### Update Customer
```http
PUT /customers/{customer_id}
Authorization: Bearer {token}
```

**Request:**
```json
{
  "full_name": "John Doe Updated",
  "phone": "+0987654321",
  "status": "ACTIVE",
  "tags": ["premium", "vip", "loyal"]
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "full_name": "John Doe Updated",
  "updated_at": "2025-10-10T12:00:00Z"
}
```

### Delete Customer (Soft Delete)
```http
DELETE /customers/{customer_id}
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "message": "Customer deactivated successfully",
  "customer_id": 1
}
```

---

## Notifications API

### Get My Notifications
```http
GET /notifications/me
Authorization: Bearer {token}
```

**Query Parameters:**
- `category`: Filter by category (TICKET, CONVERSATION, SYSTEM, REMINDER)
- `status`: Filter by status (PENDING, SENT, FAILED, CANCELLED)
- `limit` (default: 50, max: 200): Number of notifications

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "user_id": 5,
    "recipient_email": "agent@joxaibank.com",
    "notification_type": "EMAIL",
    "category": "TICKET",
    "status": "SENT",
    "subject": "New Ticket Assigned",
    "body": "You have been assigned ticket TKT-A1B2C3D4",
    "resource_type": "ticket",
    "resource_id": "TKT-A1B2C3D4",
    "sent_at": 1728564000,
    "delivery_attempts": 1,
    "error_message": null,
    "created_at": "2025-10-10T10:30:00Z",
    "updated_at": "2025-10-10T10:30:00Z"
  }
]
```

### Get Notification by ID
```http
GET /notifications/{notification_id}
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": 5,
  "notification_type": "EMAIL",
  "category": "TICKET",
  "status": "SENT",
  "subject": "New Ticket Assigned",
  "body": "You have been assigned ticket TKT-A1B2C3D4",
  "created_at": "2025-10-10T10:30:00Z"
}
```

### Retry Failed Notification (Admin/Supervisor only)
```http
POST /notifications/{notification_id}/retry
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "message": "Notification queued for retry",
  "notification_id": 1
}
```

### Get Notification Statistics (Admin/Supervisor only)
```http
GET /notifications/stats
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "total": 1250,
  "pending": 15,
  "sent": 1200,
  "failed": 35,
  "by_type": {
    "EMAIL": 1100,
    "SMS": 150
  },
  "by_category": {
    "TICKET": 800,
    "CONVERSATION": 300,
    "SYSTEM": 150
  }
}
```

---

## Settings API

### Get System Settings (Admin/Supervisor only)
```http
GET /settings/system
Authorization: Bearer {token}
```

**Query Parameters:**
- `category` (optional): Filter by category

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "key": "app_name",
    "value": "JoxAI Banking Chatbot",
    "setting_type": "SYSTEM",
    "user_id": null,
    "category": "general",
    "description": "Application display name",
    "is_public": true,
    "created_at": "2025-10-01T00:00:00Z",
    "updated_at": "2025-10-10T00:00:00Z"
  }
]
```

### Get System Setting by Key (Admin/Supervisor only)
```http
GET /settings/system/{key}
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "key": "app_name",
  "value": "JoxAI Banking Chatbot"
}
```

### Create System Setting (Admin only)
```http
POST /settings/system
Authorization: Bearer {token}
```

**Request:**
```json
{
  "key": "max_tickets_per_agent",
  "value": 10,
  "category": "limits",
  "description": "Maximum tickets per agent",
  "is_public": false
}
```

**Response (201 Created):**
```json
{
  "id": 5,
  "key": "max_tickets_per_agent",
  "value": 10,
  "setting_type": "SYSTEM",
  "category": "limits",
  "is_public": false,
  "created_at": "2025-10-10T11:00:00Z"
}
```

### Update System Setting (Admin only)
```http
PUT /settings/system/{key}
Authorization: Bearer {token}
```

**Request:**
```json
{
  "value": 15,
  "description": "Updated maximum tickets per agent"
}
```

**Response (200 OK):**
```json
{
  "id": 5,
  "key": "max_tickets_per_agent",
  "value": 15,
  "updated_at": "2025-10-10T12:00:00Z"
}
```

### Delete System Setting (Admin only)
```http
DELETE /settings/system/{key}
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "message": "Setting deleted successfully",
  "key": "max_tickets_per_agent"
}
```

### Get My User Settings
```http
GET /settings/user/me
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
[
  {
    "id": 10,
    "key": "theme",
    "value": "dark",
    "setting_type": "USER",
    "user_id": 5,
    "category": "appearance",
    "description": "User theme preference",
    "created_at": "2025-10-10T10:00:00Z"
  }
]
```

### Set User Setting
```http
POST /settings/user/me/{key}
Authorization: Bearer {token}
```

**Request:**
```json
{
  "value": "dark",
  "category": "appearance"
}
```

**Response (200 OK):**
```json
{
  "id": 10,
  "key": "theme",
  "value": "dark",
  "setting_type": "USER",
  "user_id": 5
}
```

### Get Public Settings (No auth required)
```http
GET /settings/public
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "key": "app_name",
    "value": "JoxAI Banking Chatbot",
    "is_public": true
  }
]
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
