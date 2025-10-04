# backend/app/api/v1/conversations.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.websocket_manager import manager
from app.database import get_db
from app.repositories import ConversationRepository, MessageRepository
import uuid

router = APIRouter()

@router.websocket("/ws/admin")
async def websocket_endpoint(websocket: WebSocket, token: str = None):
    """WebSocket endpoint for real-time updates in admin panel"""
    connection_id = str(uuid.uuid4())
    user_id = 1
    
    try:
        await manager.connect(websocket, user_id, connection_id)
        
        await manager.send_personal_message({
            "type": "connected",
            "message": "Connected to admin WebSocket"
        }, connection_id)
        
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "ping":
                await manager.send_personal_message({
                    "type": "pong"
                }, connection_id)
            
            elif data.get("type") == "subscribe":
                await manager.send_personal_message({
                    "type": "subscribed",
                    "channel": data.get("channel")
                }, connection_id)
    
    except WebSocketDisconnect:
        manager.disconnect(connection_id, user_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(connection_id, user_id)

@router.get("/")
async def get_conversations(status: str = None, limit: int = 50, db: Session = Depends(get_db)):
    """Get all conversations - now using PostgreSQL"""
    conv_repo = ConversationRepository(db)
    
    if status == "active":
        conversations = conv_repo.get_active_conversations(limit=limit)
    elif status == "escalated":
        conversations = conv_repo.get_escalated_conversations(limit=limit)
    else:
        conversations = conv_repo.get_all(limit=limit)
    
    conversations_list = [
        {
            "id": c.conversation_id,
            "user_id": c.user_id,
            "status": "active" if c.is_active else "ended",
            "escalated": c.is_escalated,
            "created_at": c.created_at.isoformat(),
            "updated_at": c.updated_at.isoformat()
        }
        for c in conversations
    ]
    
    return {
        "conversations": conversations_list,
        "total": len(conversations_list)
    }

@router.get("/{conversation_id}")
async def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """Get conversation details with messages - now using PostgreSQL"""
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
            "status": "active" if conversation.is_active else "ended",
            "escalated": conversation.is_escalated,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat()
        },
        "messages": [
            {
                "id": msg.id,
                "role": msg.role.value,
                "content": msg.content,
                "timestamp": msg.created_at.isoformat()
            }
            for msg in messages
        ]
    }
