# Unit tests for authentication
import pytest
from app.core.security import verify_password, get_password_hash, create_access_token, verify_token
from jose import JWTError
from datetime import datetime, timedelta

def test_password_hashing():
    """Test password hashing and verification"""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

def test_create_access_token():
    """Test JWT token creation"""
    data = {"sub": "testuser", "user_id": 1, "role": "AGENT"}
    token = create_access_token(data)
    
    assert token is not None
    assert isinstance(token, str)

def test_verify_token():
    """Test JWT token verification"""
    data = {"sub": "testuser", "user_id": 1, "role": "AGENT"}
    token = create_access_token(data)
    
    decoded = verify_token(token)
    assert decoded is not None
    assert decoded["sub"] == "testuser"
    assert decoded["user_id"] == 1
    assert decoded["role"] == "AGENT"

def test_invalid_token_verification():
    """Test verifying invalid token"""
    invalid_token = "invalid.token.here"
    
    with pytest.raises(JWTError):
        verify_token(invalid_token)
