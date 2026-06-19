# backend/app/services/auth_service.py
from sqlalchemy.orm import Session
from app.models.user_model import User_model
from app.schemas.user_schema import UserLogin, UserCreate
from app.core.crypto import verify_password, create_access_token, get_password_hash
from app.services.user_service import UserService

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)

    def authenticate(self, username: str, password: str):
        user = self.user_service.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def login(self, login_data: UserLogin):
        user = self.authenticate(login_data.username, login_data.password)
        if not user:
            return None
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, 
                "token_type": "bearer", 
                "user": user
                }

    def register(self, user_data: UserCreate):
        return self.user_service.create_user(user_data)

    def get_current_user(self, token: str):
        from jose import JWTError, jwt
        from app.core.config import settings
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username = payload.get("sub")
            if username is None:
                return None
            return self.user_service.get_by_username(username)
        except JWTError:
            return None
