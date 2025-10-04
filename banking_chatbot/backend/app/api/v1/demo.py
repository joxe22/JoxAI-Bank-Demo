# backend/app/api/v1/demo.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories import ConversationRepository, MessageRepository, TicketRepository, UserRepository
from app.models import MessageRole, TicketStatus, TicketPriority
import uuid
import random

router = APIRouter()

@router.post("/populate-demo-data")
async def populate_demo_data(db: Session = Depends(get_db)):
    """Populate database with demo data for testing - now using PostgreSQL"""
    
    conv_repo = ConversationRepository(db)
    msg_repo = MessageRepository(db)
    ticket_repo = TicketRepository(db)
    
    conversation_ids = []
    for i in range(5):
        conv_id = str(uuid.uuid4())
        conversation_ids.append(conv_id)
        
        conversation = conv_repo.create(
            conversation_id=conv_id,
            user_id=f"customer_{i+1}",
            customer_name=f"Demo Customer {i+1}",
            customer_email=f"customer{i+1}@demo.com",
            is_escalated=False,
            is_active=True
        )
        
        topics = ['mi saldo', 'una tarjeta', 'un préstamo', 'una transferencia']
        msg_repo.create(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=f"Hola, necesito ayuda con {topics[i % 4]}"
        )
        msg_repo.create(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content="¡Por supuesto! Con gusto te ayudo. ¿Podrías darme más detalles?"
        )
        msg_repo.create(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content="Sí, necesito más información sobre esto."
        )
    
    ticket_ids = []
    priorities = [TicketPriority.LOW, TicketPriority.MEDIUM, TicketPriority.HIGH]
    categories = ["technical", "billing", "general"]
    statuses = [TicketStatus.OPEN, TicketStatus.IN_PROGRESS, TicketStatus.RESOLVED]
    
    for i in range(3):
        conv = conv_repo.get_by_conversation_id(conversation_ids[i])
        
        ticket = ticket_repo.create(
            ticket_id=f"TKT-DEMO-{i+1}",
            conversation_id=conv.id,
            customer_id=f"customer_{i+1}",
            customer_name=f"Demo Customer {i+1}",
            customer_email=f"customer{i+1}@demo.com",
            subject=f"Demo: {categories[i]} issue",
            description=f"Customer needs assistance with {categories[i]} issue",
            status=statuses[i],
            priority=priorities[i],
            category=categories[i]
        )
        ticket_ids.append(ticket.ticket_id)
        
        if i > 0:
            ticket_repo.assign_to_agent(ticket.ticket_id, agent_id=5, assigned_by=2)
    
    return {
        "success": True,
        "message": "Demo data populated successfully",
        "data": {
            "conversations_created": len(conversation_ids),
            "tickets_created": len(ticket_ids),
            "conversation_ids": conversation_ids,
            "ticket_ids": ticket_ids
        }
    }

@router.post("/clear-demo-data")
async def clear_demo_data(db: Session = Depends(get_db)):
    """Clear all demo data - WARNING: Destructive operation"""
    return {
        "success": False,
        "message": "This operation is disabled. Use database management tools to clear data."
    }

@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get current database stats - now using PostgreSQL"""
    conv_repo = ConversationRepository(db)
    ticket_repo = TicketRepository(db)
    user_repo = UserRepository(db)
    msg_repo = MessageRepository(db)
    
    all_conversations = conv_repo.get_all(limit=10000)
    all_tickets = ticket_repo.get_all(limit=10000)
    all_users = user_repo.get_all(limit=1000)
    
    total_messages = sum(msg_repo.count_by_conversation(c.id) for c in all_conversations)
    
    return {
        "conversations": len(all_conversations),
        "tickets": len(all_tickets),
        "users": len(all_users),
        "total_messages": total_messages,
        "total_ticket_messages": 0
    }
