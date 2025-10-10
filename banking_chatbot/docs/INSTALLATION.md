# JoxAI Banking Chatbot - Installation & Setup Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Quick Start](#quick-start)
3. [Detailed Installation](#detailed-installation)
4. [Configuration](#configuration)
5. [Database Setup](#database-setup)
6. [Deployment](#deployment)
7. [Post-Installation](#post-installation)

---

## System Requirements

### Server Requirements
- **OS**: Linux (Ubuntu 20.04+ recommended) or macOS
- **CPU**: 2+ cores (4+ recommended for production)
- **RAM**: 2GB minimum (4GB+ recommended)
- **Storage**: 10GB minimum (20GB+ recommended)
- **Network**: Stable internet connection with HTTPS support

### Software Dependencies
- **Python**: 3.11 or higher
- **Node.js**: 20.x or higher
- **PostgreSQL**: 15 or higher
- **npm**: 9.x or higher

### Optional (for local development)
- **Docker**: For containerized database
- **Redis**: For caching (future feature)

---

## Quick Start

### For Replit (Recommended)

1. **Fork/Clone Repository**
   ```bash
   # The repository is pre-configured for Replit
   # Just click "Run" and it will auto-configure
   ```

2. **Set Environment Variables**
   - Go to Replit Secrets (🔒 icon)
   - Add required variables (see Configuration section)

3. **Run Application**
   ```bash
   # Click the "Run" button or use:
   bash start_production.sh
   ```

4. **Access Application**
   - Admin Panel: `https://your-repl.replit.app`
   - API Docs: `https://your-repl.replit.app/docs`

### For Local Development

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd banking-chatbot
   ```

2. **Install Backend Dependencies**
   ```bash
   cd banking_chatbot/backend
   pip install -r requirements.txt
   ```

3. **Install Frontend Dependencies**
   ```bash
   cd ../frontend/admin-panel
   npm install
   ```

4. **Setup Database**
   ```bash
   # Create PostgreSQL database
   createdb banking_chatbot
   
   # Run migrations
   cd ../../backend
   alembic upgrade head
   ```

5. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

6. **Start Development Server**
   ```bash
   # Terminal 1: Backend
   cd banking_chatbot/backend
   uvicorn app.main:app --reload --port 8000
   
   # Terminal 2: Frontend
   cd banking_chatbot/frontend/admin-panel
   npm run dev
   ```

---

## Detailed Installation

### Step 1: System Preparation

**Ubuntu/Debian:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs -y

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y
```

**macOS:**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python@3.11 node postgresql

# Start PostgreSQL
brew services start postgresql
```

### Step 2: Database Setup

1. **Create Database**
   ```bash
   # Switch to postgres user
   sudo -u postgres psql
   
   # In PostgreSQL console:
   CREATE DATABASE banking_chatbot;
   CREATE USER chatbot_user WITH ENCRYPTED PASSWORD 'your_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE banking_chatbot TO chatbot_user;
   \q
   ```

2. **Initialize Database Schema**
   ```bash
   cd banking_chatbot/backend
   
   # Run migrations
   alembic upgrade head
   
   # Or use the database init script
   python -m app.core.seed
   ```

### Step 3: Backend Installation

1. **Create Virtual Environment**
   ```bash
   cd banking_chatbot/backend
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Python Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Verify Installation**
   ```bash
   python -c "import fastapi; print(fastapi.__version__)"
   python -c "import sqlalchemy; print(sqlalchemy.__version__)"
   ```

### Step 4: Frontend Installation

1. **Install Node Dependencies**
   ```bash
   cd banking_chatbot/frontend/admin-panel
   npm install
   ```

2. **Build Frontend** (for production)
   ```bash
   npm run build
   ```

3. **Verify Build**
   ```bash
   ls -la dist/
   # Should see index.html and assets folder
   ```

---

## Configuration

### Environment Variables

Create `.env` file in `banking_chatbot/backend/`:

```bash
# Required Variables
DATABASE_URL=postgresql://chatbot_user:your_password@localhost:5432/banking_chatbot
SECRET_KEY=your-secret-key-min-32-chars
AI_PROVIDER=openai

# AI Provider (choose one)
OPENAI_API_KEY=sk-your-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Optional Variables
LOG_LEVEL=info
CORS_ORIGINS=http://localhost:3000,http://localhost:5000
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Frontend Configuration

Edit `banking_chatbot/frontend/admin-panel/.env`:

```bash
VITE_API_URL=http://localhost:8000
```

### Security Configuration

1. **Generate Secret Key**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Setup HTTPS** (Production)
   - Replit provides automatic HTTPS
   - For custom domains, configure SSL certificates

3. **Configure CORS**
   ```bash
   CORS_ORIGINS=https://yourdomain.com,https://admin.yourdomain.com
   ```

---

## Database Setup

### Automatic Setup

```bash
cd banking_chatbot/backend
python -m app.core.seed
```

This creates:
- Admin user (username: `admin`, password: `admin123`)
- Sample knowledge base articles
- Default system settings

### Manual Setup

1. **Create Admin User**
   ```bash
   psql -U chatbot_user -d banking_chatbot
   
   INSERT INTO users (username, email, password_hash, full_name, role)
   VALUES ('admin', 'admin@joxaibank.com', 
           '$2b$12$...', 'Admin User', 'ADMIN');
   ```

2. **Create Tables** (if migrations didn't run)
   ```bash
   # Generate migration
   alembic revision --autogenerate -m "Initial schema"
   
   # Apply migration
   alembic upgrade head
   ```

### Database Backup

```bash
# Backup
pg_dump -U chatbot_user banking_chatbot > backup.sql

# Restore
psql -U chatbot_user banking_chatbot < backup.sql
```

---

## Deployment

### Replit Deployment

1. **Configure .replit**
   ```toml
   [deployment]
   deploymentTarget = "autoscale"
   run = ["bash", "-c", "cd banking_chatbot/backend && bash start_production.sh"]
   build = ["bash", "-c", "cd banking_chatbot/frontend/admin-panel && npm install && npm run build"]
   ```

2. **Set Secrets**
   - Add all environment variables in Replit Secrets
   - Never commit `.env` files

3. **Deploy**
   - Click "Deploy" button
   - Choose "Autoscale" deployment
   - Monitor deployment logs

### Traditional Server Deployment

1. **Install Dependencies**
   ```bash
   # See Detailed Installation section
   ```

2. **Configure Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/joxai-chatbot.service
   ```

   ```ini
   [Unit]
   Description=JoxAI Banking Chatbot
   After=network.target postgresql.service
   
   [Service]
   Type=notify
   User=www-data
   WorkingDirectory=/var/www/banking-chatbot/backend
   Environment="PATH=/var/www/banking-chatbot/backend/venv/bin"
   ExecStart=/var/www/banking-chatbot/backend/venv/bin/gunicorn \
             -c gunicorn_conf.py app.main:app
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and Start Service**
   ```bash
   sudo systemctl enable joxai-chatbot
   sudo systemctl start joxai-chatbot
   sudo systemctl status joxai-chatbot
   ```

4. **Configure Nginx** (reverse proxy)
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /api/v1/ws {
           proxy_pass http://127.0.0.1:5000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
       }
   }
   ```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Post-Installation

### Verify Installation

1. **Check Backend**
   ```bash
   curl http://localhost:5000/health
   # Should return: {"status":"ok","message":"Banking ChatBot API v1.0"}
   ```

2. **Check Database**
   ```bash
   curl http://localhost:5000/readiness
   # Should return: {"api":"ok","database":"ok","version":"1.0.0"}
   ```

3. **Check Frontend**
   ```bash
   # Navigate to http://localhost:5000
   # Should see login page
   ```

### Initial Configuration

1. **Login as Admin**
   - Username: `admin`
   - Password: `admin123` (change immediately!)

2. **Change Admin Password**
   - Go to Settings → User Settings
   - Update password
   - Save changes

3. **Configure AI Provider**
   - Go to Settings → Bot Configuration
   - Select AI Provider (OpenAI/Anthropic/Mock)
   - Enter API Key
   - Save and test

4. **Create User Accounts**
   - Go to Settings → User Management (if admin)
   - Create agents and supervisors
   - Assign roles and permissions

5. **Setup Knowledge Base**
   - Go to Knowledge Base
   - Create initial articles
   - Organize by category

6. **Test Chat Widget**
   - Visit `/widget-demo`
   - Test AI responses
   - Test escalation flow

### Performance Tuning

1. **Database Optimization**
   ```bash
   # Add indexes
   CREATE INDEX idx_tickets_status ON tickets(status);
   CREATE INDEX idx_tickets_assigned_to ON tickets(assigned_to);
   CREATE INDEX idx_conversations_user_id ON conversations(user_id);
   ```

2. **Worker Scaling**
   ```bash
   # Adjust workers based on CPU
   export GUNICORN_WORKERS=4
   ```

3. **Logging**
   ```bash
   # Set appropriate log level
   export LOG_LEVEL=warning  # for production
   ```

---

## Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Find process using port 5000
lsof -i :5000
# Kill process
kill -9 <PID>
```

**Database Connection Error**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -U chatbot_user -d banking_chatbot
```

**Frontend Build Fails**
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install
npm run build
```

**AI Responses Not Working**
- Verify API key is set correctly
- Check API provider status
- Review logs for error messages
- Test with mock provider first

---

## Next Steps

After installation:

1. ✅ Read the [User Guide](USER_GUIDE.md)
2. ✅ Review [API Reference](API_REFERENCE.md)
3. ✅ Check [Security Best Practices](SECURITY.md)
4. ✅ Configure monitoring and alerts
5. ✅ Setup backup procedures

---

## Support

**Documentation:**
- User Guide: `docs/USER_GUIDE.md`
- API Reference: `docs/API_REFERENCE.md`
- FAQ: `docs/FAQ.md`

**Contact:**
- Email: support@joxaibank.com
- Issues: GitHub Issues
- Community: Discord/Slack

---

**Installation Guide Version:** 1.0.0  
**Last Updated:** October 10, 2025  
**Platform:** Replit Autoscale / Traditional Server
