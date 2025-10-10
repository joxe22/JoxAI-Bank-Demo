# JoxAI Banking Chatbot - Frequently Asked Questions (FAQ)

## Table of Contents
1. [General Questions](#general-questions)
2. [Installation & Setup](#installation--setup)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Troubleshooting](#troubleshooting)
6. [Security](#security)
7. [Performance](#performance)
8. [Customization](#customization)

---

## General Questions

### What is JoxAI Banking Chatbot?

JoxAI is an AI-powered customer service platform designed specifically for banking institutions. It combines intelligent chatbot capabilities with human agent support, ticket management, and comprehensive analytics.

### What features are included?

- ✅ AI-powered chat with OpenAI/Anthropic integration
- ✅ Seamless escalation to human agents
- ✅ Complete ticket management system
- ✅ Real-time WebSocket notifications
- ✅ Comprehensive analytics dashboard
- ✅ Knowledge base management
- ✅ Customer relationship management (CRM)
- ✅ Role-based access control
- ✅ Multi-language support ready
- ✅ Rate limiting and security features

### Is it production-ready?

Yes! JoxAI has been built with production in mind:
- Comprehensive test suite (unit, integration, E2E)
- Production deployment configuration
- Security hardening (rate limiting, audit logs)
- Database-backed persistence (PostgreSQL)
- Scalable architecture (Gunicorn + Uvicorn workers)
- Health check endpoints for load balancers

### What are the licensing terms?

JoxAI Banking Chatbot is a **commercial product** intended for licensed use by banking institutions. Contact us for licensing options and pricing.

---

## Installation & Setup

### What are the system requirements?

**Minimum:**
- 2 CPU cores
- 2GB RAM
- 10GB storage
- Python 3.11+
- Node.js 20+
- PostgreSQL 15+

**Recommended for Production:**
- 4+ CPU cores
- 4GB+ RAM
- 20GB+ storage
- Load balancer
- CDN for static assets

### Can I deploy this on Replit?

Yes! JoxAI is optimized for **Replit Autoscale** deployment with pre-configured settings for one-click deployment.

### How long does installation take?

- **Replit**: 5-10 minutes (mostly automated)
- **Traditional Server**: 30-60 minutes (manual setup)
- **Docker**: 10-15 minutes

### Do I need Docker?

No, Docker is optional. The application can run:
- Natively on Linux/macOS
- Via Docker containers
- On Replit (no Docker needed)

---

## Configuration

### Which AI provider should I use?

| Provider | Best For | Cost | Performance |
|----------|----------|------|-------------|
| **OpenAI** | General use, good performance | $$ | Fast, reliable |
| **Anthropic** | Advanced reasoning, safety | $$$ | Excellent |
| **Mock** | Testing, development | Free | Instant (fixed responses) |

**Recommendation:** Start with OpenAI for production, use Mock for testing.

### How do I configure the AI model?

1. Go to **Settings → Bot Configuration**
2. Select AI Provider
3. Enter API Key
4. Choose model (e.g., `gpt-4o-mini`, `claude-sonnet-4`)
5. Adjust temperature (0-1, default: 0.7)
6. Save settings

### Can I customize the bot's personality?

Yes! Edit the system prompt in **Settings → Bot Configuration**:

```
You are a professional banking assistant for JoxAI Bank. 
Be friendly, helpful, and secure. Always verify identity 
before sharing account information...
```

### How do I add more languages?

The system is i18n-ready. To add languages:
1. Create translation files in `/locales`
2. Update frontend language selector
3. Configure backend language detection
4. Test all UI elements

---

## Usage

### How do customers start a chat?

1. **Via Website Widget:**
   - Embed chat widget on your website
   - Customer clicks chat button
   - AI responds automatically

2. **Via API:**
   ```bash
   POST /api/v1/chat/start
   {
     "user_id": "customer_123"
   }
   ```

### When does the AI escalate to a human?

Automatic escalation triggers:
- Customer requests "speak to an agent"
- Account-specific inquiries requiring authentication
- AI confidence is low
- Sensitive transactions (wire transfers, password resets)
- Customer expresses frustration

### How do agents receive notifications?

- **WebSocket**: Real-time browser notifications
- **Email**: Ticket assignment alerts (if configured)
- **Dashboard**: Red badges on ticket counts
- **Audio**: Optional browser sound alerts

### Can multiple agents work on one ticket?

No, tickets are assigned to one agent at a time to avoid conflicts. However:
- Supervisors can reassign tickets
- Agents can add internal notes
- Full conversation history is visible

---

## Troubleshooting

### Chat widget not appearing on website

**Check:**
1. Widget script is included in HTML
2. Script URL is correct
3. CORS allows your domain
4. No JavaScript errors in console
5. Widget initialization code is correct

**Fix:**
```html
<script src="https://your-app.replit.app/widget.js"></script>
<script>
  JoxAIWidget.init({
    apiUrl: 'https://your-app.replit.app'
  });
</script>
```

### AI responses are slow

**Possible Causes:**
- AI provider rate limits
- Network latency
- High server load
- Large conversation history

**Solutions:**
1. Upgrade AI provider tier
2. Reduce max_tokens in settings
3. Scale up workers: `GUNICORN_WORKERS=8`
4. Use CDN for static assets
5. Enable response caching (future feature)

### WebSocket keeps disconnecting

**Check:**
1. Network stability
2. Load balancer WebSocket support
3. Timeout settings
4. Token expiration

**Fix:**
```javascript
// Frontend auto-reconnect (already implemented)
ws.onclose = () => {
  setTimeout(() => connectWebSocket(), 5000);
};
```

### Database connection errors

**Symptoms:**
```
psycopg2.OperationalError: could not connect to server
```

**Solutions:**
1. Verify DATABASE_URL is correct
2. Check PostgreSQL is running: `systemctl status postgresql`
3. Test connection: `psql $DATABASE_URL`
4. Check firewall allows port 5432
5. Verify database exists: `\l` in psql

### Frontend shows blank page

**Debug Steps:**
1. Check browser console for errors
2. Verify frontend build completed: `ls dist/`
3. Check network tab for failed requests
4. Clear browser cache
5. Rebuild frontend: `npm run build`

**Common Issues:**
- API URL mismatch (dev vs. prod)
- CORS blocking requests
- Missing environment variables
- Build artifacts not deployed

---

## Security

### How secure is the system?

JoxAI implements multiple security layers:
- ✅ JWT authentication with expiration
- ✅ bcrypt password hashing
- ✅ Rate limiting on all endpoints
- ✅ CORS protection
- ✅ SQL injection prevention (ORM)
- ✅ XSS protection
- ✅ Comprehensive audit logging
- ✅ HTTPS enforced in production

### How often should I rotate API keys?

**Best Practices:**
- **OpenAI/Anthropic Keys**: Every 90 days
- **SECRET_KEY**: Every 6 months or after breach
- **Database Passwords**: Every 6 months
- **JWT Tokens**: Auto-expire in 30 minutes

### What data is logged?

**Audit Logs Include:**
- User login/logout events
- Ticket creation/assignment/closure
- Conversation escalations
- Settings changes
- Knowledge base modifications
- Failed authentication attempts

**NOT Logged:**
- Passwords or API keys
- Customer PII (unless required for support)
- Payment information

### Is data encrypted?

- **In Transit**: HTTPS/TLS 1.3
- **At Rest**: PostgreSQL encryption (if enabled)
- **Passwords**: bcrypt hashing
- **Secrets**: Environment variables (not committed)

### How do I handle GDPR/privacy compliance?

1. Enable audit logging (default: ON)
2. Implement data retention policies
3. Add "Right to be Forgotten" workflow
4. Update Privacy Policy with AI usage
5. Get user consent for data processing
6. Document data flows and storage

---

## Performance

### How many concurrent users can it handle?

**Replit Autoscale:**
- 100-500 concurrent users
- 1,000-5,000 requests/hour

**Traditional Server (4 CPU, 8GB RAM):**
- 500-1,000 concurrent users
- 10,000-50,000 requests/hour

**Scaling:**
- Add more workers: `GUNICORN_WORKERS=12`
- Use load balancer with multiple instances
- Enable Redis caching (future)
- Upgrade to Reserved VM on Replit

### What are the API rate limits?

| Endpoint | Limit |
|----------|-------|
| `/auth/login` | 5/minute |
| `/chat/*` | 20/minute |
| `/tickets/*` | 30/minute |
| `/analytics/*` | 30/minute |
| Default | 60/minute |

Customize in `app/core/limiter.py`

### How to optimize database performance?

1. **Add Indexes:**
   ```sql
   CREATE INDEX idx_tickets_status ON tickets(status);
   CREATE INDEX idx_messages_conversation ON messages(conversation_id);
   ```

2. **Connection Pooling:**
   ```python
   # Already configured in database.py
   pool_size=5
   max_overflow=10
   ```

3. **Query Optimization:**
   - Use pagination for large datasets
   - Avoid N+1 queries (use joins)
   - Monitor slow queries

4. **Regular Maintenance:**
   ```bash
   # Vacuum and analyze
   psql -c "VACUUM ANALYZE;"
   ```

### Frontend bundle size too large?

**Check:**
```bash
npm run build
# Analyze dist/assets/*.js file sizes
```

**Optimize:**
1. Already using code splitting ✅
2. Tree shaking enabled ✅
3. Minification enabled ✅
4. Gzip compression (configure in nginx/CDN)
5. Lazy load routes (future enhancement)

---

## Customization

### Can I change the UI theme/colors?

Yes! Edit CSS variables in `/src/styles/variables.css`:

```css
:root {
  --primary-color: #2563eb;    /* Change primary color */
  --secondary-color: #8b5cf6;  /* Change secondary color */
  --background: #ffffff;        /* Background color */
}
```

Or use Settings → Appearance (if implemented)

### Can I add custom fields to tickets?

Yes, but requires code changes:

1. Add database column:
   ```sql
   ALTER TABLE tickets ADD COLUMN custom_field VARCHAR(255);
   ```

2. Update Pydantic model (`app/schemas/ticket.py`)
3. Update frontend form
4. Redeploy

**Better Alternative:** Use ticket tags/categories for custom classification

### Can I integrate with my existing CRM?

Yes! Options:

1. **API Integration:**
   - Use JoxAI's REST API
   - Sync data via webhooks
   - Build custom connector

2. **Database Sync:**
   - Direct PostgreSQL queries
   - Scheduled ETL jobs
   - Use foreign data wrappers

3. **Webhook Events:**
   - Listen for ticket events
   - Push to external CRM
   - Bi-directional sync

### Can I white-label the product?

Yes! Customization options:

1. **Branding:**
   - Logo: Update in `/public/logo.svg`
   - Colors: CSS variables
   - Fonts: Edit `index.css`

2. **Text/Labels:**
   - App name: `APP_NAME` env variable
   - UI text: Edit language files

3. **Domain:**
   - Custom domain on Replit
   - Or deploy to your infrastructure

---

## Advanced Topics

### How do I backup the database?

**Automated Backup:**
```bash
# Daily backup script
#!/bin/bash
pg_dump $DATABASE_URL > /backups/backup_$(date +%Y%m%d).sql
```

**Manual Backup:**
```bash
pg_dump -U chatbot_user banking_chatbot > backup.sql
```

**Restore:**
```bash
psql -U chatbot_user banking_chatbot < backup.sql
```

### Can I run multiple environments (dev/staging/prod)?

Yes! Use environment-specific configs:

```bash
# Development
export ENVIRONMENT=development
export DATABASE_URL=postgresql://localhost/chatbot_dev

# Staging
export ENVIRONMENT=staging
export DATABASE_URL=postgresql://staging-db/chatbot_staging

# Production
export ENVIRONMENT=production
export DATABASE_URL=postgresql://prod-db/chatbot_prod
```

### How do I monitor production health?

1. **Health Endpoints:**
   - `/health` - Basic check
   - `/readiness` - Database check

2. **Logging:**
   ```bash
   # View logs
   tail -f /var/log/joxai-chatbot/app.log
   ```

3. **Metrics** (future enhancement):
   - Prometheus integration
   - Grafana dashboards
   - Alert manager

4. **External Monitoring:**
   - UptimeRobot for uptime
   - Sentry for error tracking
   - Datadog/New Relic for APM

---

## Getting More Help

### Where can I find more documentation?

- **User Guide:** `/docs/USER_GUIDE.md`
- **API Reference:** `/docs/API_REFERENCE.md`
- **Installation:** `/docs/INSTALLATION.md`
- **Technical Docs:** `/docs/TECHNICAL.md`
- **Deployment:** `/DEPLOYMENT.md`

### How do I report bugs?

1. Check existing issues on GitHub
2. Create new issue with:
   - Description of problem
   - Steps to reproduce
   - Expected vs. actual behavior
   - Environment details (OS, versions)
   - Relevant logs/screenshots

### Can I request new features?

Yes! Submit feature requests via:
- GitHub Issues (label: `enhancement`)
- Email: features@joxaibank.com
- Community forum

### Is there a support SLA?

**Enterprise Support:**
- Response time: < 4 hours
- Resolution: Best effort within 48 hours
- 24/7 availability for critical issues
- Dedicated support channel

**Community Support:**
- Best effort
- GitHub issues
- Community forums

---

## Quick Troubleshooting Checklist

**❓ Something's not working?**

1. ☑️ Check health endpoints: `/health`, `/readiness`
2. ☑️ Review browser console for errors
3. ☑️ Check backend logs: `tail -f app.log`
4. ☑️ Verify environment variables are set
5. ☑️ Test database connection: `psql $DATABASE_URL`
6. ☑️ Restart services: `systemctl restart joxai-chatbot`
7. ☑️ Clear cache and rebuild: `npm run build`
8. ☑️ Check API rate limits
9. ☑️ Verify API keys are valid
10. ☑️ Review recent changes/deployments

**Still stuck?** Contact support with:
- Error messages
- Steps to reproduce
- Environment details
- Recent changes made

---

**FAQ Version:** 1.0.0  
**Last Updated:** October 10, 2025  
**Next Review:** January 10, 2026
