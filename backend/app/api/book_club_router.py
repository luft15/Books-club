# backend/app/api/book_club_router.pyfrom fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas import (
    BookResponse, BookCreate,
    EventResponse, EventCreate,
    BookingResponse, BookingCreate,
    AdminStats
)
from app.services.book_service import BookService
from app.services.event_service import EventService
from app.services.booking_service import BookingService

from app.core.dependencies import (
    get_current_user,
    get_current_admin_user,
    get_book_service,
    get_event_service,
    get_booking_service
)
from app.models.user_model import User_model
from app.core.database import get_db

router = APIRouter(prefix="/api/book-club", tags=["book-club"])

# публичные
@router.get("/books", response_model=List[BookResponse])
def get_books(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    book_service: BookService = Depends(get_book_service)
):
    return book_service.get_all(skip, limit, search)

@router.get("/events", response_model=List[EventResponse])
def get_events(
    skip: int = 0,
    limit: int = 100,
    upcoming: bool = False,
    event_service: EventService = Depends(get_event_service)
):
    events = event_service.get_all(skip, limit, upcoming)
    for event in events:
        event.participants_count = event_service.get_participants_count(event.id)
    return events

@router.get("/events/{event_id}", response_model=EventResponse)
def get_event(event_id: int, event_service: EventService = Depends(get_event_service)):
    event = event_service.get_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    event.participants_count = event_service.get_participants_count(event_id)
    return event

@router.get("/events/{event_id}/bookings", response_model=List[BookingResponse])
def get_event_bookings(event_id: int, event_service: EventService = Depends(get_event_service)):
    event = event_service.get_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    bookings = event_service.get_bookings_for_event(event_id)
    # добавим user_name и user_email
    for b in bookings:
        b.user_name = b.user.full_name or b.user.username
        b.user_email = b.user.email
    return bookings

# защищенные (требуется авторизация)
@router.post("/bookings", response_model=BookingResponse)
def create_booking(
    booking_data: BookingCreate,
    current_user: User_model = Depends(get_current_user),
    booking_service: BookingService = Depends(get_booking_service)
):
    booking = booking_service.create_booking(booking_data, current_user.id)
    booking.user_name = current_user.full_name or current_user.username
    booking.user_email = current_user.email
    return booking

@router.delete("/bookings/{booking_id}")
def cancel_booking(
    booking_id: int,
    current_user: User_model = Depends(get_current_user),
    booking_service: BookingService = Depends(get_booking_service)
):
    result = booking_service.cancel_booking(booking_id, current_user.id, current_user.is_admin)
    if not result:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")
    return {"message": "Бронирование отменено"}

@router.get("/my-bookings", response_model=List[BookingResponse])
def get_my_bookings(
    current_user: User_model = Depends(get_current_user),
    booking_service: BookingService = Depends(get_booking_service)
):
    bookings = booking_service.get_user_bookings(current_user.id)
    for b in bookings:
        b.user_name = current_user.full_name or current_user.username
        b.user_email = current_user.email
    return bookings

# админские
@router.post("/events", response_model=EventResponse)
def create_event(
    event_data: EventCreate,
    current_user: User_model = Depends(get_current_admin_user),
    event_service: EventService = Depends(get_event_service)
):
    return event_service.create(event_data)

@router.put("/events/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    event_data: EventCreate,
    current_user: User_model = Depends(get_current_admin_user),
    event_service: EventService = Depends(get_event_service)
):
    event = event_service.update(event_id, event_data)
    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    return event

@router.delete("/events/{event_id}")
def delete_event(
    event_id: int,
    current_user: User_model = Depends(get_current_admin_user),
    event_service: EventService = Depends(get_event_service)
):
    if not event_service.delete(event_id):
        raise HTTPException(status_code=404, detail="Событие не найдено")
    return {"message": "Событие удалено"}

@router.post("/books", response_model=BookResponse)
def create_book(
    book_data: BookCreate,
    current_user: User_model = Depends(get_current_admin_user),
    book_service: BookService = Depends(get_book_service)
):
    return book_service.create(book_data)

@router.get("/admin/stats", response_model=AdminStats)
def get_admin_stats(
    current_user: User_model = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    from sqlalchemy import func, desc
    from app.models import User_model, Book_model, Event_model, Booking_model
    total_users = db.query(User_model).count()
    total_books = db.query(Book_model).count()
    total_events = db.query(Event_model).count()
    total_bookings = db.query(Booking_model).count()

    popular = db.query(
        Event_model.id, Event_model.description, Event_model.event_date,
        func.count(Booking_model.id).label("participants")
    ).join(Booking_model, Booking_model.event_id == Event_model.id)\
     .group_by(Event_model.id)\
     .order_by(desc("participants"))\
     .limit(5).all()

    recent = db.query(
        Booking_model.id, User_model.username, Event_model.description.label("event_name"), Booking_model.created_at
    ).join(User_model, User_model.id == Booking_model.user_id)\
     .join(Event_model, Event_model.id == Booking_model.event_id)\
     .order_by(desc(Booking_model.created_at))\
     .limit(10).all()

    return AdminStats(
        total_users=total_users,
        total_books=total_books,
        total_events=total_events,
        total_bookings=total_bookings,
        popular_events=[{"id": e.id, "description": e.description, "event_date": e.event_date, "participants": e.participants} for e in popular],
        recent_bookings=[{"id": b.id, "username": b.username, "event_name": b.event_name, "created_at": b.created_at} for b in recent]
    )
