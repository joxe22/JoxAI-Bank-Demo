from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, cast, String

from app.repositories.base import BaseRepository
from app.models.db_customer import Customer, CustomerStatus, CustomerType


class CustomerRepository(BaseRepository[Customer]):
    def __init__(self, db: Session):
        super().__init__(Customer, db)
    
    def get_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email address"""
        return self.db.query(self.model).filter(self.model.email == email).first()
    
    def get_by_phone(self, phone: str) -> Optional[Customer]:
        """Get customer by phone number"""
        return self.db.query(self.model).filter(self.model.phone == phone).first()
    
    def get_by_account_number(self, account_number: str) -> Optional[Customer]:
        """Get customer by account number"""
        return self.db.query(self.model).filter(self.model.account_number == account_number).first()
    
    def get_by_status(self, status: CustomerStatus, skip: int = 0, limit: int = 100) -> List[Customer]:
        """Get all customers by status"""
        return self.db.query(self.model).filter(
            self.model.status == status
        ).offset(skip).limit(limit).all()
    
    def get_by_type(self, customer_type: CustomerType, skip: int = 0, limit: int = 100) -> List[Customer]:
        """Get all customers by type"""
        return self.db.query(self.model).filter(
            self.model.customer_type == customer_type
        ).offset(skip).limit(limit).all()
    
    def get_by_assigned_agent(self, agent_id: int, skip: int = 0, limit: int = 100) -> List[Customer]:
        """Get all customers assigned to a specific agent"""
        return self.db.query(self.model).filter(
            self.model.assigned_agent_id == agent_id
        ).offset(skip).limit(limit).all()
    
    def search(
        self, 
        query: str, 
        status: Optional[CustomerStatus] = None,
        customer_type: Optional[CustomerType] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Customer]:
        """
        Search customers by name, email, phone, account number, or tags.
        Supports filtering by status and customer type.
        """
        search_filter = or_(
            self.model.full_name.ilike(f"%{query}%"),
            self.model.email.ilike(f"%{query}%"),
            self.model.phone.ilike(f"%{query}%"),
            self.model.account_number.ilike(f"%{query}%"),
            cast(self.model.tags, String).ilike(f"%{query}%")
        )
        
        filters = [search_filter]
        if status:
            filters.append(self.model.status == status)
        if customer_type:
            filters.append(self.model.customer_type == customer_type)
        
        query_obj = self.db.query(self.model)
        for f in filters:
            query_obj = query_obj.filter(f)
        
        return query_obj.offset(skip).limit(limit).all()
    
    def create_customer(
        self,
        full_name: str,
        email: str,
        created_by_id: int,
        phone: Optional[str] = None,
        account_number: Optional[str] = None,
        customer_type: CustomerType = CustomerType.INDIVIDUAL,
        status: CustomerStatus = CustomerStatus.ACTIVE,
        preferences: Optional[dict] = None,
        tags: Optional[List[str]] = None,
        notes: Optional[str] = None,
        assigned_agent_id: Optional[int] = None
    ) -> Customer:
        """Create a new customer"""
        customer = self.model(
            full_name=full_name,
            email=email,
            phone=phone,
            account_number=account_number,
            customer_type=customer_type,
            status=status,
            preferences=preferences or {},
            tags=tags or [],
            notes=notes,
            assigned_agent_id=assigned_agent_id,
            created_by_id=created_by_id
        )
        self.db.add(customer)
        self.db.flush()
        return customer
    
    def update_customer(
        self,
        customer_id: int,
        updated_by_id: int,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        account_number: Optional[str] = None,
        customer_type: Optional[CustomerType] = None,
        status: Optional[CustomerStatus] = None,
        preferences: Optional[dict] = None,
        tags: Optional[List[str]] = None,
        notes: Optional[str] = None,
        assigned_agent_id: Optional[int] = None
    ) -> Optional[Customer]:
        """Update an existing customer"""
        customer = self.get(customer_id)
        if not customer:
            return None
        
        if full_name is not None:
            customer.full_name = full_name
        if email is not None:
            customer.email = email
        if phone is not None:
            customer.phone = phone
        if account_number is not None:
            customer.account_number = account_number
        if customer_type is not None:
            customer.customer_type = customer_type
        if status is not None:
            customer.status = status
        if preferences is not None:
            customer.preferences = preferences
        if tags is not None:
            customer.tags = tags
        if notes is not None:
            customer.notes = notes
        if assigned_agent_id is not None:
            customer.assigned_agent_id = assigned_agent_id
        
        customer.updated_by_id = updated_by_id
        self.db.add(customer)
        self.db.flush()
        return customer
    
    def soft_delete(self, customer_id: int, updated_by_id: int) -> Optional[Customer]:
        """Soft delete a customer by setting status to INACTIVE"""
        customer = self.get(customer_id)
        if not customer:
            return None
        
        customer.status = CustomerStatus.INACTIVE
        customer.updated_by_id = updated_by_id
        self.db.add(customer)
        self.db.flush()
        return customer
    
    def get_active_customers(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        """Get all active customers"""
        return self.get_by_status(CustomerStatus.ACTIVE, skip, limit)
    
    def count_by_status(self, status: CustomerStatus) -> int:
        """Count customers by status"""
        return self.db.query(self.model).filter(self.model.status == status).count()
    
    def count_by_type(self, customer_type: CustomerType) -> int:
        """Count customers by type"""
        return self.db.query(self.model).filter(self.model.customer_type == customer_type).count()
