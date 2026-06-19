# backend/app/event_model.py
from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Event_model(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    event_date = Column(Date, nullable=False)
    description = Column(Text, nullable=True)
    max_participants = Column(Integer, default=20)
    created_at = Column(DateTime, server_default=func.now())
    
    # Связи
    book = relationship("Book_model", back_populates="events")
    bookings = relationship("Booking_model", back_populates="event", cascade="all, delete-orphan")
