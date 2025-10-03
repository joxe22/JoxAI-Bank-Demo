# WebSocket connection manager
from fastapi import WebSocket
from typing import Dict, Set
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_connections: Dict[int, Set[str]] = {}  # user_id -> connection_ids
    
    async def connect(self, websocket: WebSocket, user_id: int, connection_id: str):
        """Accept and store a WebSocket connection"""
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        
        if user_id not in self.user_connections:
            self.user_connections[user_id] = set()
        self.user_connections[user_id].add(connection_id)
        
        print(f"WebSocket connected: user_id={user_id}, connection_id={connection_id}")
    
    def disconnect(self, connection_id: str, user_id: int = None):
        """Remove a WebSocket connection"""
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
        
        if user_id and user_id in self.user_connections:
            self.user_connections[user_id].discard(connection_id)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
        
        print(f"WebSocket disconnected: connection_id={connection_id}")
    
    async def send_personal_message(self, message: dict, connection_id: str):
        """Send a message to a specific connection"""
        if connection_id in self.active_connections:
            try:
                websocket = self.active_connections[connection_id]
                await websocket.send_json(message)
            except Exception as e:
                print(f"Error sending message to {connection_id}: {e}")
                self.disconnect(connection_id)
    
    async def send_to_user(self, message: dict, user_id: int):
        """Send a message to all connections of a user"""
        if user_id in self.user_connections:
            connection_ids = list(self.user_connections[user_id])
            for connection_id in connection_ids:
                await self.send_personal_message(message, connection_id)
    
    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients"""
        connection_ids = list(self.active_connections.keys())
        for connection_id in connection_ids:
            try:
                websocket = self.active_connections[connection_id]
                await websocket.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to {connection_id}: {e}")
                self.disconnect(connection_id)
    
    async def broadcast_ticket_update(self, ticket: dict):
        """Broadcast ticket update to all admin connections"""
        message = {
            "type": "ticket_update",
            "data": ticket
        }
        await self.broadcast(message)
    
    async def broadcast_new_ticket(self, ticket: dict):
        """Broadcast new ticket to all admin connections"""
        message = {
            "type": "new_ticket",
            "data": ticket
        }
        await self.broadcast(message)
    
    async def broadcast_message(self, ticket_id: int, message_data: dict):
        """Broadcast new message in a ticket"""
        message = {
            "type": "new_message",
            "ticket_id": ticket_id,
            "data": message_data
        }
        await self.broadcast(message)

# Global manager instance
manager = ConnectionManager()
