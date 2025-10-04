from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, HTTPException
from typing import Optional
import json

from app.core.websocket_manager import manager
from app.core.security import verify_token

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: Optional[str] = Query(None)
):
    """
    WebSocket endpoint for real-time updates.
    Requires JWT token as query parameter: /ws?token=<jwt_token>
    """
    
    if not token:
        await websocket.close(code=4001, reason="Authentication required")
        return
    
    try:
        payload = verify_token(token)
        user_id = payload.get("user_id")
        role = payload.get("role", "AGENT")
        
        if not user_id:
            await websocket.close(code=4002, reason="Invalid token: user_id missing")
            return
        
    except Exception as e:
        await websocket.close(code=4003, reason="Invalid token")
        return
    
    await manager.connect(websocket, user_id, role)
    
    try:
        while True:
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                message_type = message.get("type")
                
                if message_type == "ping":
                    await manager.send_personal_message(
                        json.dumps({"type": "pong", "timestamp": message.get("timestamp")}),
                        websocket
                    )
                
                elif message_type == "get_stats":
                    if role in ["ADMIN", "SUPERVISOR"]:
                        stats = manager.get_connection_stats()
                        await manager.send_personal_message(
                            json.dumps({"type": "stats", "data": stats}),
                            websocket
                        )
                
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    json.dumps({"type": "error", "message": "Invalid JSON"}),
                    websocket
                )
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id, role)
    
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, user_id, role)


@router.get("/ws/stats")
async def get_websocket_stats():
    """Get WebSocket connection statistics (public endpoint for monitoring)."""
    return manager.get_connection_stats()
