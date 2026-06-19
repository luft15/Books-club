# backend/app/schemas/event_schema.py
from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional

from .book_schema import BookResponse


class EventBase(BaseModel):
    book_id: int = Field(..., description="ID книги")
    event_date: date = Field(..., description="Дата события")
    description: Optional[str] = Field(None, max_length=1000, description="Описание")
    max_participants: int = Field(20, ge=1, le=1000, description="Максимум участников")


class EventCreate(EventBase):
    @validator('event_date')
    def validate_date(cls, v):
        if v < date.today():
            raise ValueError('Дата события не может быть в прошлом')
        return v


class EventResponse(EventBase):
    id: int
    created_at: datetime
    book: Optional[BookResponse] = None
    participants_count: Optional[int] = 0
    
    class Config:
        from_attributes = True
        