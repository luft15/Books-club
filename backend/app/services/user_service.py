# app/services/user_service.py
from sqlalchemy.orm import Session
from app.models.user_model import User_model
from app.schemas.user_schema import UserCreate
from app.core.crypto import get_password_hash

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> User_model | None:
        return self.db.query(User_model).filter(User_model.username == username).first()

    def get_by_email(self, email: str) -> User_model | None:
        return self.db.query(User_model).filter(User_model.email == email).first()

    def create_user(self, user_data: UserCreate) -> User_model:
        hashed = get_password_hash(user_data.password)
        db_user = User_model(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed,
            full_name=user_data.full_name,
            phone=user_data.phone,
            is_admin=False
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_by_id(self, user_id: int) -> User_model | None:
        return self.db.query(User_model).filter(User_model.id == user_id).first()
    