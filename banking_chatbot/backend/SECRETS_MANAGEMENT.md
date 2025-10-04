# Secrets Management Guide

## Overview
This application uses environment variables for all sensitive configuration, including API keys, database credentials, and JWT secrets. This ensures security and allows for easy deployment across different environments.

## Required Secrets

### Database (Automatically Configured on Replit)
- `DATABASE_URL`: PostgreSQL connection string
- `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`: PostgreSQL connection details

### Security
- **`SECRET_KEY`**: Used for JWT token signing
  - **CRITICAL**: Must be kept secret and never committed to version control
  - Auto-generated using cryptographically secure random if not provided
  - **Production**: MUST set a fixed value (minimum 32 characters)
  - Generate using: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

### AI Services (Optional)
- **`OPENAI_API_KEY`**: Required for OpenAI GPT models
  - Get from: https://platform.openai.com/api-keys
  - Format: `sk-...`
  
- **`ANTHROPIC_API_KEY`**: Required for Anthropic Claude models
  - Get from: https://console.anthropic.com/
  - Format: `sk-ant-...`

## Configuration Methods

### Development (Replit)
1. Use the Secrets tab in Replit to add environment variables
2. The application automatically detects and uses these secrets
3. Never commit actual secret values to `.env` files

### Production Deployment
1. Use your hosting platform's environment variable configuration
2. Ensure `SECRET_KEY` is set to a fixed, secure value
3. Configure only the AI provider you plan to use (OpenAI or Anthropic)

## Security Best Practices

1. **Never Hardcode Secrets**: Always use environment variables
2. **Rotate Secrets Regularly**: Update API keys and secrets periodically
3. **Use Strong SECRET_KEY**: Minimum 32 characters, cryptographically random
4. **Limit Secret Access**: Only grant access to team members who need it
5. **Monitor Secret Usage**: Track API usage and set up alerts for unusual activity

## Configuration Validation

The application validates configuration on startup:
- Checks if required secrets are present
- Auto-generates `SECRET_KEY` if missing (development only)
- Logs warnings for missing AI API keys
- Fails gracefully if database credentials are missing

## Checking Current Configuration

Run this command to verify secrets are set (without showing values):
```bash
python -c "from app.config import settings; print(f'SECRET_KEY: {'✅ Set' if settings.SECRET_KEY else '❌ Missing'}'); print(f'OPENAI_API_KEY: {'✅ Set' if settings.OPENAI_API_KEY else '❌ Missing'}'); print(f'ANTHROPIC_API_KEY: {'✅ Set' if settings.ANTHROPIC_API_KEY else '❌ Missing'}')"
```

## Troubleshooting

### "JWT token invalid" errors
- Check that `SECRET_KEY` is set and hasn't changed
- In production, ensure `SECRET_KEY` is fixed (not auto-generated each restart)

### AI service errors
- Verify the correct API key is set (`OPENAI_API_KEY` or `ANTHROPIC_API_KEY`)
- Check API key has not expired or been revoked
- Ensure account has sufficient credits/quota

### Database connection errors
- Verify `DATABASE_URL` is correct
- Check that database is accessible from your environment
- Ensure PostgreSQL credentials haven't changed

## Emergency Procedures

### Compromised SECRET_KEY
1. Generate a new `SECRET_KEY` immediately
2. Update in all environments (dev, staging, production)
3. All existing JWT tokens will be invalidated
4. Users will need to log in again

### Compromised API Keys
1. Revoke the compromised key in the provider's dashboard
2. Generate a new API key
3. Update `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
4. Restart the application

## Additional Resources

- [FastAPI Settings Management](https://fastapi.tiangolo.com/advanced/settings/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [OWASP Secrets Management](https://owasp.org/www-community/vulnerabilities/Use_of_hard-coded_password)
