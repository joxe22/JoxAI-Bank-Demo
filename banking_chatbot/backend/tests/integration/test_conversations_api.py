# Integration tests for conversations API
import pytest
from fastapi.testclient import TestClient

def test_get_conversations(integration_client, integration_auth_headers):
    """Test getting list of conversations"""
    response = integration_client.get(
        "/api/v1/conversations",
        headers=integration_auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_active_conversations(integration_client, integration_auth_headers):
    """Test getting active conversations"""
    response = integration_client.get(
        "/api/v1/conversations/active",
        headers=integration_auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_conversation_detail(integration_client, integration_auth_headers):
    """Test getting conversation details"""
    # First get list of conversations
    list_response = integration_client.get(
        "/api/v1/conversations",
        headers=integration_auth_headers
    )
    
    conversations = list_response.json()
    
    if len(conversations) > 0:
        conv_id = conversations[0]["id"]
        
        # Get conversation detail
        response = integration_client.get(
            f"/api/v1/conversations/{conv_id}",
            headers=integration_auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "conversation" in data
        assert "messages" in data

def test_unauthorized_conversations_access(integration_client):
    """Test accessing conversations without authentication"""
    response = integration_client.get("/api/v1/conversations")
    
    assert response.status_code == 401
