# backernd/app/core/dependencies.py
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.database import get_db
from app.services.auth_service import AuthService
from app.models.user_model import User_model
from app.services.book_service import BookService
from app.services.event_service import EventService
from app.services.booking_service import BookingService
from app.services.stats_service import StatsService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service)
) -> User_model:
    user = auth_service.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_admin_user(current_user: User_model = Depends(get_current_user)) -> User_model:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

def get_book_service(db: Session = Depends(get_db)) -> BookService:
    return BookService(db)

def get_event_service(db: Session = Depends(get_db)) -> EventService:
    return EventService(db)

def get_booking_service(db: Session = Depends(get_db)) -> BookingService:
    return BookingService(db)

def get_stats_service(db: Session = Depends(get_db)) -> StatsService:
    return StatsService(db)

