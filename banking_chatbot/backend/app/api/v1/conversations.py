# backend/app/api/v1/conversations.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.services.websocket_manager import WebSocketManager
from app.core.security import get_current_user_ws

router = APIRouter()
manager = WebSocketManager()

@router.websocket("/ws/admin")
async def websocket_endpoint(
        websocket: WebSocket,
        token: str
):
    """
    WebSocket para actualizaciones en tiempo real

    Frontend se conecta así:
    ws://localhost:8000/ws/admin?token=jwt_token

    Eventos que envía al frontend:
    - ticket_created
    - ticket_updated
    - new_message
    - agent_status_changed
    """
    # Validar token
    user = await get_current_user_ws(token)

    await manager.connect(websocket, user.id, user.role)

    try:
        while True:
            data = await websocket.receive_json()

            # Manejar suscripciones
            if data["type"] == "subscribe":
                if data["channel"] == "ticket":
                    await manager.subscribe_ticket(user.id, data["ticketId"])
                elif data["channel"] == "stats":
                    await manager.subscribe_stats(user.id)

            # Manejar typing indicator
            elif data["type"] == "typing":
                await manager.broadcast_typing(data["ticketId"], user.id, data["isTyping"])

    except WebSocketDisconnect:
        manager.disconnect(user.id)