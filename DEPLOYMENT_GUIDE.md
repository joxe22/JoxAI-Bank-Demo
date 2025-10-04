# JoxAI Banking Chatbot - Production Deployment Guide

## 🚀 Deployment Overview

The JoxAI Banking Chatbot is production-ready and configured for **Replit Autoscale Deployment**. This guide covers everything needed to deploy the system to production.

---

## ✅ Pre-Deployment Checklist

### 1. Required Environment Variables

Before deploying, ensure these secrets are configured in Replit Secrets:

#### **Critical (Required)**
- `DATABASE_URL` - PostgreSQL connection string (auto-provided by Replit)
- `SECRET_KEY` - Strong random string for JWT signing (min 32 characters)
  - Generate: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- `ANTHROPIC_API_KEY` **OR** `OPENAI_API_KEY` - AI provider API key
  - Get Anthropic key: https://console.anthropic.com/
  - Get OpenAI key: https://platform.openai.com/api-keys
  - **⚠️ IMPORTANT**: Ensure your AI account has sufficient credits

#### **Recommended (Optional)**
- `SMTP_HOST` - Email server (e.g., smtp.gmail.com)
- `SMTP_PORT` - Email port (e.g., 587)
- `SMTP_USER` - Email username
- `SMTP_PASSWORD` - Email password
- `FROM_EMAIL` - Sender email address
- `FROM_NAME` - Sender name (e.g., "JoxAI Banking Chatbot")

#### **Optional Configuration**
- `AI_PROVIDER` - Choose "anthropic" or "openai" (default: auto-detect)
- `ACCESS_TOKEN_EXPIRE_HOURS` - JWT expiration time (default: 720 hours)
- `CORS_ORIGINS` - Comma-separated allowed origins

### 2. Database Setup

The PostgreSQL database is automatically configured by Replit. Ensure:
- ✅ Database is created (check Replit Database tab)
- ✅ All migrations are up to date
- ✅ Default admin user exists (auto-created on first run)

**Default Admin Credentials:**
- Email: `admin@joxai.com`
- Password: `admin123`
- **⚠️ Change this password immediately after first login!**

### 3. Frontend Build

The deployment automatically builds the React admin panel:
```bash
cd banking_chatbot/frontend/admin-panel && npm install && npm run build
```

This is handled automatically during deployment via the build configuration.

---

## 🔧 Deployment Configuration

### Current Setup (.replit)

```toml
[deployment]
deploymentTarget = "autoscale"

# Build step - compiles React frontend
build = ["bash", "-c", "cd banking_chatbot/frontend/admin-panel && npm install && npm run build"]

# Run step - starts production server with gunicorn
run = ["bash", "-c", "cd banking_chatbot/backend && gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000 --workers 2 --timeout 120 --graceful-timeout 30"]
```

### Why Autoscale?

- **Stateless Architecture**: API is stateless (all state in PostgreSQL)
- **Cost-Effective**: Only runs when receiving requests
- **Auto-Scaling**: Handles traffic spikes automatically
- **WebSocket Support**: Autoscale supports WebSocket connections

---

## 📦 Production Server Configuration

### Gunicorn with Uvicorn Workers

The deployment uses **gunicorn** as the process manager with **uvicorn** workers for optimal performance:

- **2 Workers**: Parallel request handling
- **120s Timeout**: Handles long-running AI requests
- **30s Graceful Timeout**: Clean shutdown on deployment updates
- **UvicornWorker**: ASGI support for WebSockets

### Performance Characteristics

- **Concurrent Connections**: 20-50 per worker
- **WebSocket Support**: Full duplex real-time updates
- **Request Timeout**: 120 seconds (AI requests can be slow)
- **Rate Limiting**: Configured per endpoint (5-30 requests/minute)

---

## 🔒 Security Configuration

### Rate Limiting (slowapi)

| Endpoint Category | Rate Limit | Purpose |
|-------------------|------------|---------|
| Authentication | 5/min | Prevent brute force |
| Chat API | 20/min | Prevent API abuse |
| New Conversations | 10/min | Limit resource usage |
| Analytics/Settings | 30/min | General protection |

### Authentication & Authorization

- **JWT Tokens**: HS256 algorithm, configurable expiration
- **Role-Based Access**: ADMIN, SUPERVISOR, AGENT
- **Password Hashing**: bcrypt with salt rounds
- **Audit Logging**: All critical operations logged

### WebSocket Security

- **JWT Authentication**: Required via query parameter `?token=JWT`
- **Role-Based Routing**: Messages filtered by user role
- **Connection Limits**: Per-user and per-role limits
- **Automatic Cleanup**: Disconnected connections cleaned up

---

## 🌐 API Endpoints

### Public Endpoints
- `GET /health` - Health check
- `POST /api/v1/auth/login` - User authentication
- `POST /api/v1/chat/start` - Start customer conversation
- `POST /api/v1/chat/message` - Send chat message

### Authenticated Endpoints (Require JWT)
- `GET /api/v1/tickets/` - List tickets (note trailing slash)
- `GET /api/v1/analytics/dashboard` - Dashboard metrics
- `GET /api/v1/customers` - Customer management
- `GET /api/v1/knowledge` - Knowledge base
- `GET /api/v1/settings` - System/user settings
- `GET /api/v1/notifications/me` - User notifications
- `WS /api/v1/ws?token=JWT` - WebSocket real-time updates

### OpenAPI Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

**⚠️ Important**: Some endpoints require a trailing slash (e.g., `/api/v1/tickets/`) due to SPA routing configuration.

---

## 🧪 Pre-Deployment Testing

Run these tests before deploying:

### 1. Health Check
```bash
curl https://your-app-domain.repl.co/health
# Expected: {"status": "ok", "message": "Banking ChatBot API v1.0"}
```

### 2. Authentication
```bash
curl -X POST https://your-app-domain.repl.co/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@joxai.com","password":"admin123"}'
# Expected: {"token": "...", "user": {...}}
```

### 3. Analytics (with token)
```bash
TOKEN="your-jwt-token"
curl https://your-app-domain.repl.co/api/v1/analytics/dashboard \
  -H "Authorization: Bearer $TOKEN"
# Expected: Dashboard metrics JSON
```

### 4. WebSocket
```bash
curl https://your-app-domain.repl.co/api/v1/ws/stats
# Expected: Connection statistics JSON
```

---

## 🚀 Deployment Steps

### 1. Configure Secrets

1. Open your Replit project
2. Click the **Secrets** tab (lock icon)
3. Add all required environment variables (see checklist above)
4. **Critical**: Ensure `SECRET_KEY`, `DATABASE_URL`, and at least one AI API key are set

### 2. Click Deploy

1. Click the **Deploy** button in Replit
2. Choose **Production** deployment
3. Replit will:
   - Run the build command (build React frontend)
   - Run database migrations
   - Start the production server with gunicorn

### 3. Verify Deployment

1. Check deployment logs for errors
2. Visit your deployment URL (e.g., `https://your-app.repl.co`)
3. Login with admin credentials
4. Test critical features:
   - Dashboard loads
   - Ticket creation
   - Chat conversations
   - Real-time WebSocket updates

### 4. Post-Deployment

1. **Change default admin password** immediately
2. Configure SMTP for email notifications
3. Monitor logs for errors
4. Test with real users
5. Set up monitoring/alerts

---

## 📊 Monitoring & Maintenance

### Built-in Monitoring

- **Health Endpoint**: `GET /health` - Monitor API status
- **WebSocket Stats**: `GET /api/v1/ws/stats` - Connection metrics
- **Audit Logs**: Database audit trail of all critical operations
- **Analytics Dashboard**: In-app metrics (conversations, tickets, customers)

### Database Maintenance

- **Backups**: Replit automatically backs up PostgreSQL
- **Migrations**: Use Alembic for schema changes
- **Rollbacks**: Replit supports instant rollbacks to previous versions

### Performance Tuning

- **Gunicorn Workers**: Adjust `--workers` based on CPU cores
- **Database Connections**: SQLAlchemy connection pooling auto-configured
- **Rate Limits**: Adjust in code based on usage patterns
- **Caching**: Consider adding Redis for high-traffic deployments

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "API endpoint not found" (404)
- **Cause**: Missing trailing slash on endpoint
- **Solution**: Add trailing slash (e.g., `/api/v1/tickets/`)

#### 2. "Unauthorized" (401)
- **Cause**: Invalid or expired JWT token
- **Solution**: Re-authenticate to get new token

#### 3. AI requests failing
- **Cause**: Missing API key or insufficient credits
- **Solution**: Verify `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` in secrets

#### 4. Email notifications not sending
- **Cause**: SMTP not configured
- **Solution**: Add SMTP configuration to secrets (optional feature)

#### 5. WebSocket connection failing
- **Cause**: Invalid JWT token or network issues
- **Solution**: Ensure token is passed as query parameter: `/api/v1/ws?token=JWT`

### Debug Mode

To enable debug logging:
```bash
# Add to secrets
LOG_LEVEL=DEBUG
```

---

## 💰 Pricing Considerations

### Replit Costs
- **Autoscale Deployment**: Pay per request/compute time
- **PostgreSQL Database**: Included in deployment
- **Egress**: Minimal for typical API usage

### External Service Costs
- **Anthropic Claude API**: ~$3-15 per 1M tokens (varies by model)
- **OpenAI GPT API**: ~$3-60 per 1M tokens (varies by model)
- **SMTP (Gmail)**: Free for low volume, paid for high volume
- **SMS (Twilio)**: ~$0.0075 per SMS (when implemented)

### Cost Optimization Tips
1. Use rate limiting to prevent API abuse
2. Monitor AI token usage
3. Cache common AI responses
4. Use cheaper AI models for simple queries
5. Implement request batching where possible

---

## 📈 Scaling Recommendations

### Current Capacity
- **Autoscale**: Handles 100-1000 requests/min automatically
- **Database**: PostgreSQL scales with Replit plan
- **WebSocket**: 50-100 concurrent connections per worker

### When to Scale Up
- **High Traffic**: Increase gunicorn workers (4-8 workers)
- **Database Load**: Upgrade Replit database plan
- **AI Costs**: Implement caching layer (Redis)
- **Global Users**: Consider CDN for static assets

### Enterprise Considerations
- Migrate to **VM Deployment** for dedicated resources
- Add **Redis** for session/cache management
- Implement **load balancing** for multiple regions
- Set up **monitoring** (Datadog, New Relic, etc.)
- Configure **backup strategy** beyond Replit defaults

---

## 🎯 Success Metrics

After deployment, monitor these KPIs:

- **Uptime**: Target 99.9%
- **Response Time**: API < 500ms, AI requests < 10s
- **Error Rate**: < 1% of requests
- **WebSocket Connections**: Monitor disconnect rate
- **Escalation Rate**: Track AI → human escalations
- **User Satisfaction**: Measure through feedback

---

## 📞 Support

For issues or questions:
1. Check this guide and `.env.example`
2. Review API documentation at `/docs`
3. Check Replit deployment logs
4. Review audit logs in database
5. Contact Replit support for platform issues

---

## 🎉 You're Ready to Deploy!

Follow the steps above and your JoxAI Banking Chatbot will be live in minutes.

**Remember**:
- ✅ Set all required secrets
- ✅ Test the health endpoint after deployment
- ✅ Change the default admin password
- ✅ Monitor logs for the first few hours
- ✅ Have fun serving your customers! 🚀
