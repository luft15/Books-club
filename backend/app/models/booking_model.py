# backend/app/booking_model.py
from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Booking_model(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    time_slot = Column(Time, nullable=True)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Связи
    event = relationship("Event_model", back_populates="bookings")
    user = relationship("User_model", back_populates="bookings")