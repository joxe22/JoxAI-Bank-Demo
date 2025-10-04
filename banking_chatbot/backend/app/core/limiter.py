# backend/app/core/limiter.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

def get_limiter():
    """Get the shared limiter instance for use in routers"""
    return limiter
