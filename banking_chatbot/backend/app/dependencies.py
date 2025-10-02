"""
Dependencies para FastAPI.
Aquí definimos funciones que se usan como Depends() en los endpoints.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Optional

from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User
from app.config import settings


# ==================== OAUTH2 SCHEME ====================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login"
)


# ==================== AUTH DEPENDENCIES ====================

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    """
    Dependency para obtener el usuario actual desde el JWT token.

    Se usa en endpoints así:
    @router.get("/protected")
    async def protected_route(current_user: User = Depends(get_current_user)):
        return {"user": current_user.email}

    Raises:
        HTTPException 401: Si el token es inválido o el usuario no existe
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodificar token
        payload = verify_token(token)
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Buscar usuario en DB
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    return user


async def get_current_active_user(
        current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency que verifica que el usuario esté activo.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    return current_user


# ==================== ROLE DEPENDENCIES ====================

class RoleChecker:
    """
    Clase helper para verificar roles de usuario.

    Uso:
    require_admin = RoleChecker(["admin"])

    @router.get("/admin-only")
    async def admin_route(current_user: User = Depends(require_admin)):
        ...
    """

    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Roles permitidos: {', '.join(self.allowed_roles)}"
            )
        return current_user


# Instancias pre-configuradas para usar directamente
require_admin = RoleChecker(["admin"])
require_admin_or_supervisor = RoleChecker(["admin", "supervisor"])
require_agent = RoleChecker(["admin", "supervisor", "agent"])


# ==================== PAGINATION DEPENDENCIES ====================

class PaginationParams:
    """
    Parámetros de paginación para endpoints que retornan listas.

    Uso:
    @router.get("/items")
    async def get_items(pagination: PaginationParams = Depends()):
        items = db.query(Item).offset(pagination.skip).limit(pagination.limit).all()
        ...
    """

    def __init__(
            self,
            page: int = 1,
            page_size: int = 20,
            max_page_size: int = 100
    ):
        self.page = max(1, page)
        self.page_size = min(page_size, max_page_size)
        self.skip = (self.page - 1) * self.page_size
        self.limit = self.page_size

    def get_offset(self) -> int:
        return self.skip

    def get_limit(self) -> int:
        return self.limit


# ==================== FILTER DEPENDENCIES ====================

class TicketFilters:
    """
    Filtros comunes para endpoints de tickets.

    Uso:
    @router.get("/tickets")
    async def get_tickets(filters: TicketFilters = Depends()):
        query = db.query(Ticket)
        if filters.status:
            query = query.filter(Ticket.status == filters.status)
        ...
    """

    def __init__(
            self,
            status: Optional[str] = None,
            priority: Optional[str] = None,
            category: Optional[str] = None,
            assigned_to: Optional[int] = None,
            search: Optional[str] = None,
            date_from: Optional[str] = None,
            date_to: Optional[str] = None,
            sort_by: str = "created_at",
            sort_order: str = "desc"
    ):
        self.status = status if status != "all" else None
        self.priority = priority if priority != "all" else None
        self.category = category if category != "all" else None
        self.assigned_to = assigned_to if assigned_to != "all" else None
        self.search = search
        self.date_from = date_from
        self.date_to = date_to
        self.sort_by = sort_by
        self.sort_order = sort_order