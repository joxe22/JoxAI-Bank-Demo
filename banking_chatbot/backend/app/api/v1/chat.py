# backend/app/api/v1/chat.py
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
import uuid
import json

from app.database import get_db
from app.repositories import ConversationRepository, MessageRepository, TicketRepository
from app.models import MessageRole, TicketStatus, TicketPriority
from app.core.limiter import limiter

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
@limiter.limit("10/minute")
async def start_conversation(request: Request, conv_request: StartConversationRequest, db: Session = Depends(get_db)):
    """
    Start a new conversation - now using PostgreSQL.
    Rate limit: 10 new conversations per minute per IP.
    """
    conversation_id = str(uuid.uuid4())
    
    conv_repo = ConversationRepository(db)
    msg_repo = MessageRepository(db)
    
    conversation = conv_repo.create(
        conversation_id=conversation_id,
        user_id=conv_request.user_id,
        customer_name=f"Customer {conv_request.user_id}",
        customer_email=conv_request.metadata.get("email", f"{conv_request.user_id}@customer.com"),
        is_escalated=False,
        is_active=True
    )
    
    welcome_msg = msg_repo.create(
        conversation_id=conversation.id,
        role=MessageRole.ASSISTANT,
        content="¡Hola! Soy el asistente virtual de JoxAI Bank. ¿En qué puedo ayudarte hoy? Puedo ayudarte con información sobre:\n\n• Consultas de saldo y movimientos\n• Tarjetas de crédito y recomendaciones\n• Planes financieros y ahorro\n• Transferencias y pagos\n• Y mucho más...",
        message_metadata=json.dumps({"type": "welcome"})
    )
    
    return {
        "conversation_id": conversation_id,
        "status": "started",
        "messages": [{
            "id": welcome_msg.id,
            "role": welcome_msg.role.value,
            "content": welcome_msg.content,
            "timestamp": welcome_msg.created_at.isoformat()
        }]
    }

@router.post("/message")
@limiter.limit("20/minute")
async def send_message(request: Request, msg_request: SendMessageRequest, db: Session = Depends(get_db)):
    """
    Send a message and get AI response - now using PostgreSQL.
    Rate limit: 20 messages per minute per IP to prevent API abuse.
    """
    conv_repo = ConversationRepository(db)
    msg_repo = MessageRepository(db)
    
    conversation = conv_repo.get_by_conversation_id(msg_request.conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    history = msg_repo.get_by_conversation(conversation.id)
    
    msg_repo.create(
        conversation_id=conversation.id,
        role=MessageRole.USER,
        content=msg_request.message,
        message_metadata=json.dumps(msg_request.context or {})
    )
    
    context = msg_request.context or {}
    context["history"] = [
        {
            "role": msg.role.value,
            "content": msg.content,
            "timestamp": msg.created_at.isoformat()
        }
        for msg in history
    ]
    
    ai_response = await generate_response(msg_request.message, context)
    
    msg_repo.create(
        conversation_id=conversation.id,
        role=MessageRole.ASSISTANT,
        content=ai_response["content"],
        message_metadata=json.dumps(ai_response.get("metadata", {}))
    )
    
    return {
        "message": ai_response["content"],
        "metadata": ai_response.get("metadata", {}),
        "conversation_id": msg_request.conversation_id
    }

@router.get("/history/{conversation_id}")
async def get_history(conversation_id: str, db: Session = Depends(get_db)):
    """Get conversation history - now using PostgreSQL"""
    conv_repo = ConversationRepository(db)
    msg_repo = MessageRepository(db)
    
    conversation = conv_repo.get_by_conversation_id(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = msg_repo.get_by_conversation(conversation.id)
    
    return {
        "conversation": {
            "id": conversation.conversation_id,
            "user_id": conversation.user_id,
            "is_escalated": conversation.is_escalated,
            "is_active": conversation.is_active,
            "created_at": conversation.created_at.isoformat()
        },
        "messages": [
            {
                "id": msg.id,
                "role": msg.role.value,
                "content": msg.content,
                "timestamp": msg.created_at.isoformat(),
                "metadata": json.loads(msg.message_metadata) if msg.message_metadata else {}
            }
            for msg in messages
        ]
    }

@router.post("/escalate")
async def escalate_to_agent(request: EscalateRequest, db: Session = Depends(get_db)):
    """Escalate conversation to human agent - now using PostgreSQL"""
    from app.core.websocket_manager import manager
    
    conv_repo = ConversationRepository(db)
    msg_repo = MessageRepository(db)
    ticket_repo = TicketRepository(db)
    
    conversation = conv_repo.get_by_conversation_id(request.conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    priority_map = {
        "low": TicketPriority.LOW,
        "medium": TicketPriority.MEDIUM,
        "high": TicketPriority.HIGH,
        "urgent": TicketPriority.URGENT
    }
    
    ticket = ticket_repo.create(
        ticket_id=f"TKT-{uuid.uuid4().hex[:8].upper()}",
        conversation_id=conversation.id,
        customer_id=conversation.user_id,
        customer_name=conversation.customer_name,
        customer_email=conversation.customer_email,
        subject=f"Escalation: {request.category}",
        description=request.description or "Customer requested human assistance",
        status=TicketStatus.OPEN,
        priority=priority_map.get(request.priority.lower(), TicketPriority.MEDIUM),
        category=request.category
    )
    
    conv_repo.escalate(request.conversation_id, request.description or "Customer escalation")
    
    msg_repo.create(
        conversation_id=conversation.id,
        role=MessageRole.SYSTEM,
        content=f"Tu consulta ha sido escalada a un agente humano. Te contactaremos pronto. Número de ticket: #{ticket.ticket_id}",
        message_metadata=json.dumps({"type": "escalation", "ticket_id": ticket.id})
    )
    
    ticket_dict = {
        "id": ticket.id,
        "ticket_id": ticket.ticket_id,
        "customer_name": ticket.customer_name,
        "category": ticket.category,
        "priority": ticket.priority.value,
        "status": ticket.status.value,
        "created_at": ticket.created_at.isoformat()
    }
    
    await manager.broadcast_new_ticket(ticket_dict)
    
    return {
        "ticket_id": ticket.ticket_id,
        "ticket": ticket_dict,
        "status": "escalated",
        "message": "Conversación escalada exitosamente"
    }

@router.post("/end")
async def end_conversation(request: EndConversationRequest, db: Session = Depends(get_db)):
    """End conversation - now using PostgreSQL"""
    conv_repo = ConversationRepository(db)
    
    conversation = conv_repo.get_by_conversation_id(request.conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conv_repo.close(request.conversation_id)
    
    return {
        "status": "ended",
        "conversation_id": request.conversation_id
    }

@router.post("/feedback")
async def send_feedback(request: FeedbackRequest, db: Session = Depends(get_db)):
    """Submit conversation feedback - now using PostgreSQL"""
    conv_repo = ConversationRepository(db)
    
    conversation = conv_repo.get_by_conversation_id(request.conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conv_repo.update_sentiment(request.conversation_id, request.rating)
    
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

async def generate_response(message: str, context: dict) -> dict:
    """Generate AI response using AI Service"""
    from app.services.ai_service import ai_service
    
    conversation_history = context.get("history", [])
    
    response = await ai_service.generate_response(
        message=message,
        conversation_history=conversation_history,
        system_prompt=None
    )
    
    return response
