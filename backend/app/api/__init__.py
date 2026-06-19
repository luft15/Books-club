# backend/app/api/__init__.py
from .auth_router import router as auth_router
from .book_club_router import router as book_club_router

__all__ = ["auth_router", "book_club_router"]
