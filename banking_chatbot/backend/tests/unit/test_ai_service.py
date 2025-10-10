# Unit tests for AI service
import pytest
import os
from app.services.ai_service import AIService

@pytest.mark.asyncio
async def test_mock_ai_service(monkeypatch):
    """Test mock AI service provider"""
    monkeypatch.setenv("AI_PROVIDER", "mock")
    service = AIService()
    
    response = await service.generate_response(
        message="What is my account balance?",
        conversation_history=[]
    )
    
    assert response is not None
    assert isinstance(response, dict)
    assert "content" in response
    assert len(response["content"]) > 0

@pytest.mark.asyncio
async def test_ai_service_auto_detection(monkeypatch):
    """Test AI service provider auto-detection"""
    # Clear all provider env vars
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("AI_PROVIDER", raising=False)
    
    service = AIService()
    
    # Should default to mock when no keys available
    assert service.provider == "mock"

@pytest.mark.asyncio
async def test_ai_service_with_conversation_history(monkeypatch):
    """Test AI service with conversation history"""
    monkeypatch.setenv("AI_PROVIDER", "mock")
    service = AIService()
    
    conversation_history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi! How can I help you today?"}
    ]
    
    response = await service.generate_response(
        message="What's my balance?",
        conversation_history=conversation_history
    )
    
    assert response is not None
    assert isinstance(response, dict)
    assert "content" in response

@pytest.mark.asyncio
async def test_ai_service_with_custom_system_prompt(monkeypatch):
    """Test AI service with custom system prompt"""
    monkeypatch.setenv("AI_PROVIDER", "mock")
    service = AIService()
    
    custom_prompt = "You are a helpful banking assistant"
    
    response = await service.generate_response(
        message="Hello",
        system_prompt=custom_prompt
    )
    
    assert response is not None
    assert isinstance(response, dict)
    assert "content" in response
