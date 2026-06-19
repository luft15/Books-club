# backend/app/schemas/__init__.py
from .user_schema import UserBase, UserCreate, UserLogin, UserResponse, UserInDB
from .book_schema import BookBase, BookCreate, BookResponse
from .event_schema import EventBase, EventCreate, EventResponse
from .booking_schema import BookingBase, BookingCreate, BookingResponse
from .token_schema import Token, TokenData, AdminStats

__all__ = [
    # User
    "UserBase", "UserCreate", "UserLogin", "UserResponse", "UserInDB",
    # Book
    "BookBase", "BookCreate", "BookResponse",
    # Event
    "EventBase", "EventCreate", "EventResponse",
    # Booking
    "BookingBase", "BookingCreate", "BookingResponse",
    # Token
    "Token", "TokenData", "AdminStats"
]
