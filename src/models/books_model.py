from typing import Optional, List
from db.db import Database


class BookModel:
    """Модель книги (Active Record) - данные + методы работы с БД"""

    def __init__(
        self,
        title: str,
        db: Database,
        author: Optional[str] = None,
        year: Optional[int] = None,
        book_id: Optional[int] = None,
    ):
        self.id = book_id
        self.title = title.strip() if title else ""
        self.author = author.strip() if author else None
        self.year = year
        self.db = db

        # Валидация при создании
        self.validate()

    def validate(self) -> None:
        """Проверка корректности полей книги"""
        errors = []

        if not self.title:
            errors.append("Название книги не может быть пустым")
        elif len(self.title) > 255:
            errors.append("Название книги не должно превышать 255 символов")

        if self.author and len(self.author) > 255:
            errors.append("Имя автора не должно превышать 255 символов")

        if self.year is not None:
            if not isinstance(self.year, int) or self.year < 0 or self.year > 2100:
                errors.append("Год издания должен быть целым числом от 0 до 2100")

        if errors:
            raise ValueError(f"Ошибки валидации: {', '.join(errors)}")

    def save(self) -> bool:
        """Сохраняет книгу (вставка или обновление)"""
        if self.id is None:
            return self._insert()
        else:
            return self._update()

    def _insert(self) -> bool:
        """Вставляет новую книгу в БД и получает сгенерированный id"""
        query = """
            INSERT INTO books (title, author, year)
            VALUES (%s, %s, %s)
            RETURNING id;
        """
        try:
            result = self.db.execute_query(query, (self.title, self.author, self.year), fetch=True)
            if result:
                self.id = result[0]["id"]
                return True
            return False
        except Exception as e:
            print(f"Ошибка при вставке книги: {e}")
            return False

    def _update(self) -> bool:
        """обновляет существующую книгу"""
        query = """
            UPDATE books
            SET title = %s, author = %s, year = %s
            WHERE id = %s;
        """
        try:
            self.db.execute_query(query, (self.title, self.author, self.year, self.id))
            return True
        except Exception as e:
            print(f"Ошибка при обновлении книги: {e}")
            return False

    def delete(self) -> bool:
        """удаляет книгу из БД"""
        if self.id is None:
            return False
        query = "DELETE FROM books WHERE id = %s;"
        try:
            self.db.execute_query(query, (self.id,))
            self.id = None
            return True
        except Exception as e:
            print(f"Ошибка при удалении книги: {e}")
            return False

    # Классовые методы для поиска
    @classmethod
    def get_by_id(self, cls, book_id: int) -> Optional["BookModel"]:
        """возвращает книгу по id или None"""
        query = "SELECT id, title, author, year FROM books WHERE id = %s;"
        result = self.db.execute_query(query, (book_id,), fetch=True)
        if not result:
            return None
        row = result[0]
        return cls(
            book_id=row["id"],
            title=row["title"],
            author=row["author"],
            year=row["year"],
        )

    @classmethod
    def get_all(self, cls) -> List["BookModel"]:
        """возвращает список всех книг"""
        query = "SELECT id, title, author, year FROM books ORDER BY id;"
        rows = self.db.execute_query(query, fetch=True)
        return [
            cls(
                book_id=row["id"],
                title=row["title"],
                author=row["author"],
                year=row["year"],
            )
            for row in rows
        ]

    @classmethod
    def get_by_author(self, cls, author: str) -> List["BookModel"]:
        """возвращает книги автора (точное совпадение)"""
        query = "SELECT id, title, author, year FROM books WHERE author = %s ORDER BY year;"
        rows = self.db.execute_query(query, (author.strip(),), fetch=True)
        return [
            cls(
                book_id=row["id"],
                title=row["title"],
                author=row["author"],
                year=row["year"],
            )
            for row in rows
        ]
