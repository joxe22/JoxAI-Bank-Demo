from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, case, extract
from datetime import datetime, timedelta

from app.models.db_conversation import DBConversation
from app.models.db_message import DBMessage, MessageRole
from app.models.db_ticket import DBTicket, TicketStatus, TicketPriority
from app.models.db_user import DBUser, UserRole
from app.models.db_customer import Customer, CustomerStatus
from app.models.db_audit_log import AuditLog
from app.repositories.base import BaseRepository


class AnalyticsRepository(BaseRepository[DBConversation]):
    def __init__(self, db: Session):
        super().__init__(DBConversation, db)
    
    def get_dashboard_overview(self) -> Dict[str, Any]:
        total_conversations = self.db.query(func.count(DBConversation.id)).scalar()
        total_tickets = self.db.query(func.count(DBTicket.id)).scalar()
        total_customers = self.db.query(func.count(Customer.id)).scalar()
        total_messages = self.db.query(func.count(DBMessage.id)).scalar()
        
        active_conversations = self.db.query(func.count(DBConversation.id)).filter(
            DBConversation.is_active == True
        ).scalar()
        
        escalated_conversations = self.db.query(func.count(DBConversation.id)).filter(
            DBConversation.is_escalated == True
        ).scalar()
        
        escalation_rate = (escalated_conversations / total_conversations * 100) if total_conversations > 0 else 0
        
        return {
            "total_conversations": total_conversations or 0,
            "active_conversations": active_conversations or 0,
            "total_tickets": total_tickets or 0,
            "total_customers": total_customers or 0,
            "total_messages": total_messages or 0,
            "escalation_rate": round(escalation_rate, 2),
        }
    
    def get_conversation_stats(self, days: int = 30) -> Dict[str, Any]:
        since_date = datetime.utcnow() - timedelta(days=days)
        
        conversations_period = self.db.query(func.count(DBConversation.id)).filter(
            DBConversation.created_at >= since_date
        ).scalar()
        
        escalated_period = self.db.query(func.count(DBConversation.id)).filter(
            and_(
                DBConversation.created_at >= since_date,
                DBConversation.is_escalated == True
            )
        ).scalar()
        
        avg_messages = self.db.query(
            func.avg(func.count(DBMessage.id))
        ).select_from(DBMessage).join(DBConversation).filter(
            DBConversation.created_at >= since_date
        ).group_by(DBMessage.conversation_id).scalar()
        
        return {
            "period_days": days,
            "total_conversations": conversations_period or 0,
            "escalated_conversations": escalated_period or 0,
            "escalation_rate": round((escalated_period / conversations_period * 100) if conversations_period > 0 else 0, 2),
            "avg_messages_per_conversation": round(float(avg_messages or 0), 2),
        }
    
    def get_ticket_stats(self) -> Dict[str, Any]:
        total_tickets = self.db.query(func.count(DBTicket.id)).scalar() or 0
        
        by_status = self.db.query(
            DBTicket.status,
            func.count(DBTicket.id).label('count')
        ).group_by(DBTicket.status).all()
        
        by_priority = self.db.query(
            DBTicket.priority,
            func.count(DBTicket.id).label('count')
        ).group_by(DBTicket.priority).all()
        
        avg_resolution_time = self.db.query(
            func.avg(
                extract('epoch', DBTicket.resolved_at - DBTicket.created_at) / 3600
            )
        ).filter(
            DBTicket.resolved_at.isnot(None)
        ).scalar()
        
        return {
            "total_tickets": total_tickets,
            "by_status": {status.value: count for status, count in by_status},
            "by_priority": {priority.value: count for priority, count in by_priority},
            "avg_resolution_hours": round(float(avg_resolution_time or 0), 2),
        }
    
    def get_agent_performance(self, agent_id: Optional[int] = None) -> Dict[str, Any]:
        query = self.db.query(
            DBUser.id,
            DBUser.full_name,
            func.count(DBTicket.id).label('total_tickets'),
            func.sum(
                case((DBTicket.status == TicketStatus.RESOLVED, 1), else_=0)
            ).label('resolved_tickets'),
            func.sum(
                case((DBTicket.status == TicketStatus.IN_PROGRESS, 1), else_=0)
            ).label('in_progress_tickets'),
        ).join(
            DBTicket, DBUser.id == DBTicket.agent_id, isouter=True
        ).filter(
            DBUser.role == UserRole.AGENT
        ).group_by(DBUser.id, DBUser.full_name)
        
        if agent_id:
            query = query.filter(DBUser.id == agent_id)
        
        results = query.all()
        
        agents_data = []
        for user_id, full_name, total, resolved, in_progress in results:
            agents_data.append({
                "agent_id": user_id,
                "agent_name": full_name,
                "total_tickets": total or 0,
                "resolved_tickets": resolved or 0,
                "in_progress_tickets": in_progress or 0,
                "resolution_rate": round((resolved / total * 100) if total and total > 0 else 0, 2),
            })
        
        return {
            "agents": agents_data,
            "total_agents": len(agents_data),
        }
    
    def get_customer_stats(self) -> Dict[str, Any]:
        total_customers = self.db.query(func.count(Customer.id)).scalar() or 0
        
        active_customers = self.db.query(func.count(Customer.id)).filter(
            Customer.status == CustomerStatus.ACTIVE
        ).scalar() or 0
        
        inactive_customers = self.db.query(func.count(Customer.id)).filter(
            Customer.status == CustomerStatus.INACTIVE
        ).scalar() or 0
        
        by_type = self.db.query(
            Customer.customer_type,
            func.count(Customer.id).label('count')
        ).group_by(Customer.customer_type).all()
        
        return {
            "total_customers": total_customers,
            "active_customers": active_customers,
            "inactive_customers": inactive_customers,
            "by_type": {ctype.value: count for ctype, count in by_type},
        }
    
    def get_activity_timeline(self, days: int = 7) -> Dict[str, Any]:
        since_date = datetime.utcnow() - timedelta(days=days)
        
        daily_conversations = self.db.query(
            func.date(DBConversation.created_at).label('date'),
            func.count(DBConversation.id).label('count')
        ).filter(
            DBConversation.created_at >= since_date
        ).group_by(func.date(DBConversation.created_at)).order_by('date').all()
        
        daily_tickets = self.db.query(
            func.date(DBTicket.created_at).label('date'),
            func.count(DBTicket.id).label('count')
        ).filter(
            DBTicket.created_at >= since_date
        ).group_by(func.date(DBTicket.created_at)).order_by('date').all()
        
        daily_messages = self.db.query(
            func.date(DBMessage.created_at).label('date'),
            func.count(DBMessage.id).label('count')
        ).filter(
            DBMessage.created_at >= since_date
        ).group_by(func.date(DBMessage.created_at)).order_by('date').all()
        
        return {
            "period_days": days,
            "conversations_timeline": [
                {"date": str(date), "count": count} for date, count in daily_conversations
            ],
            "tickets_timeline": [
                {"date": str(date), "count": count} for date, count in daily_tickets
            ],
            "messages_timeline": [
                {"date": str(date), "count": count} for date, count in daily_messages
            ],
        }
    
    def get_audit_stats(self, hours: int = 24) -> Dict[str, Any]:
        since_time = datetime.utcnow() - timedelta(hours=hours)
        
        total_actions = self.db.query(func.count(AuditLog.id)).filter(
            AuditLog.timestamp >= since_time
        ).scalar() or 0
        
        by_action = self.db.query(
            AuditLog.action,
            func.count(AuditLog.id).label('count')
        ).filter(
            AuditLog.timestamp >= since_time
        ).group_by(AuditLog.action).order_by(func.count(AuditLog.id).desc()).limit(10).all()
        
        by_status = self.db.query(
            AuditLog.status,
            func.count(AuditLog.id).label('count')
        ).filter(
            AuditLog.timestamp >= since_time
        ).group_by(AuditLog.status).all()
        
        failed_actions = self.db.query(func.count(AuditLog.id)).filter(
            and_(
                AuditLog.timestamp >= since_time,
                AuditLog.status == 'FAILURE'
            )
        ).scalar() or 0
        
        return {
            "period_hours": hours,
            "total_actions": total_actions,
            "failed_actions": failed_actions,
            "success_rate": round(((total_actions - failed_actions) / total_actions * 100) if total_actions > 0 else 100, 2),
            "top_actions": [
                {"action": action, "count": count} for action, count in by_action
            ],
            "by_status": {status: count for status, count in by_status},
        }
