# backend/app/services/booking_service.py
from sqlalchemy.orm import Session, joinedload
from app.models.booking_model import Booking_model
from app.models.event_model import Event_model
from app.schemas.booking_schema import BookingCreate
from fastapi import HTTPException, status

class BookingService:
    def __init__(self, db: Session):
        self.db = db

    def create_booking(self, booking_data: BookingCreate, user_id: int) -> Booking_model:
        # Проверка события
        event = self.db.query(Event_model).filter(Event_model.id == booking_data.event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Событие не найдено")

        # Проверка, не записан ли уже
        existing = self.db.query(Booking_model).filter(
            Booking_model.event_id == booking_data.event_id,
            Booking_model.user_id == user_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Вы уже записаны на это событие")

        # Проверка мест
        current_count = self.db.query(Booking_model).filter(Booking_model.event_id == booking_data.event_id).count()
        if current_count >= event.max_participants:
            raise HTTPException(status_code=400, detail="Нет свободных мест")

        db_booking = Booking_model(
            event_id=booking_data.event_id,
            user_id=user_id,
            time_slot=booking_data.time_slot,
            comment=booking_data.comment
        )
        self.db.add(db_booking)
        self.db.commit()
        self.db.refresh(db_booking)
        return db_booking

    def cancel_booking(self, booking_id: int, user_id: int, is_admin: bool = False) -> bool:
        booking = self.db.query(Booking_model).filter(Booking_model.id == booking_id).first()
        if not booking:
            return False
        if not is_admin and booking.user_id != user_id:
            raise HTTPException(status_code=403, detail="Нет прав на отмену")
        self.db.delete(booking)
        self.db.commit()
        return True

    def get_user_bookings(self, user_id: int):
        return self.db.query(Booking_model).options(
            joinedload(Booking_model.event),
            joinedload(Booking_model.event).joinedload(Event_model.book)
        ).filter(Booking_model.user_id == user_id).all()
    