# backend/app/services/event_service.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from datetime import date
from app.models.event_model import Event_model
from app.models.booking_model import Booking_model
from app.schemas.event_schema import EventCreate

class EventService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100, upcoming: bool = False):
        query = self.db.query(Event_model).options(joinedload(Event_model.book))
        if upcoming:
            query = query.filter(Event_model.event_date >= date.today())
        return query.order_by(Event_model.event_date).offset(skip).limit(limit).all()

    def get_by_id(self, event_id: int) -> Event_model | None:
        return self.db.query(Event_model).options(joinedload(Event_model.book)).filter(Event_model.id == event_id).first()

    def create(self, event_data: EventCreate) -> Event_model:
        db_event = Event_model(**event_data.dict())
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def update(self, event_id: int, event_data: EventCreate) -> Event_model | None:
        event = self.get_by_id(event_id)
        if not event:
            return None
        for key, value in event_data.dict().items():
            setattr(event, key, value)
        self.db.commit()
        self.db.refresh(event)
        return event

    def delete(self, event_id: int) -> bool:
        event = self.get_by_id(event_id)
        if not event:
            return False
        self.db.delete(event)
        self.db.commit()
        return True

    def get_participants_count(self, event_id: int) -> int:
        return self.db.query(Booking_model).filter(Booking_model.event_id == event_id).count()

    def get_bookings_for_event(self, event_id: int):
        return self.db.query(Booking_model).filter(Booking_model.event_id == event_id).all()
