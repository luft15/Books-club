# backend/app/schemas/booking_schema.py
from pydantic import BaseModel, Field
from datetime import time, datetime
from typing import Optional

from .event_schema import EventResponse


class BookingBase(BaseModel):
    event_id: int = Field(..., description="ID события")
    time_slot: Optional[time] = Field(None, description="Временной слот")
    comment: Optional[str] = Field(None, max_length=500, description="Комментарий")


class BookingCreate(BookingBase):
    pass


class BookingResponse(BookingBase):
    id: int
    created_at: datetime
    user_id: int
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    event: Optional[EventResponse] = None
    
    class Config:
        from_attributes = True
        