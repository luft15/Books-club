# backend/app/book.py
from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Book_model(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    author = Column(String(200), nullable=True)
    year = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Связь с событиями
    events = relationship("Event_model", back_populates="book", cascade="all, delete-orphan")
