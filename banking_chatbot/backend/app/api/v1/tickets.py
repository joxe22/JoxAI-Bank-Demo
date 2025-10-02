# backend/app/api/v1/tickets.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=List[TicketResponse])
async def get_tickets(
        status: Optional[str] = None,
        priority: Optional[str] = None,
        category: Optional[str] = None,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    """
    GET /api/v1/tickets?status=open&priority=high

    Retorna tickets filtrados según rol:
    - Admin/Supervisor: todos
    - Agent: solo asignados a él
    """
    query = db.query(Ticket)

    # Filtrar por rol
    if current_user.role == "agent":
        query = query.filter(Ticket.assigned_to == current_user.id)

    if status and status != "all":
        query = query.filter(Ticket.status == status)

    if priority and priority != "all":
        query = query.filter(Ticket.priority == priority)

    tickets = query.all()

    return {
        "tickets": [t.to_dict() for t in tickets],
        "total": len(tickets)
    }

@router.post("/", response_model=TicketResponse)
async def create_ticket(
        ticket: TicketCreate,
        db: Session = Depends(get_db)
):
    """Crear nuevo ticket (escalación desde chatbot)"""
    new_ticket = Ticket(**ticket.dict())
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

@router.put("/{ticket_id}")
async def update_ticket(
        ticket_id: int,
        ticket_data: TicketUpdate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    """Actualizar ticket (cambiar estado, prioridad, asignar)"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    for key, value in ticket_data.dict(exclude_unset=True).items():
        setattr(ticket, key, value)

    db.commit()
    return ticket