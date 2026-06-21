from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.user_model import User_model
from app.models.book_model import Book_model
from app.models.event_model import Event_model
from app.models.booking_model import Booking_model

class StatsService:
    def __init__(self, db: Session):
        self.db = db

    def get_stats(self):
        total_users = self.db.query(User_model).count()
        total_books = self.db.query(Book_model).count()
        total_events = self.db.query(Event_model).count()
        total_bookings = self.db.query(Booking_model).count()

        popular = self.db.query(
            Event_model.id,
            Event_model.description,
            Event_model.event_date,
            func.count(Booking_model.id).label("participants")
        ).join(Booking_model, Booking_model.event_id == Event_model.id)\
         .group_by(Event_model.id)\
         .order_by(desc("participants"))\
         .limit(5).all()

        recent = self.db.query(
            Booking_model.id,
            User_model.username,
            Event_model.description.label("event_name"),
            Booking_model.created_at
        ).join(User_model, User_model.id == Booking_model.user_id)\
         .join(Event_model, Event_model.id == Booking_model.event_id)\
         .order_by(desc(Booking_model.created_at))\
         .limit(10).all()

        return {
            "total_users": total_users,
            "total_books": total_books,
            "total_events": total_events,
            "total_bookings": total_bookings,
            "popular_events": [
                {
                    "id": e.id,
                    "description": e.description,
                    "event_date": e.event_date,
                    "participants": e.participants
                }
                for e in popular
            ],
            "recent_bookings": [
                {
                    "id": b.id,
                    "username": b.username,
                    "event_name": b.event_name,
                    "created_at": b.created_at
                }
                for b in recent
            ]
        }
    