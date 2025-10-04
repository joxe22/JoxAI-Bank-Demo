# backend/app/api/v1/tickets.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.repositories import TicketRepository, UserRepository, ConversationRepository, MessageRepository
from app.models import TicketStatus, TicketPriority, MessageRole
from app.services.websocket_manager import manager

router = APIRouter()

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[int] = None
    category: Optional[str] = None

class MessageRequest(BaseModel):
    message: str

class AssignRequest(BaseModel):
    agentId: int

class StatusRequest(BaseModel):
    status: str

class PriorityRequest(BaseModel):
    priority: str

class NoteRequest(BaseModel):
    note: str

@router.get("/statistics")
async def get_statistics(period: str = "week", db: Session = Depends(get_db)):
    """Get ticket statistics - now using PostgreSQL"""
    ticket_repo = TicketRepository(db)
    
    all_tickets = ticket_repo.get_all()
    
    stats = {
        "total": len(all_tickets),
        "open": ticket_repo.get_open_count(),
        "in_progress": ticket_repo.get_in_progress_count(),
        "resolved": ticket_repo.count(status=TicketStatus.RESOLVED),
        "closed": ticket_repo.count(status=TicketStatus.CLOSED),
        "by_priority": {
            "low": ticket_repo.count(priority=TicketPriority.LOW),
            "medium": ticket_repo.count(priority=TicketPriority.MEDIUM),
            "high": ticket_repo.count(priority=TicketPriority.HIGH),
            "urgent": ticket_repo.get_urgent_count()
        },
        "by_category": {}
    }
    
    for ticket in all_tickets:
        category = ticket.category or "general"
        stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
    
    return stats

@router.get("/")
async def get_tickets(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all tickets with optional filters - now using PostgreSQL"""
    ticket_repo = TicketRepository(db)
    
    filters = {}
    if status:
        status_map = {
            "open": TicketStatus.OPEN,
            "in_progress": TicketStatus.IN_PROGRESS,
            "resolved": TicketStatus.RESOLVED,
            "closed": TicketStatus.CLOSED
        }
        filters["status"] = status_map.get(status.lower())
    
    if priority:
        priority_map = {
            "low": TicketPriority.LOW,
            "medium": TicketPriority.MEDIUM,
            "high": TicketPriority.HIGH,
            "urgent": TicketPriority.URGENT
        }
        filters["priority"] = priority_map.get(priority.lower())
    
    if category:
        filters["category"] = category
    
    tickets = ticket_repo.get_all(**filters)
    
    ticket_list = [
        {
            "id": t.id,
            "ticket_id": t.ticket_id,
            "customer_name": t.customer_name,
            "customer_email": t.customer_email,
            "subject": t.subject,
            "status": t.status.value,
            "priority": t.priority.value,
            "category": t.category,
            "assigned_to": t.agent_id,
            "created_at": t.created_at.isoformat(),
            "updated_at": t.updated_at.isoformat()
        }
        for t in tickets
    ]
    
    return {
        "tickets": ticket_list,
        "total": len(ticket_list)
    }

@router.get("/{ticket_id}")
async def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    """Get ticket by ID - now using PostgreSQL"""
    ticket_repo = TicketRepository(db)
    ticket = ticket_repo.get_by_ticket_id(ticket_id)
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return {
        "id": ticket.id,
        "ticket_id": ticket.ticket_id,
        "conversation_id": ticket.conversation_id,
        "customer_id": ticket.customer_id,
        "customer_name": ticket.customer_name,
        "customer_email": ticket.customer_email,
        "subject": ticket.subject,
        "description": ticket.description,
        "status": ticket.status.value,
        "priority": ticket.priority.value,
        "category": ticket.category,
        "assigned_to": ticket.agent_id,
        "created_at": ticket.created_at.isoformat(),
        "updated_at": ticket.updated_at.isoformat()
    }

@router.post("/")
async def create_ticket(ticket_data: dict, db: Session = Depends(get_db)):
    """Create a new ticket - now using PostgreSQL"""
    ticket_repo = TicketRepository(db)
    
    priority_map = {
        "low": TicketPriority.LOW,
        "medium": TicketPriority.MEDIUM,
        "high": TicketPriority.HIGH,
        "urgent": TicketPriority.URGENT
    }
    
    ticket = ticket_repo.create(
        ticket_id=f"TKT-{uuid.uuid4().hex[:8].upper()}",
        conversation_id=ticket_data.get("conversation_id"),
        customer_id=ticket_data.get("customer_id", "manual"),
        customer_name=ticket_data.get("customer_name", "Manual Customer"),
        customer_email=ticket_data.get("customer_email"),
        subject=ticket_data.get("subject", "Manual Ticket"),
        description=ticket_data.get("description", ""),
        status=TicketStatus.OPEN,
        priority=priority_map.get(ticket_data.get("priority", "medium").lower(), TicketPriority.MEDIUM),
        category=ticket_data.get("category", "general")
    )
    
    ticket_dict = {
        "id": ticket.id,
        "ticket_id": ticket.ticket_id,
        "customer_name": ticket.customer_name,
        "status": ticket.status.value,
        "priority": ticket.priority.value,
        "created_at": ticket.created_at.isoformat()
    }
    
    await manager.broadcast_new_ticket(ticket_dict)
    
    return ticket_dict

@router.put("/{ticket_id}")
async def update_ticket(ticket_id: str, ticket_data: TicketUpdate, db: Session = Depends(get_db)):
    """Update ticket - now using PostgreSQL"""
    ticket_repo = TicketRepository(db)
    user_repo = UserRepository(db)
    
    ticket = ticket_repo.get_by_ticket_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    updates = ticket_data.model_dump(exclude_unset=True)
    update_kwargs = {}
    
    if "status" in updates:
        status_map = {
            "open": TicketStatus.OPEN,
            "in_progress": TicketStatus.IN_PROGRESS,
            "resolved": TicketStatus.RESOLVED,
            "closed": TicketStatus.CLOSED
        }
        update_kwargs["status"] = status_map.get(updates["status"].lower())
    
    if "priority" in updates:
        priority_map = {
            "low": TicketPriority.LOW,
            "medium": TicketPriority.MEDIUM,
            "high": TicketPriority.HIGH,
            "urgent": TicketPriority.URGENT
        }
        update_kwargs["priority"] = priority_map.get(updates["priority"].lower())
    
    if "assigned_to" in updates:
        update_kwargs["agent_id"] = updates["assigned_to"]
    
    if "category" in updates:
        update_kwargs["category"] = updates["category"]
    
    updated_ticket = ticket_repo.update(ticket.id, **update_kwargs)
    
    ticket_dict = {
        "id": updated_ticket.id,
        "ticket_id": updated_ticket.ticket_id,
        "status": updated_ticket.status.value,
        "priority": updated_ticket.priority.value,
        "updated_at": updated_ticket.updated_at.isoformat()
    }
    
    await manager.broadcast_ticket_update(ticket_dict)
    
    return ticket_dict

@router.post("/{ticket_id}/assign")
async def assign_ticket(ticket_id: str, request: AssignRequest, db: Session = Depends(get_db)):
    """Assign ticket to agent - now using PostgreSQL"""
    ticket_repo = TicketRepository(db)
    user_repo = UserRepository(db)
    
    ticket = ticket_repo.get_by_ticket_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    agent = user_repo.get(request.agentId)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    updated_ticket = ticket_repo.assign_to_agent(ticket_id, request.agentId, 1)
    
    ticket_dict = {
        "id": updated_ticket.id,
        "ticket_id": updated_ticket.ticket_id,
        "assigned_to": updated_ticket.agent_id,
        "assigned_to_name": agent.full_name,
        "status": updated_ticket.status.value
    }
    
    await manager.broadcast_ticket_update(ticket_dict)
    
    return ticket_dict

@router.patch("/{ticket_id}/status")
async def change_status(ticket_id: str, request: StatusRequest, db: Session = Depends(get_db)):
    """Change ticket status - now using PostgreSQL"""
    ticket_repo = TicketRepository(db)
    
    ticket = ticket_repo.get_by_ticket_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    status_map = {
        "open": TicketStatus.OPEN,
        "in_progress": TicketStatus.IN_PROGRESS,
        "resolved": TicketStatus.RESOLVED,
        "closed": TicketStatus.CLOSED
    }
    
    updated_ticket = ticket_repo.update_status(ticket_id, status_map.get(request.status.lower(), TicketStatus.OPEN))
    
    ticket_dict = {
        "id": updated_ticket.id,
        "ticket_id": updated_ticket.ticket_id,
        "status": updated_ticket.status.value
    }
    
    await manager.broadcast_ticket_update(ticket_dict)
    
    return ticket_dict

@router.patch("/{ticket_id}/priority")
async def change_priority(ticket_id: str, request: PriorityRequest, db: Session = Depends(get_db)):
    """Change ticket priority - now using PostgreSQL"""
    ticket_repo = TicketRepository(db)
    
    ticket = ticket_repo.get_by_ticket_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    priority_map = {
        "low": TicketPriority.LOW,
        "medium": TicketPriority.MEDIUM,
        "high": TicketPriority.HIGH,
        "urgent": TicketPriority.URGENT
    }
    
    updated_ticket = ticket_repo.update_priority(ticket_id, priority_map.get(request.priority.lower(), TicketPriority.MEDIUM))
    
    ticket_dict = {
        "id": updated_ticket.id,
        "ticket_id": updated_ticket.ticket_id,
        "priority": updated_ticket.priority.value
    }
    
    await manager.broadcast_ticket_update(ticket_dict)
    
    return ticket_dict

@router.get("/{ticket_id}/messages")
async def get_messages(ticket_id: str, db: Session = Depends(get_db)):
    """Get messages for a ticket - now using PostgreSQL"""
    ticket_repo = TicketRepository(db)
    msg_repo = MessageRepository(db)
    conv_repo = ConversationRepository(db)
    
    ticket = ticket_repo.get_by_ticket_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    conversation_messages = msg_repo.get_by_conversation(ticket.conversation_id)
    
    return {
        "messages": [],
        "conversation_history": [
            {
                "role": msg.role.value,
                "content": msg.content,
                "timestamp": msg.created_at.isoformat()
            }
            for msg in conversation_messages
        ]
    }

@router.post("/{ticket_id}/messages")
async def send_message(ticket_id: str, request: MessageRequest, db: Session = Depends(get_db)):
    """Send a message to ticket - now using PostgreSQL"""
    ticket_repo = TicketRepository(db)
    
    ticket = ticket_repo.get_by_ticket_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    message_dict = {
        "id": 0,
        "sender_name": "Agent",
        "content": request.message,
        "is_internal": False,
        "timestamp": "now"
    }
    
    await manager.broadcast_message(ticket.id, message_dict)
    
    return message_dict

@router.post("/{ticket_id}/notes")
async def add_note(ticket_id: str, request: NoteRequest, db: Session = Depends(get_db)):
    """Add internal note to ticket - now using PostgreSQL"""
    ticket_repo = TicketRepository(db)
    
    ticket = ticket_repo.get_by_ticket_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    note_dict = {
        "id": 0,
        "sender_name": "Agent",
        "content": request.note,
        "is_internal": True,
        "timestamp": "now"
    }
    
    return note_dict

@router.get("/{ticket_id}/history")
async def get_history(ticket_id: str, db: Session = Depends(get_db)):
    """Get ticket history - now using PostgreSQL"""
    ticket_repo = TicketRepository(db)
    msg_repo = MessageRepository(db)
    
    ticket = ticket_repo.get_with_conversation(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    conversation_messages = msg_repo.get_by_conversation(ticket.conversation_id)
    
    return {
        "ticket": {
            "id": ticket.id,
            "ticket_id": ticket.ticket_id,
            "status": ticket.status.value,
            "priority": ticket.priority.value,
            "created_at": ticket.created_at.isoformat()
        },
        "conversation_history": [
            {
                "role": msg.role.value,
                "content": msg.content,
                "timestamp": msg.created_at.isoformat()
            }
            for msg in conversation_messages
        ],
        "messages": []
    }
