# JoxAI Banking Chatbot - Production Deployment Guide

## 🚀 Deployment Configuration

### Replit Autoscale Deployment

The application is optimized for **Replit Autoscale** deployment with the following architecture:

```
┌─────────────────────────────────────┐
│   Replit Autoscale Load Balancer    │
└──────────────┬──────────────────────┘
               │
       ┌───────┴───────┐
       │   Port 5000   │
       └───────┬───────┘
               │
       ┌───────▼────────────────────┐
       │    Gunicorn (Master)       │
       │  + Uvicorn Workers (N)     │
       └────────────────────────────┘
                    │
         ┌──────────┴──────────┐
         │                     │
    ┌────▼─────┐        ┌──────▼───────┐
    │ FastAPI  │        │  Static      │
    │   API    │        │  Frontend    │
    └──────────┘        └──────────────┘
         │
    ┌────▼──────────┐
    │  PostgreSQL   │
    │   (Neon DB)   │
    └───────────────┘
```

### Production Configuration Files

1. **gunicorn_conf.py** - Optimized Gunicorn configuration
   - Auto-scales workers based on CPU cores
   - Worker restart policy to prevent memory leaks
   - SO_REUSEPORT for better load distribution
   - Comprehensive logging

2. **start_production.sh** - Production startup script
   - Environment validation
   - Database connectivity checks
   - Graceful startup and logging

## 📋 Deployment Settings

### Current .replit Configuration

```toml
[deployment]
deploymentTarget = "autoscale"
run = ["bash", "-c", "cd banking_chatbot/backend && bash start_production.sh"]
build = ["bash", "-c", "cd banking_chatbot/frontend/admin-panel && npm install && npm run build"]
```

**Recommended Update:** Use the optimized production script:
```toml
run = ["bash", "-c", "cd banking_chatbot/backend && bash start_production.sh"]
```

### Worker Configuration

**Auto-scaling Formula:** `workers = (CPU cores × 2) + 1`

For Replit Autoscale (typically 1-2 vCPUs):
- **Minimum**: 2 workers
- **Recommended**: 3-5 workers
- **Maximum**: 8 workers

Override via environment variable:
```bash
GUNICORN_WORKERS=4
```

### Performance Tuning

| Setting | Value | Purpose |
|---------|-------|---------|
| `max_requests` | 1000 | Restart workers after N requests (prevents memory leaks) |
| `timeout` | 120s | Worker timeout for long-running requests |
| `keepalive` | 5s | Keep-Alive connection timeout |
| `worker_connections` | 1000 | Max concurrent connections per worker |
| `preload_app` | true | Load app before forking (saves memory) |
| `reuse_port` | true | Enable SO_REUSEPORT (better load balancing) |

## 🌍 Environment Variables

### Required Production Variables

```bash
# Database (Required)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Security (Required)
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Provider (Required - choose one)
AI_PROVIDER=openai  # or 'anthropic' or 'mock'
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Email (Optional for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@joxaibank.com
```

### Optional Configuration

```bash
# Logging
LOG_LEVEL=info  # debug, info, warning, error, critical

# Workers
GUNICORN_WORKERS=4  # Override auto-calculation

# CORS (comma-separated)
CORS_ORIGINS=https://yourdomain.com,https://admin.yourdomain.com

# Performance
MAX_UPLOAD_SIZE=10485760  # 10MB in bytes
```

## 🏗️ Build Process

### Frontend Build

```bash
cd banking_chatbot/frontend/admin-panel
npm install
npm run build
```

**Output:** `dist/` directory with optimized static files

### Static File Serving

The FastAPI backend automatically serves:
- React app from `/` (SPA routing)
- Static assets from `/assets`
- API endpoints from `/api/v1`

## 🔍 Health Checks

### Endpoints

1. **Basic Health Check**
   ```
   GET /health
   Response: {"status": "ok", "message": "Banking ChatBot API v1.0"}
   ```

2. **Readiness Check** (includes DB check)
   ```
   GET /readiness
   Response: {
     "api": "ok",
     "database": "ok",
     "version": "1.0.0"
   }
   ```

### Load Balancer Configuration

Configure your load balancer to use:
- **Health check**: `/health` (every 30s)
- **Readiness check**: `/readiness` (before routing traffic)
- **Unhealthy threshold**: 3 consecutive failures
- **Healthy threshold**: 2 consecutive successes

## 🚦 Deployment Steps

### 1. Pre-deployment Checklist

- [ ] All environment variables configured
- [ ] Database migrations applied
- [ ] Frontend build successful
- [ ] Health checks responding
- [ ] API keys and secrets set

### 2. Deploy to Replit

```bash
# The deployment automatically:
1. Runs frontend build (npm run build)
2. Installs Python dependencies
3. Starts Gunicorn with optimized config
4. Serves static files and API
```

### 3. Post-deployment Verification

```bash
# Test health endpoints
curl https://your-app.replit.app/health
curl https://your-app.replit.app/readiness

# Test API
curl https://your-app.replit.app/api/v1/auth/health

# Test frontend
open https://your-app.replit.app
```

## 📊 Monitoring

### Key Metrics to Monitor

1. **Application Performance**
   - Response times (p50, p95, p99)
   - Request rates
   - Error rates (4xx, 5xx)

2. **System Resources**
   - CPU utilization
   - Memory usage
   - Worker count
   - Database connections

3. **Business Metrics**
   - Active conversations
   - Ticket creation rate
   - Escalation frequency
   - AI response quality

### Logging

Logs are output to stdout/stderr and can be viewed in Replit's deployment console.

**Log Format:**
```
%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s
```

## 🔒 Security Best Practices

1. **Always use HTTPS** in production (Replit provides this automatically)
2. **Rotate secrets** regularly (SECRET_KEY, API keys)
3. **Use strong passwords** for database and admin accounts
4. **Enable rate limiting** (already configured in the app)
5. **Monitor audit logs** for suspicious activity
6. **Keep dependencies updated** (`npm audit`, `pip-audit`)

## 🆘 Troubleshooting

### Common Issues

**Issue: Workers timeout**
```bash
# Increase timeout
export GUNICORN_TIMEOUT=180
```

**Issue: High memory usage**
```bash
# Reduce workers or enable more aggressive restarts
export GUNICORN_WORKERS=2
export MAX_REQUESTS=500
```

**Issue: Database connection errors**
```bash
# Check DATABASE_URL
echo $DATABASE_URL

# Test connection
curl https://your-app.replit.app/readiness
```

**Issue: Frontend not loading**
```bash
# Rebuild frontend
cd banking_chatbot/frontend/admin-panel
npm run build
```

## 📈 Scaling Recommendations

### Autoscale (Current)
- ✅ Best for moderate traffic (< 10k requests/day)
- ✅ Automatic scaling based on demand
- ✅ Cost-effective
- ⚠️ Cold starts possible during low traffic

### Reserved VM (Future)
- ✅ Consistent performance
- ✅ No cold starts
- ✅ Better for high traffic (> 10k requests/day)
- ⚠️ Higher cost

## 🎯 Performance Benchmarks

**Target Performance (Replit Autoscale):**
- Health check: < 50ms
- API requests: < 200ms (p95)
- AI responses: < 2s (p95)
- WebSocket latency: < 100ms
- Concurrent users: 100-500

---

**Last Updated:** October 10, 2025  
**Version:** 1.0.0  
**Deployment Target:** Replit Autoscale
