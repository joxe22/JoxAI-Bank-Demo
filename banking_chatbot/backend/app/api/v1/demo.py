# backend/app/api/v1/demo.py
from fastapi import APIRouter
from app.services.data_store import data_store
import uuid
from datetime import datetime, timedelta
import random

router = APIRouter()

@router.post("/populate-demo-data")
async def populate_demo_data():
    """Populate database with demo data for testing"""
    
    # Create some demo conversations
    conversation_ids = []
    for i in range(5):
        conv_id = str(uuid.uuid4())
        conversation_ids.append(conv_id)
        
        data_store.create_conversation(
            conversation_id=conv_id,
            user_id=f"customer_{i+1}",
            metadata={"source": "web-widget", "demo": True}
        )
        
        # Add some messages
        data_store.add_message(conv_id, "user", f"Hola, necesito ayuda con {['mi saldo', 'una tarjeta', 'un préstamo', 'una transferencia'][i % 4]}")
        data_store.add_message(conv_id, "assistant", "¡Por supuesto! Con gusto te ayudo. ¿Podrías darme más detalles?")
        data_store.add_message(conv_id, "user", "Sí, necesito más información sobre esto.")
    
    # Create some demo tickets from conversations
    ticket_ids = []
    priorities = ["low", "medium", "high", "urgent"]
    categories = ["technical", "billing", "general", "account"]
    statuses = ["open", "assigned", "in_progress", "resolved"]
    
    for i in range(3):
        ticket = data_store.create_ticket(
            conversation_id=conversation_ids[i],
            category=random.choice(categories),
            priority=priorities[i % 4],
            description=f"Customer needs assistance with {categories[i % 4]} issue",
            metadata={"demo": True}
        )
        ticket_ids.append(ticket["id"])
        
        # Update some tickets to different statuses
        if i > 0:
            data_store.update_ticket(ticket["id"], {"status": statuses[i % 4]})
        
        # Assign some tickets to agents
        if i > 0:
            data_store.update_ticket(ticket["id"], {
                "assigned_to": 2 if i == 1 else 3,
                "assigned_to_name": "Agent Smith" if i == 1 else "Supervisor Rodriguez"
            })
        
        # Add some messages to tickets
        data_store.add_ticket_message(
            ticket_id=ticket["id"],
            sender_id=2,
            sender_name="Agent Smith",
            content="Hi! I'm reviewing your case and will help you shortly.",
            is_internal=False
        )
    
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
async def clear_demo_data():
    """Clear all demo data"""
    data_store.conversations.clear()
    data_store.tickets.clear()
    data_store.messages.clear()
    data_store.ticket_messages.clear()
    data_store.next_ticket_id = 1
    
    return {
        "success": True,
        "message": "All demo data cleared"
    }

@router.get("/stats")
async def get_stats():
    """Get current database stats"""
    return {
        "conversations": len(data_store.conversations),
        "tickets": len(data_store.tickets),
        "users": len(data_store.users),
        "total_messages": sum(len(msgs) for msgs in data_store.messages.values()),
        "total_ticket_messages": sum(len(msgs) for msgs in data_store.ticket_messages.values())
    }
