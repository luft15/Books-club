# backend/app/schemas/token_schema.py
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from .user_schema import UserResponse


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    username: Optional[str] = None


class AdminStats(BaseModel):
    total_users: int
    total_books: int
    total_events: int
    total_bookings: int
    popular_events: List[Dict[str, Any]]
    recent_bookings: List[Dict[str, Any]]
    