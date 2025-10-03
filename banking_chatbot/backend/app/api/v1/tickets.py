# backend/app/api/v1/tickets.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.services.data_store import data_store
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

@router.get("/")
async def get_tickets(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None
):
    """Get all tickets with optional filters"""
    tickets = data_store.get_all_tickets(status, priority, category)
    return {
        "tickets": tickets,
        "total": len(tickets)
    }

@router.get("/{ticket_id}")
async def get_ticket(ticket_id: int):
    """Get ticket by ID"""
    ticket = data_store.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.post("/")
async def create_ticket(ticket_data: dict):
    """Create a new ticket"""
    # This endpoint is typically called by the chat escalation
    # but can also be used to create tickets manually
    ticket = data_store.create_ticket(
        conversation_id=ticket_data.get("conversation_id", "manual"),
        category=ticket_data.get("category", "general"),
        priority=ticket_data.get("priority", "medium"),
        description=ticket_data.get("description", ""),
        metadata=ticket_data.get("metadata", {})
    )
    
    # Broadcast new ticket to all admin connections
    await manager.broadcast_new_ticket(ticket)
    
    return ticket

@router.put("/{ticket_id}")
async def update_ticket(ticket_id: int, ticket_data: TicketUpdate):
    """Update ticket"""
    ticket = data_store.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    updates = ticket_data.model_dump(exclude_unset=True)
    
    # If assigning to agent, get agent name
    if "assigned_to" in updates and updates["assigned_to"]:
        agent = data_store.get_user_by_id(updates["assigned_to"])
        if agent:
            updates["assigned_to_name"] = agent["name"]
    
    updated_ticket = data_store.update_ticket(ticket_id, updates)
    
    # Broadcast update
    await manager.broadcast_ticket_update(updated_ticket)
    
    return updated_ticket

@router.post("/{ticket_id}/assign")
async def assign_ticket(ticket_id: int, request: AssignRequest):
    """Assign ticket to agent"""
    ticket = data_store.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    agent = data_store.get_user_by_id(request.agentId)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    updated_ticket = data_store.update_ticket(ticket_id, {
        "assigned_to": request.agentId,
        "assigned_to_name": agent["name"],
        "status": "assigned"
    })
    
    await manager.broadcast_ticket_update(updated_ticket)
    
    return updated_ticket

@router.patch("/{ticket_id}/status")
async def change_status(ticket_id: int, request: StatusRequest):
    """Change ticket status"""
    ticket = data_store.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    updated_ticket = data_store.update_ticket(ticket_id, {"status": request.status})
    await manager.broadcast_ticket_update(updated_ticket)
    
    return updated_ticket

@router.patch("/{ticket_id}/priority")
async def change_priority(ticket_id: int, request: PriorityRequest):
    """Change ticket priority"""
    ticket = data_store.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    updated_ticket = data_store.update_ticket(ticket_id, {"priority": request.priority})
    await manager.broadcast_ticket_update(updated_ticket)
    
    return updated_ticket

@router.get("/{ticket_id}/messages")
async def get_messages(ticket_id: int):
    """Get messages for a ticket"""
    ticket = data_store.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    messages = data_store.get_ticket_messages(ticket_id)
    return {
        "messages": messages,
        "conversation_history": ticket.get("conversation_history", [])
    }

@router.post("/{ticket_id}/messages")
async def send_message(ticket_id: int, request: MessageRequest):
    """Send a message to ticket"""
    ticket = data_store.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # For now, use a default user (in real app, get from auth)
    message = data_store.add_ticket_message(
        ticket_id=ticket_id,
        sender_id=1,
        sender_name="Agent",
        content=request.message,
        is_internal=False
    )
    
    await manager.broadcast_message(ticket_id, message)
    
    return message

@router.post("/{ticket_id}/notes")
async def add_note(ticket_id: int, request: NoteRequest):
    """Add internal note to ticket"""
    ticket = data_store.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    note = data_store.add_ticket_message(
        ticket_id=ticket_id,
        sender_id=1,
        sender_name="Agent",
        content=request.note,
        is_internal=True
    )
    
    return note

@router.get("/{ticket_id}/history")
async def get_history(ticket_id: int):
    """Get ticket history"""
    ticket = data_store.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return {
        "ticket": ticket,
        "conversation_history": ticket.get("conversation_history", []),
        "messages": data_store.get_ticket_messages(ticket_id)
    }

@router.get("/statistics")
async def get_statistics(period: str = "week"):
    """Get ticket statistics"""
    all_tickets = data_store.get_all_tickets()
    
    stats = {
        "total": len(all_tickets),
        "open": len([t for t in all_tickets if t["status"] == "open"]),
        "assigned": len([t for t in all_tickets if t["status"] == "assigned"]),
        "in_progress": len([t for t in all_tickets if t["status"] == "in_progress"]),
        "resolved": len([t for t in all_tickets if t["status"] == "resolved"]),
        "closed": len([t for t in all_tickets if t["status"] == "closed"]),
        "by_priority": {
            "low": len([t for t in all_tickets if t["priority"] == "low"]),
            "medium": len([t for t in all_tickets if t["priority"] == "medium"]),
            "high": len([t for t in all_tickets if t["priority"] == "high"]),
            "urgent": len([t for t in all_tickets if t["priority"] == "urgent"])
        },
        "by_category": {}
    }
    
    # Count by category
    for ticket in all_tickets:
        category = ticket.get("category", "general")
        stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
    
    return stats
