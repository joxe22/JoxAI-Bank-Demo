from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.core.security import verify_token
from app.core.limiter import limiter
from app.repositories import AnalyticsRepository

router = APIRouter()


def get_current_user(request: Request) -> dict:
    """Extract user info from JWT token"""
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    try:
        payload = verify_token(token)
        return payload
    except Exception:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")


@router.get("/dashboard")
@limiter.limit("30/minute")
async def get_dashboard_overview(
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive dashboard overview with key metrics.
    """
    analytics_repo = AnalyticsRepository(db)
    return analytics_repo.get_dashboard_overview()


@router.get("/conversations")
@limiter.limit("30/minute")
async def get_conversation_stats(
    request: Request,
    days: int = Query(default=30, ge=1, le=365, description="Number of days to analyze"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get conversation statistics for the specified period.
    Includes total conversations, escalation rate, and average messages per conversation.
    """
    analytics_repo = AnalyticsRepository(db)
    return analytics_repo.get_conversation_stats(days=days)


@router.get("/tickets")
@limiter.limit("30/minute")
async def get_ticket_stats(
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get ticket statistics including breakdown by status, priority,
    and average resolution time.
    """
    analytics_repo = AnalyticsRepository(db)
    return analytics_repo.get_ticket_stats()


@router.get("/agents/performance")
@limiter.limit("30/minute")
async def get_agent_performance(
    request: Request,
    agent_id: Optional[int] = Query(default=None, description="Specific agent ID to analyze"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get agent performance metrics including tickets handled,
    resolution rates, and current workload.
    
    If agent_id is provided, returns stats for that specific agent.
    Otherwise, returns stats for all agents.
    """
    # Only admins and supervisors can view all agents' performance
    if agent_id is None and current_user.get("role") not in ["ADMIN", "SUPERVISOR"]:
        # Agents can only view their own performance
        agent_id = current_user.get("user_id")
    
    analytics_repo = AnalyticsRepository(db)
    return analytics_repo.get_agent_performance(agent_id=agent_id)


@router.get("/customers")
@limiter.limit("30/minute")
async def get_customer_stats(
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get customer statistics including total customers,
    active/inactive breakdown, and customer type distribution.
    """
    analytics_repo = AnalyticsRepository(db)
    return analytics_repo.get_customer_stats()


@router.get("/timeline")
@limiter.limit("30/minute")
async def get_activity_timeline(
    request: Request,
    days: int = Query(default=7, ge=1, le=90, description="Number of days for timeline"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get activity timeline showing daily aggregations of conversations,
    tickets, and messages for the specified period.
    
    Useful for dashboard charts and trend analysis.
    """
    analytics_repo = AnalyticsRepository(db)
    return analytics_repo.get_activity_timeline(days=days)


@router.get("/audit")
@limiter.limit("30/minute")
async def get_audit_stats(
    request: Request,
    hours: int = Query(default=24, ge=1, le=168, description="Number of hours to analyze"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get audit log statistics including total actions, top actions,
    success rate, and failed actions for the specified time period.
    
    Only accessible to admins and supervisors.
    """
    if current_user.get("role") not in ["ADMIN", "SUPERVISOR"]:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Not authorized to view audit statistics")
    
    analytics_repo = AnalyticsRepository(db)
    return analytics_repo.get_audit_stats(hours=hours)
