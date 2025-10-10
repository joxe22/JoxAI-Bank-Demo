# Integration test configuration using PostgreSQL
import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base
from app.dependencies import get_db
from app.repositories.user_repository import UserRepository
from app.core.security import get_password_hash
from app.models.db_user import UserRole

# Use test PostgreSQL database
TEST_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/test_db")

@pytest.fixture(scope="function")
def integration_db():
    """Create a test database session"""
    engine = create_engine(TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def integration_client(integration_db):
    """FastAPI test client with PostgreSQL database"""
    def override_get_db():
        try:
            yield integration_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def integration_test_user(integration_db):
    """Create a test user in PostgreSQL"""
    user_repo = UserRepository(integration_db)
    
    # Check if user already exists
    existing_user = user_repo.get_by_username("testuser_integration")
    if existing_user:
        return existing_user
    
    user = user_repo.create(
        username="testuser_integration",
        email="test_integration@example.com",
        password_hash=get_password_hash("testpass123"),
        full_name="Integration Test User",
        role=UserRole.AGENT
    )
    return user

@pytest.fixture
def integration_auth_headers(integration_client, integration_test_user):
    """Get authentication headers for integration tests"""
    response = integration_client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser_integration",
            "password": "testpass123"
        }
    )
    
    if response.status_code != 200:
        raise Exception(f"Login failed: {response.json()}")
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
