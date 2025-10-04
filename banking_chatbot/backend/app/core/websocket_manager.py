from typing import Dict, List, Set
from fastapi import WebSocket
import json
import asyncio
from datetime import datetime


class ConnectionManager:
    """Manages WebSocket connections for real-time updates."""
    
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}
        self.role_connections: Dict[str, Set[WebSocket]] = {
            "ADMIN": set(),
            "SUPERVISOR": set(),
            "AGENT": set()
        }
    
    async def connect(self, websocket: WebSocket, user_id: int, role: str):
        """Accept and register a new WebSocket connection."""
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        
        self.active_connections[user_id].append(websocket)
        
        if role in self.role_connections:
            self.role_connections[role].add(websocket)
        
        await self.send_personal_message(
            json.dumps({
                "type": "connection_established",
                "message": "Connected to real-time updates",
                "timestamp": datetime.utcnow().isoformat()
            }),
            websocket
        )
    
    def disconnect(self, websocket: WebSocket, user_id: int, role: str):
        """Remove a WebSocket connection."""
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        
        if role in self.role_connections:
            self.role_connections[role].discard(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific WebSocket connection."""
        try:
            await websocket.send_text(message)
        except Exception as e:
            print(f"Error sending message to websocket: {e}")
    
    async def send_to_user(self, user_id: int, message: dict):
        """Send a message to all connections of a specific user."""
        if user_id not in self.active_connections:
            return
        
        message_str = json.dumps(message)
        disconnected = []
        
        for connection in self.active_connections[user_id]:
            try:
                await connection.send_text(message_str)
            except Exception as e:
                print(f"Error sending to user {user_id}: {e}")
                disconnected.append(connection)
        
        for connection in disconnected:
            self.active_connections[user_id].remove(connection)
    
    async def send_to_role(self, role: str, message: dict):
        """Send a message to all users with a specific role."""
        if role not in self.role_connections:
            return
        
        message_str = json.dumps(message)
        disconnected = []
        
        for connection in list(self.role_connections[role]):
            try:
                await connection.send_text(message_str)
            except Exception as e:
                print(f"Error sending to role {role}: {e}")
                disconnected.append(connection)
        
        for connection in disconnected:
            self.role_connections[role].discard(connection)
    
    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients."""
        message_str = json.dumps(message)
        
        for user_connections in self.active_connections.values():
            for connection in user_connections:
                try:
                    await connection.send_text(message_str)
                except Exception as e:
                    print(f"Error broadcasting: {e}")
    
    async def notify_ticket_created(self, ticket_data: dict):
        """Notify about new ticket creation."""
        message = {
            "type": "ticket_created",
            "data": ticket_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.send_to_role("ADMIN", message)
        await self.send_to_role("SUPERVISOR", message)
    
    async def notify_ticket_assigned(self, ticket_data: dict, agent_id: int):
        """Notify agent about ticket assignment."""
        message = {
            "type": "ticket_assigned",
            "data": ticket_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.send_to_user(agent_id, message)
        await self.send_to_role("ADMIN", message)
        await self.send_to_role("SUPERVISOR", message)
    
    async def notify_ticket_status_changed(self, ticket_data: dict):
        """Notify about ticket status change."""
        message = {
            "type": "ticket_status_changed",
            "data": ticket_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if ticket_data.get("assigned_to"):
            await self.send_to_user(ticket_data["assigned_to"], message)
        
        await self.send_to_role("ADMIN", message)
        await self.send_to_role("SUPERVISOR", message)
    
    async def notify_new_message(self, message_data: dict, conversation_id: str):
        """Notify about new message in conversation."""
        message = {
            "type": "new_message",
            "data": message_data,
            "conversation_id": conversation_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast(message)
    
    async def notify_escalation(self, conversation_data: dict):
        """Notify about conversation escalation."""
        message = {
            "type": "conversation_escalated",
            "data": conversation_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.send_to_role("ADMIN", message)
        await self.send_to_role("SUPERVISOR", message)
        await self.send_to_role("AGENT", message)
    
    def get_connection_stats(self) -> dict:
        """Get statistics about active connections."""
        total_connections = sum(len(conns) for conns in self.active_connections.values())
        
        return {
            "total_connections": total_connections,
            "unique_users": len(self.active_connections),
            "connections_by_role": {
                role: len(conns) for role, conns in self.role_connections.items()
            }
        }


manager = ConnectionManager()
