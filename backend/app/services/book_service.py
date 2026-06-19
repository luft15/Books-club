# backend/app/services/book_service.py
from sqlalchemy.orm import Session
from app.models.book_model import Book_model
from app.schemas.book_schema import BookCreate

class BookService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100, search: str | None = None):
        query = self.db.query(Book_model)
        if search:
            query = query.filter(
                Book_model.title.ilike(f"%{search}%") | Book_model.author.ilike(f"%{search}%")
            )
        return query.order_by(Book_model.title).offset(skip).limit(limit).all()

    def create(self, book_data: BookCreate) -> Book_model:
        db_book = Book_model(**book_data.dict())
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def get_by_id(self, book_id: int) -> Book_model | None:
        return self.db.query(Book_model).filter(Book_model.id == book_id).first()
