# End-to-end test for complete chat to ticket flow
import pytest
from fastapi.testclient import TestClient

@pytest.mark.asyncio
async def test_complete_chat_escalation_flow(integration_client, integration_auth_headers):
    """
    Test complete flow: Chat start → AI response → Escalation → Ticket creation
    
    This E2E test validates the entire customer journey from starting a chat
    conversation to escalating it to a human agent ticket.
    """
    
    # Step 1: Start a new chat conversation
    start_chat_response = integration_client.post(
        "/api/v1/chat/start",
        json={"user_id": "test_e2e_user"}
    )
    
    assert start_chat_response.status_code == 200
    chat_data = start_chat_response.json()
    conversation_id = chat_data["conversation_id"]
    
    # Step 2: Send a message and get AI response
    message_response = integration_client.post(
        "/api/v1/chat/message",
        json={
            "conversation_id": conversation_id,
            "message": "I need help with my account"
        }
    )
    
    assert message_response.status_code == 200
    message_data = message_response.json()
    assert "response" in message_data
    
    # Step 3: Escalate to human agent (triggers ticket creation)
    escalate_response = integration_client.post(
        "/api/v1/chat/escalate",
        json={
            "conversation_id": conversation_id,
            "reason": "Customer needs account assistance"
        }
    )
    
    assert escalate_response.status_code == 200
    escalate_data = escalate_response.json()
    assert "ticket_id" in escalate_data
    
    # Step 4: Verify ticket was created
    ticket_id = escalate_data["ticket_id"]
    ticket_response = integration_client.get(
        f"/api/v1/tickets/{ticket_id}",
        headers=integration_auth_headers
    )
    
    assert ticket_response.status_code == 200
    ticket_data = ticket_response.json()
    assert ticket_data["status"] in ["OPEN", "open"]
    assert ticket_data["conversation_id"] == conversation_id

@pytest.mark.asyncio
async def test_ticket_assignment_flow(integration_client, integration_auth_headers):
    """
    Test ticket assignment and status update flow
    
    This validates the agent workflow for taking ownership of escalated tickets.
    """
    
    # Step 1: Create a ticket
    create_response = integration_client.post(
        "/api/v1/tickets",
        json={
            "subject": "E2E Test Ticket Assignment",
            "description": "Testing agent assignment",
            "priority": "high"
        },
        headers=integration_auth_headers
    )
    
    assert create_response.status_code == 200
    ticket_data = create_response.json()
    ticket_id = ticket_data["ticket_id"]
    
    # Step 2: Get user ID from auth headers for assignment
    me_response = integration_client.get(
        "/api/v1/auth/me",
        headers=integration_auth_headers
    )
    agent_id = me_response.json()["id"]
    
    # Step 3: Assign ticket to agent
    assign_response = integration_client.post(
        f"/api/v1/tickets/{ticket_id}/assign",
        json={"agentId": agent_id},
        headers=integration_auth_headers
    )
    
    assert assign_response.status_code == 200
    assign_data = assign_response.json()
    assert assign_data["assigned_to"] == agent_id
    
    # Step 4: Update ticket status
    status_response = integration_client.patch(
        f"/api/v1/tickets/{ticket_id}/status",
        json={"status": "RESOLVED", "resolution_notes": "Issue resolved via testing"},
        headers=integration_auth_headers
    )
    
    assert status_response.status_code == 200
    status_data = status_response.json()
    assert status_data["status"] == "RESOLVED"

@pytest.mark.asyncio
async def test_knowledge_base_search_flow(integration_client, integration_auth_headers):
    """
    Test knowledge base article creation and search
    
    This validates the knowledge management system for agent support.
    """
    
    # Step 1: Create a knowledge base article
    create_response = integration_client.post(
        "/api/v1/knowledge",
        json={
            "title": "How to Reset Password",
            "content": "To reset your password: 1. Click 'Forgot Password' 2. Enter your email 3. Check your inbox",
            "category": "account_management",
            "tags": ["password", "reset", "account"]
        },
        headers=integration_auth_headers
    )
    
    if create_response.status_code == 200:
        article_id = create_response.json()["id"]
        
        # Step 2: Search for the article
        search_response = integration_client.get(
            "/api/v1/knowledge/search",
            params={"q": "password reset"},
            headers=integration_auth_headers
        )
        
        assert search_response.status_code == 200
        search_results = search_response.json()
        assert len(search_results) > 0
        
        # Step 3: Get article details
        detail_response = integration_client.get(
            f"/api/v1/knowledge/{article_id}",
            headers=integration_auth_headers
        )
        
        assert detail_response.status_code == 200
        article = detail_response.json()
        assert article["title"] == "How to Reset Password"
