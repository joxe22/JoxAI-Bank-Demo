# backend/app/api/v1/chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import uuid
from app.services.data_store import data_store

router = APIRouter()

class StartConversationRequest(BaseModel):
    user_id: str
    metadata: Optional[dict] = {}

class SendMessageRequest(BaseModel):
    conversation_id: str
    message: str
    context: Optional[dict] = {}

class EscalateRequest(BaseModel):
    conversation_id: str
    category: Optional[str] = "general"
    priority: Optional[str] = "medium"
    description: Optional[str] = ""
    metadata: Optional[dict] = {}

class EndConversationRequest(BaseModel):
    conversation_id: str
    feedback: Optional[dict] = None

class FeedbackRequest(BaseModel):
    conversation_id: str
    rating: int
    comment: Optional[str] = ""

@router.post("/start")
async def start_conversation(request: StartConversationRequest):
    """Start a new conversation"""
    conversation_id = str(uuid.uuid4())
    conversation = data_store.create_conversation(
        conversation_id=conversation_id,
        user_id=request.user_id,
        metadata=request.metadata
    )
    
    # Add welcome message
    data_store.add_message(
        conversation_id=conversation_id,
        role="assistant",
        content="¡Hola! Soy el asistente virtual de JoxAI Bank. ¿En qué puedo ayudarte hoy? Puedo ayudarte con información sobre:\n\n• Consultas de saldo y movimientos\n• Tarjetas de crédito y recomendaciones\n• Planes financieros y ahorro\n• Transferencias y pagos\n• Y mucho más...",
        metadata={"type": "welcome"}
    )
    
    return {
        "conversation_id": conversation_id,
        "status": "started",
        "messages": data_store.get_messages(conversation_id)
    }

@router.post("/message")
async def send_message(request: SendMessageRequest):
    """Send a message and get AI response"""
    conversation = data_store.get_conversation(request.conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Get conversation history BEFORE adding new message (avoid duplication)
    history = data_store.get_messages(request.conversation_id)
    
    # Add user message
    data_store.add_message(
        conversation_id=request.conversation_id,
        role="user",
        content=request.message,
        metadata=request.context or {}
    )
    
    # Create context dict safely with history (without current message)
    context = request.context or {}
    context["history"] = history
    
    # Generate AI response using AI service
    ai_response = await generate_response(request.message, context)
    
    # Add assistant message
    data_store.add_message(
        conversation_id=request.conversation_id,
        role="assistant",
        content=ai_response["content"],
        metadata=ai_response.get("metadata", {})
    )
    
    return {
        "message": ai_response["content"],
        "metadata": ai_response.get("metadata", {}),
        "conversation_id": request.conversation_id
    }

@router.get("/history/{conversation_id}")
async def get_history(conversation_id: str):
    """Get conversation history"""
    conversation = data_store.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = data_store.get_messages(conversation_id)
    return {
        "conversation": conversation,
        "messages": messages
    }

@router.post("/escalate")
async def escalate_to_agent(request: EscalateRequest):
    """Escalate conversation to human agent"""
    from app.services.websocket_manager import manager
    
    conversation = data_store.get_conversation(request.conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Create ticket from conversation
    ticket = data_store.create_ticket(
        conversation_id=request.conversation_id,
        category=request.category,
        priority=request.priority,
        description=request.description or "Customer requested human assistance",
        metadata=request.metadata
    )
    
    # Add escalation message
    data_store.add_message(
        conversation_id=request.conversation_id,
        role="system",
        content="Tu consulta ha sido escalada a un agente humano. Te contactaremos pronto. Número de ticket: #" + str(ticket["id"]),
        metadata={"type": "escalation", "ticket_id": ticket["id"]}
    )
    
    # Broadcast new ticket to all admin connections
    await manager.broadcast_new_ticket(ticket)
    
    return {
        "ticket_id": ticket["id"],
        "ticket": ticket,
        "status": "escalated",
        "message": "Conversación escalada exitosamente"
    }

@router.post("/end")
async def end_conversation(request: EndConversationRequest):
    """End conversation"""
    conversation = data_store.get_conversation(request.conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conversation["status"] = "ended"
    if request.feedback:
        conversation["feedback"] = request.feedback
    
    return {
        "status": "ended",
        "conversation_id": request.conversation_id
    }

@router.post("/feedback")
async def send_feedback(request: FeedbackRequest):
    """Submit conversation feedback"""
    conversation = data_store.get_conversation(request.conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conversation["feedback"] = {
        "rating": request.rating,
        "comment": request.comment
    }
    
    return {
        "status": "success",
        "message": "Feedback received"
    }

@router.get("/config")
async def get_widget_config():
    """Get widget configuration"""
    return {
        "theme": {
            "primaryColor": "#5B9BD5",
            "secondaryColor": "#2F5F8F",
            "textColor": "#333333"
        },
        "features": {
            "fileUpload": False,
            "voiceInput": False,
            "quickReplies": True,
            "escalation": True
        },
        "quickReplies": [
            "Consultar saldo",
            "Tarjetas de crédito",
            "Hacer una transferencia",
            "Hablar con un agente"
        ],
        "welcomeMessage": "¡Bienvenido a JoxAI Bank!"
    }

# Helper function to generate AI responses using AI service
async def generate_response(message: str, context: dict) -> dict:
    """Generate AI response using AI Service (supports Anthropic, OpenAI, and mock)"""
    from app.services.ai_service import ai_service
    
    # Get conversation history for context
    conversation_history = context.get("history", [])
    
    # Generate response using AI service
    response = await ai_service.generate_response(
        message=message,
        conversation_history=conversation_history,
        system_prompt=None  # Uses default banking prompt
    )
    
    return response
