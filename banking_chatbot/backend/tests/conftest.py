# Test fixtures and configuration
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base
from app.dependencies import get_db
from app.repositories.user_repository import UserRepository
from app.core.security import get_password_hash
from app.models.db_user import UserRole

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_db():
    """Create a fresh database for each test"""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(test_db):
    """FastAPI test client with test database"""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(test_db):
    """Create a test user"""
    user_repo = UserRepository(test_db)
    user = user_repo.create(
        username="testuser",
        email="test@example.com",
        password_hash=get_password_hash("testpassword"),
        full_name="Test User",
        role=UserRole.AGENT
    )
    return user

@pytest.fixture
def test_admin(test_db):
    """Create a test admin user"""
    user_repo = UserRepository(test_db)
    admin = user_repo.create(
        username="admin",
        email="admin@example.com",
        password_hash=get_password_hash("adminpass"),
        full_name="Admin User",
        role=UserRole.ADMIN
    )
    return admin

@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers for test user"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_headers(client, test_admin):
    """Get authentication headers for admin user"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "admin",
            "password": "adminpass"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def mock_ai_service(monkeypatch):
    """Mock AI service for testing"""
    async def mock_generate_response(*args, **kwargs):
        return "This is a mock AI response for testing purposes."
    
    from app.services import ai_service
    monkeypatch.setattr(ai_service, "generate_response", mock_generate_response)
    
    return mock_generate_response
