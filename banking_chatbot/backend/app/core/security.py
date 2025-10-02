# backend/app/core/security.py

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency para validar JWT y obtener usuario"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")

        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        # Buscar usuario en DB
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

# Decoradores de rol
def require_role(*allowed_roles):
    """Decorator para restringir endpoints por rol"""
    def decorator(func):
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if current_user.role not in allowed_roles:
                raise HTTPException(status_code=403, detail="Acceso denegado")
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# Uso en endpoints:
# @router.get("/admin-only")
# @require_role("admin", "supervisor")
# async def admin_endpoint():
#     ...