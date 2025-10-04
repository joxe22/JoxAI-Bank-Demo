"""
Ticket repository for database operations.
"""

from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session, joinedload

from app.models.db_ticket import DBTicket, TicketStatus, TicketPriority
from app.repositories.base import BaseRepository


class TicketRepository(BaseRepository[DBTicket]):
    """Repository for Ticket operations"""

    def __init__(self, db: Session):
        super().__init__(DBTicket, db)

    def get_by_ticket_id(self, ticket_id: str) -> Optional[DBTicket]:
        """Get ticket by ticket_id"""
        return self.get_by(ticket_id=ticket_id)

    def get_with_conversation(self, ticket_id: str) -> Optional[DBTicket]:
        """Get ticket with conversation loaded"""
        return (
            self.db.query(DBTicket)
            .options(joinedload(DBTicket.conversation))
            .filter(DBTicket.ticket_id == ticket_id)
            .first()
        )

    def get_with_agent(self, ticket_id: str) -> Optional[DBTicket]:
        """Get ticket with agent loaded"""
        return (
            self.db.query(DBTicket)
            .options(joinedload(DBTicket.agent))
            .filter(DBTicket.ticket_id == ticket_id)
            .first()
        )

    def get_by_status(
        self, status: TicketStatus, skip: int = 0, limit: int = 100
    ) -> List[DBTicket]:
        """Get tickets by status"""
        return self.get_all(skip=skip, limit=limit, status=status)

    def get_by_priority(
        self, priority: TicketPriority, skip: int = 0, limit: int = 100
    ) -> List[DBTicket]:
        """Get tickets by priority"""
        return self.get_all(skip=skip, limit=limit, priority=priority)

    def get_by_agent(
        self, agent_id: int, skip: int = 0, limit: int = 100
    ) -> List[DBTicket]:
        """Get tickets assigned to an agent"""
        return self.get_all(skip=skip, limit=limit, agent_id=agent_id)

    def get_by_customer(
        self, customer_id: str, skip: int = 0, limit: int = 100
    ) -> List[DBTicket]:
        """Get tickets for a customer"""
        return self.get_all(skip=skip, limit=limit, customer_id=customer_id)

    def get_unassigned(self, skip: int = 0, limit: int = 100) -> List[DBTicket]:
        """Get unassigned tickets"""
        return (
            self.db.query(DBTicket)
            .filter(DBTicket.agent_id == None)
            .order_by(DBTicket.priority.desc(), DBTicket.created_at.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def assign_to_agent(
        self, ticket_id: str, agent_id: int, assigned_by: int
    ) -> Optional[DBTicket]:
        """Assign ticket to an agent"""
        ticket = self.get_by_ticket_id(ticket_id)
        if ticket:
            return self.update(
                ticket.id,
                agent_id=agent_id,
                assigned_by=assigned_by,
                assigned_at=datetime.utcnow(),
                status=TicketStatus.IN_PROGRESS,
            )
        return None

    def update_status(
        self, ticket_id: str, status: TicketStatus
    ) -> Optional[DBTicket]:
        """Update ticket status"""
        ticket = self.get_by_ticket_id(ticket_id)
        if ticket:
            data = {"status": status}
            if status == TicketStatus.RESOLVED:
                data["resolved_at"] = datetime.utcnow()
            return self.update(ticket.id, **data)
        return None

    def update_priority(
        self, ticket_id: str, priority: TicketPriority
    ) -> Optional[DBTicket]:
        """Update ticket priority"""
        ticket = self.get_by_ticket_id(ticket_id)
        if ticket:
            return self.update(ticket.id, priority=priority)
        return None

    def resolve(
        self, ticket_id: str, resolution_notes: str
    ) -> Optional[DBTicket]:
        """Resolve a ticket"""
        ticket = self.get_by_ticket_id(ticket_id)
        if ticket:
            return self.update(
                ticket.id,
                status=TicketStatus.RESOLVED,
                resolved_at=datetime.utcnow(),
                resolution_notes=resolution_notes,
            )
        return None

    def close(self, ticket_id: str) -> Optional[DBTicket]:
        """Close a ticket"""
        ticket = self.get_by_ticket_id(ticket_id)
        if ticket:
            return self.update(ticket.id, status=TicketStatus.CLOSED)
        return None

    def get_open_count(self) -> int:
        """Get count of open tickets"""
        return self.count(status=TicketStatus.OPEN)

    def get_in_progress_count(self) -> int:
        """Get count of in-progress tickets"""
        return self.count(status=TicketStatus.IN_PROGRESS)

    def get_urgent_count(self) -> int:
        """Get count of urgent tickets"""
        return self.count(priority=TicketPriority.URGENT)
