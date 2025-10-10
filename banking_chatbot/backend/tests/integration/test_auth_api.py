# Integration tests for authentication API
import pytest
from fastapi.testclient import TestClient

def test_login_success(client, test_user):
    """Test successful login"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client, test_user):
    """Test login with invalid credentials"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401

def test_login_nonexistent_user(client):
    """Test login with nonexistent user"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "nonexistent",
            "password": "somepassword"
        }
    )
    
    assert response.status_code == 401

def test_get_current_user(client, auth_headers):
    """Test getting current user info"""
    response = client.get(
        "/api/v1/auth/me",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["role"] == "AGENT"

def test_unauthorized_access(client):
    """Test accessing protected endpoint without auth"""
    response = client.get("/api/v1/auth/me")
    
    assert response.status_code == 401
