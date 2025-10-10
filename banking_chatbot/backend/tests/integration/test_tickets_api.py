# Integration tests for tickets API
import pytest
from fastapi.testclient import TestClient

def test_get_tickets(integration_client, integration_auth_headers):
    """Test getting list of tickets"""
    response = integration_client.get(
        "/api/v1/tickets",
        headers=integration_auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_ticket(integration_client, integration_auth_headers):
    """Test creating a new ticket"""
    ticket_data = {
        "subject": "Test Integration Ticket",
        "description": "This is a test ticket for integration testing",
        "priority": "medium",
        "category": "general"
    }
    
    response = integration_client.post(
        "/api/v1/tickets",
        json=ticket_data,
        headers=integration_auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "ticket_id" in data
    assert data["status"] == "OPEN"

def test_get_ticket_detail(integration_client, integration_auth_headers):
    """Test getting ticket details"""
    # First create a ticket
    create_response = integration_client.post(
        "/api/v1/tickets",
        json={
            "subject": "Detail Test Ticket",
            "description": "Testing ticket details",
            "priority": "high"
        },
        headers=integration_auth_headers
    )
    
    ticket_id = create_response.json()["ticket_id"]
    
    # Get ticket details
    response = integration_client.get(
        f"/api/v1/tickets/{ticket_id}",
        headers=integration_auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["ticket_id"] == ticket_id
    assert data["subject"] == "Detail Test Ticket"

def test_update_ticket_priority(integration_client, integration_auth_headers):
    """Test updating ticket priority"""
    # Create ticket
    create_response = integration_client.post(
        "/api/v1/tickets",
        json={
            "subject": "Priority Test",
            "priority": "low"
        },
        headers=integration_auth_headers
    )
    
    ticket_id = create_response.json()["ticket_id"]
    
    # Update priority
    response = integration_client.patch(
        f"/api/v1/tickets/{ticket_id}/priority",
        json={"priority": "HIGH"},
        headers=integration_auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["priority"] == "HIGH"

def test_unauthorized_ticket_access(integration_client):
    """Test accessing tickets without authentication"""
    response = integration_client.get("/api/v1/tickets")
    
    assert response.status_code == 401
