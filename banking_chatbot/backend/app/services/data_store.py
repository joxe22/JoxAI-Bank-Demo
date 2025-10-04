# In-memory data store for conversations, tickets, and users
from datetime import datetime
from typing import Dict, List, Optional
from threading import Lock

class DataStore:
    def __init__(self):
        self.lock = Lock()
        self.conversations: Dict[str, dict] = {}
        self.tickets: Dict[int, dict] = {}
        self.messages: Dict[str, List[dict]] = {}  # conversation_id -> messages
        self.ticket_messages: Dict[int, List[dict]] = {}  # ticket_id -> messages
        self.users: Dict[int, dict] = {
            1: {
                "id": 1,
                "name": "Admin User",
                "email": "admin@joxai.com",
                "role": "admin",
                "hashed_password": "$2b$12$wKnLWCwRSbpJinhpFRGLAuJtyF3PacEgvpvIEJD5hzOYK8iytWsKW"  # admin123
            },
            2: {
                "id": 2,
                "name": "Agent Smith",
                "email": "agent@joxai.com",
                "role": "agent",
                "hashed_password": "$2b$12$wKnLWCwRSbpJinhpFRGLAuJtyF3PacEgvpvIEJD5hzOYK8iytWsKW"  # admin123
            },
            3: {
                "id": 3,
                "name": "Supervisor Rodriguez",
                "email": "supervisor@joxai.com",
                "role": "supervisor",
                "hashed_password": "$2b$12$wKnLWCwRSbpJinhpFRGLAuJtyF3PacEgvpvIEJD5hzOYK8iytWsKW"  # admin123
            }
        }
        self.next_ticket_id = 1
        
    # Conversation methods
    def create_conversation(self, conversation_id: str, user_id: str, metadata: dict) -> dict:
        with self.lock:
            conversation = {
                "id": conversation_id,
                "user_id": user_id,
                "status": "active",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": metadata,
                "escalated": False
            }
            self.conversations[conversation_id] = conversation
            self.messages[conversation_id] = []
            return conversation
    
    def get_conversation(self, conversation_id: str) -> Optional[dict]:
        return self.conversations.get(conversation_id)
    
    def add_message(self, conversation_id: str, role: str, content: str, metadata: dict = None) -> dict:
        with self.lock:
            message = {
                "id": f"msg_{len(self.messages.get(conversation_id, []))}",
                "conversation_id": conversation_id,
                "role": role,  # user, assistant, system
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            if conversation_id not in self.messages:
                self.messages[conversation_id] = []
            self.messages[conversation_id].append(message)
            return message
    
    def get_messages(self, conversation_id: str) -> List[dict]:
        return self.messages.get(conversation_id, [])
    
    # Ticket methods
    def create_ticket(self, conversation_id: str, category: str, priority: str, description: str, metadata: dict) -> dict:
        with self.lock:
            ticket_id = self.next_ticket_id
            self.next_ticket_id += 1
            
            conversation = self.conversations.get(conversation_id, {})
            
            ticket = {
                "id": ticket_id,
                "conversation_id": conversation_id,
                "customer_id": conversation.get("user_id"),
                "customer_name": f"Customer {conversation.get('user_id', 'Unknown')}",
                "customer_email": f"{conversation.get('user_id', 'unknown')}@customer.com",
                "category": category,
                "priority": priority,
                "status": "open",
                "subject": f"Escalation: {category}",
                "description": description,
                "assigned_to": None,
                "assigned_to_name": None,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": metadata,
                "tags": [category, priority],
                "conversation_history": self.messages.get(conversation_id, [])
            }
            self.tickets[ticket_id] = ticket
            self.ticket_messages[ticket_id] = []
            
            # Mark conversation as escalated
            if conversation_id in self.conversations:
                self.conversations[conversation_id]["escalated"] = True
                self.conversations[conversation_id]["ticket_id"] = ticket_id
            
            return ticket
    
    def get_ticket(self, ticket_id: int) -> Optional[dict]:
        return self.tickets.get(ticket_id)
    
    def get_all_tickets(self, status: str = None, priority: str = None, category: str = None) -> List[dict]:
        tickets = list(self.tickets.values())
        
        if status:
            tickets = [t for t in tickets if t["status"] == status]
        if priority:
            tickets = [t for t in tickets if t["priority"] == priority]
        if category:
            tickets = [t for t in tickets if t["category"] == category]
        
        # Sort by created_at descending
        tickets.sort(key=lambda x: x["created_at"], reverse=True)
        return tickets
    
    def update_ticket(self, ticket_id: int, updates: dict) -> Optional[dict]:
        with self.lock:
            if ticket_id not in self.tickets:
                return None
            self.tickets[ticket_id].update(updates)
            self.tickets[ticket_id]["updated_at"] = datetime.now().isoformat()
            return self.tickets[ticket_id]
    
    def add_ticket_message(self, ticket_id: int, sender_id: int, sender_name: str, content: str, is_internal: bool = False) -> dict:
        with self.lock:
            message = {
                "id": f"tmsg_{len(self.ticket_messages.get(ticket_id, []))}",
                "ticket_id": ticket_id,
                "sender_id": sender_id,
                "sender_name": sender_name,
                "content": content,
                "is_internal": is_internal,
                "timestamp": datetime.now().isoformat()
            }
            if ticket_id not in self.ticket_messages:
                self.ticket_messages[ticket_id] = []
            self.ticket_messages[ticket_id].append(message)
            return message
    
    def get_ticket_messages(self, ticket_id: int) -> List[dict]:
        return self.ticket_messages.get(ticket_id, [])
    
    # User methods
    def get_user_by_email(self, email: str) -> Optional[dict]:
        for user in self.users.values():
            if user["email"] == email:
                return user
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        return self.users.get(user_id)

# Global instance
data_store = DataStore()
