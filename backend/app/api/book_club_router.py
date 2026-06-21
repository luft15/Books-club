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
from app.services.stats_service import StatsService
from app.core.dependencies import (
    get_current_user,
    get_current_admin_user,
    get_book_service,
    get_event_service,
    get_booking_service,
    get_stats_service
)
from app.models.user_model import User_model

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
    for b in bookings:
        b.user_name = b.user.full_name or b.user.username
        b.user_email = b.user.email
    return bookings

# защищенные
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
    stats_service: StatsService = Depends(get_stats_service)
):
    stats = stats_service.get_stats()
    return AdminStats(**stats)