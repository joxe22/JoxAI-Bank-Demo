from fastapi import APIRouter, HTTPException, Depends, Request, Query
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.customer_repository import CustomerRepository
from app.models.db_customer import CustomerType, CustomerStatus
from app.core.security import verify_token
from app.core.audit import log_audit

router = APIRouter()


class CustomerCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=50)
    account_number: Optional[str] = Field(None, max_length=100)
    customer_type: CustomerType = CustomerType.INDIVIDUAL
    status: CustomerStatus = CustomerStatus.ACTIVE
    preferences: Optional[Dict[str, Any]] = Field(default_factory=dict)
    tags: Optional[List[str]] = Field(default_factory=list)
    notes: Optional[str] = None
    assigned_agent_id: Optional[int] = None


class CustomerUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    account_number: Optional[str] = Field(None, max_length=100)
    customer_type: Optional[CustomerType] = None
    status: Optional[CustomerStatus] = None
    preferences: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    assigned_agent_id: Optional[int] = None


class CustomerResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: Optional[str]
    account_number: Optional[str]
    customer_type: CustomerType
    status: CustomerStatus
    preferences: Dict[str, Any]
    tags: List[str]
    notes: Optional[str]
    assigned_agent_id: Optional[int]
    created_by_id: Optional[int]
    updated_by_id: Optional[int]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


def get_current_user_id(request: Request) -> int:
    """Extract user ID from JWT token"""
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    try:
        payload = verify_token(token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload.get("user_id", 1)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/", response_model=List[CustomerResponse])
async def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[CustomerStatus] = None,
    customer_type: Optional[CustomerType] = None,
    assigned_agent_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """List all customers with optional filtering"""
    customer_repo = CustomerRepository(db)
    
    if assigned_agent_id:
        customers = customer_repo.get_by_assigned_agent(assigned_agent_id, skip, limit)
    elif status:
        customers = customer_repo.get_by_status(status, skip, limit)
    elif customer_type:
        customers = customer_repo.get_by_type(customer_type, skip, limit)
    else:
        customers = customer_repo.get_all(skip, limit)
    
    return [
        CustomerResponse(
            id=c.id,
            full_name=c.full_name,
            email=c.email,
            phone=c.phone,
            account_number=c.account_number,
            customer_type=c.customer_type,
            status=c.status,
            preferences=c.preferences or {},
            tags=c.tags or [],
            notes=c.notes,
            assigned_agent_id=c.assigned_agent_id,
            created_by_id=c.created_by_id,
            updated_by_id=c.updated_by_id,
            created_at=c.created_at.isoformat() if c.created_at else "",
            updated_at=c.updated_at.isoformat() if c.updated_at else ""
        )
        for c in customers
    ]


@router.get("/search", response_model=List[CustomerResponse])
async def search_customers(
    q: str = Query(..., min_length=1),
    status: Optional[CustomerStatus] = None,
    customer_type: Optional[CustomerType] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Search customers by name, email, phone, account number, or tags"""
    customer_repo = CustomerRepository(db)
    customers = customer_repo.search(q, status, customer_type, skip, limit)
    
    return [
        CustomerResponse(
            id=c.id,
            full_name=c.full_name,
            email=c.email,
            phone=c.phone,
            account_number=c.account_number,
            customer_type=c.customer_type,
            status=c.status,
            preferences=c.preferences or {},
            tags=c.tags or [],
            notes=c.notes,
            assigned_agent_id=c.assigned_agent_id,
            created_by_id=c.created_by_id,
            updated_by_id=c.updated_by_id,
            created_at=c.created_at.isoformat() if c.created_at else "",
            updated_at=c.updated_at.isoformat() if c.updated_at else ""
        )
        for c in customers
    ]


@router.get("/stats/summary", response_model=dict)
async def get_customer_stats(
    *,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get customer statistics summary"""
    customer_repo = CustomerRepository(db)
    
    return {
        "total_active": customer_repo.count_by_status(CustomerStatus.ACTIVE),
        "total_inactive": customer_repo.count_by_status(CustomerStatus.INACTIVE),
        "total_suspended": customer_repo.count_by_status(CustomerStatus.SUSPENDED),
        "total_individual": customer_repo.count_by_type(CustomerType.INDIVIDUAL),
        "total_business": customer_repo.count_by_type(CustomerType.BUSINESS),
        "total": customer_repo.count()
    }


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: int,
    *,
    request: Request,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get a specific customer by ID"""
    customer_repo = CustomerRepository(db)
    customer = customer_repo.get(customer_id)
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    log_audit(
        db=db,
        user_id=user_id,
        action="CUSTOMER_VIEWED",
        resource_type="CUSTOMER",
        resource_id=str(customer_id),
        details={"full_name": customer.full_name, "email": customer.email},
        request=request
    )
    
    return CustomerResponse(
        id=customer.id,
        full_name=customer.full_name,
        email=customer.email,
        phone=customer.phone,
        account_number=customer.account_number,
        customer_type=customer.customer_type,
        status=customer.status,
        preferences=customer.preferences or {},
        tags=customer.tags or [],
        notes=customer.notes,
        assigned_agent_id=customer.assigned_agent_id,
        created_by_id=customer.created_by_id,
        updated_by_id=customer.updated_by_id,
        created_at=customer.created_at.isoformat() if customer.created_at else "",
        updated_at=customer.updated_at.isoformat() if customer.updated_at else ""
    )


@router.post("/", response_model=CustomerResponse, status_code=201)
async def create_customer(
    *,
    request: Request,
    customer_data: CustomerCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a new customer"""
    customer_repo = CustomerRepository(db)
    
    existing = customer_repo.get_by_email(customer_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Customer with this email already exists")
    
    if customer_data.account_number:
        existing_account = customer_repo.get_by_account_number(customer_data.account_number)
        if existing_account:
            raise HTTPException(status_code=400, detail="Customer with this account number already exists")
    
    try:
        customer = customer_repo.create_customer(
            full_name=customer_data.full_name,
            email=customer_data.email,
            phone=customer_data.phone,
            account_number=customer_data.account_number,
            customer_type=customer_data.customer_type,
            status=customer_data.status,
            preferences=customer_data.preferences,
            tags=customer_data.tags,
            notes=customer_data.notes,
            assigned_agent_id=customer_data.assigned_agent_id,
            created_by_id=user_id
        )
        db.commit()
        db.refresh(customer)
        
        log_audit(
            db=db,
            user_id=user_id,
            action="CUSTOMER_CREATE",
            resource_type="CUSTOMER",
            resource_id=str(customer.id),
            details={
                "full_name": customer.full_name,
                "email": customer.email,
                "customer_type": customer.customer_type.value
            },
            request=request
        )
        
        return CustomerResponse(
            id=customer.id,
            full_name=customer.full_name,
            email=customer.email,
            phone=customer.phone,
            account_number=customer.account_number,
            customer_type=customer.customer_type,
            status=customer.status,
            preferences=customer.preferences or {},
            tags=customer.tags or [],
            notes=customer.notes,
            assigned_agent_id=customer.assigned_agent_id,
            created_by_id=customer.created_by_id,
            updated_by_id=customer.updated_by_id,
            created_at=customer.created_at.isoformat() if customer.created_at else "",
            updated_at=customer.updated_at.isoformat() if customer.updated_at else ""
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create customer: {str(e)}")


@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int,
    *,
    request: Request,
    customer_data: CustomerUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update an existing customer"""
    customer_repo = CustomerRepository(db)
    
    if customer_data.email:
        existing = customer_repo.get_by_email(customer_data.email)
        if existing and existing.id != customer_id:
            raise HTTPException(status_code=400, detail="Customer with this email already exists")
    
    if customer_data.account_number:
        existing_account = customer_repo.get_by_account_number(customer_data.account_number)
        if existing_account and existing_account.id != customer_id:
            raise HTTPException(status_code=400, detail="Customer with this account number already exists")
    
    try:
        customer = customer_repo.update_customer(
            customer_id=customer_id,
            updated_by_id=user_id,
            full_name=customer_data.full_name,
            email=customer_data.email,
            phone=customer_data.phone,
            account_number=customer_data.account_number,
            customer_type=customer_data.customer_type,
            status=customer_data.status,
            preferences=customer_data.preferences,
            tags=customer_data.tags,
            notes=customer_data.notes,
            assigned_agent_id=customer_data.assigned_agent_id
        )
        
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        db.commit()
        db.refresh(customer)
        
        log_audit(
            db=db,
            user_id=user_id,
            action="CUSTOMER_UPDATE",
            resource_type="CUSTOMER",
            resource_id=str(customer.id),
            details={
                "full_name": customer.full_name,
                "email": customer.email,
                "status": customer.status.value
            },
            request=request
        )
        
        return CustomerResponse(
            id=customer.id,
            full_name=customer.full_name,
            email=customer.email,
            phone=customer.phone,
            account_number=customer.account_number,
            customer_type=customer.customer_type,
            status=customer.status,
            preferences=customer.preferences or {},
            tags=customer.tags or [],
            notes=customer.notes,
            assigned_agent_id=customer.assigned_agent_id,
            created_by_id=customer.created_by_id,
            updated_by_id=customer.updated_by_id,
            created_at=customer.created_at.isoformat() if customer.created_at else "",
            updated_at=customer.updated_at.isoformat() if customer.updated_at else ""
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update customer: {str(e)}")


@router.delete("/{customer_id}", status_code=200)
async def delete_customer(
    customer_id: int,
    *,
    request: Request,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Soft delete a customer (set status to INACTIVE)"""
    customer_repo = CustomerRepository(db)
    
    try:
        customer = customer_repo.soft_delete(customer_id, user_id)
        
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        db.commit()
        
        log_audit(
            db=db,
            user_id=user_id,
            action="CUSTOMER_DELETE",
            resource_type="CUSTOMER",
            resource_id=str(customer_id),
            details={
                "full_name": customer.full_name,
                "email": customer.email,
                "deletion_type": "soft"
            },
            request=request
        )
        
        return {"message": "Customer deactivated successfully", "customer_id": customer_id}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete customer: {str(e)}")
