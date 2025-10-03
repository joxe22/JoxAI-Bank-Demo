# backend/app/api/v1/conversations.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_manager import manager
import uuid

router = APIRouter()

@router.websocket("/ws/admin")
async def websocket_endpoint(websocket: WebSocket, token: str = None):
    """
    WebSocket endpoint for real-time updates in admin panel
    """
    connection_id = str(uuid.uuid4())
    user_id = 1  # For now, default to admin user
    
    try:
        await manager.connect(websocket, user_id, connection_id)
        
        # Send welcome message
        await manager.send_personal_message({
            "type": "connected",
            "message": "Connected to admin WebSocket"
        }, connection_id)
        
        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_json()
            
            # Handle different message types
            if data.get("type") == "ping":
                await manager.send_personal_message({
                    "type": "pong"
                }, connection_id)
            
            elif data.get("type") == "subscribe":
                # Handle subscription requests
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
async def get_conversations(status: str = None, limit: int = 50):
    """Get all conversations"""
    from app.services.data_store import data_store
    
    conversations = list(data_store.conversations.values())
    
    if status:
        conversations = [c for c in conversations if c["status"] == status]
    
    # Sort by updated_at descending
    conversations.sort(key=lambda x: x["updated_at"], reverse=True)
    
    # Limit results
    conversations = conversations[:limit]
    
    return {
        "conversations": conversations,
        "total": len(conversations)
    }

@router.get("/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation details with messages"""
    from app.services.data_store import data_store
    
    conversation = data_store.get_conversation(conversation_id)
    if not conversation:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = data_store.get_messages(conversation_id)
    
    return {
        "conversation": conversation,
        "messages": messages
    }
