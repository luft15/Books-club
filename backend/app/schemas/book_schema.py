# backend/app/schemas/book_schema.py
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500, description="Название книги")
    author: Optional[str] = Field(None, max_length=200, description="Автор")
    year: Optional[int] = Field(None, ge=0, le=datetime.now().year, description="Год издания")


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        