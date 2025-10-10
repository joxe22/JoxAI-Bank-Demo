# JoxAI Banking Chatbot - Test Suite

## Overview
Comprehensive automated testing suite for the JoxAI Banking Chatbot system.

## Test Structure

```
tests/
├── unit/                      # Unit tests for core services
│   ├── test_auth.py          # Authentication & security tests
│   └── test_ai_service.py    # AI service tests
├── integration/               # Integration tests with database
│   ├── test_auth_api.py      # Auth API endpoints
│   ├── test_tickets_api.py   # Tickets API endpoints
│   └── test_conversations_api.py  # Conversations API
└── e2e/                       # End-to-end workflow tests
    └── test_chat_to_ticket_flow.py  # Complete user journeys
```

## Running Tests

### Run all unit tests:
```bash
cd banking_chatbot/backend
pytest tests/unit/ -v
```

### Run with coverage:
```bash
pytest tests/unit/ -v --cov=app --cov-report=term-missing
```

### Run integration tests (requires PostgreSQL):
```bash
pytest tests/integration/ -v
```

### Run E2E tests:
```bash
pytest tests/e2e/ -v
```

### Run all tests:
```bash
pytest tests/ -v
```

## Test Coverage

### Unit Tests (8 tests, all passing ✅)
- **Authentication** (4 tests): Password hashing, token creation/verification
- **AI Service** (4 tests): Mock provider, auto-detection, conversation history, custom prompts
- **Coverage**: 96% on security module

### Integration Tests (9 tests)
- **Auth API** (5 tests): Login, logout, user info, unauthorized access
- **Tickets API** (5 tests): List, create, detail, update, unauthorized
- **Conversations API** (4 tests): List, active, detail, unauthorized

### E2E Tests (3 tests)
- **Chat to Ticket Flow**: Complete escalation journey
- **Ticket Assignment**: Agent workflow
- **Knowledge Base Search**: Content management

## Test Fixtures

### Database Fixtures
- `test_db`: In-memory SQLite for unit tests
- `integration_db`: PostgreSQL for integration tests

### Authentication Fixtures
- `test_user`: Standard agent user
- `test_admin`: Admin user with elevated permissions
- `auth_headers`: Bearer token headers
- `admin_headers`: Admin bearer token headers

### Mock Fixtures
- `mock_ai_service`: Mocked AI responses for testing

## Environment Variables

```bash
# For integration tests
DATABASE_URL=postgresql://user:pass@localhost:5432/test_db

# For AI service testing
AI_PROVIDER=mock
```

## Best Practices

1. **Isolation**: Each test is independent and doesn't affect others
2. **Cleanup**: Database is reset between tests
3. **Mocking**: External services (AI, email) are mocked
4. **Async**: Properly handles async/await patterns
5. **Coverage**: Tracks code coverage metrics

## CI/CD Integration

Tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run Tests
  run: |
    cd banking_chatbot/backend
    pytest tests/ -v --cov=app
```

## Adding New Tests

1. Create test file in appropriate directory (unit/integration/e2e)
2. Import fixtures from conftest.py
3. Use descriptive test names: `test_<feature>_<scenario>()`
4. Include docstrings explaining what's tested
5. Assert expected behaviors clearly

## Test Categories

- 🔧 **Unit**: Test individual functions/classes
- 🔗 **Integration**: Test API endpoints with database
- 🚀 **E2E**: Test complete user workflows
