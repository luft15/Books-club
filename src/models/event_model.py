from typing import Optional, List, Dict, Any
from datetime import date
from db.db import Database


class EventModel:
    """модель события"""

    def __init__(
        self,
        db: Database,
        book_id: Optional[int] = None,
        event_date: Optional[str] = None,  # будет преобразовываться в date при валидации
        description: Optional[str] = None,
        max_participants: int = 20,
        event_id: Optional[int] = None,
        created_at: Optional[str] = None,
        book_title: Optional[str] = None,  # для денормализации при запросах с JOIN
        book_author: Optional[str] = None,
        book_year: Optional[int] = None,
    ):
        self.id = event_id
        self.book_id = book_id
        self.event_date = event_date  # строка в формате YYYY-MM-DD
        self.description = description.strip() if description else None
        self.max_participants = max_participants
        self.created_at = created_at
        # дополнительные поля для информации о книге (не сохраняются в БД напрямую)
        self.book_title = book_title
        self.book_author = book_author
        self.book_year = book_year
        self.db = db

        if book_id is not None and event_date is not None:
            self.validate()

    def validate(self) -> None:
        """проверяет корректность полей события"""
        errors = []

        if not isinstance(self.book_id, int) or self.book_id <= 0:
            errors.append("ID книги должен быть положительным числом")

        # проверка даты
        if not self.event_date:
            errors.append("Дата события не может быть пустой")
        else:
            try:
                # пытаемся распарсить дату в формате YYYY-MM-DD
                date.fromisoformat(self.event_date)
            except ValueError:
                errors.append("Дата должна быть в формате YYYY-MM-DD")

        if not isinstance(self.max_participants, int) or self.max_participants < 1:
            errors.append("Максимальное количество участников должно быть положительным числом")

        if self.description and len(self.description) > 500:
            errors.append("Описание не должно превышать 500 символов")

        if errors:
            raise ValueError(f"Ошибки валидации: {', '.join(errors)}")

    def save(self) -> bool:
        """сохраняет событие (вставка или обновление)"""
        if self.id is None:
            return self._insert()
        else:
            return self._update()

    def _insert(self) -> bool:
        """вставляет новое событие и получает id через RETURNING"""
        query = """
            INSERT INTO events (book_id, event_date, description, max_participants)
            VALUES (%s, %s, %s, %s)
            RETURNING id, created_at;
        """
        try:
            result = self.db.execute_query(
                query,
                (self.book_id, self.event_date, self.description, self.max_participants),
                fetch=True,
            )
            if result:
                self.id = result[0]["id"]
                self.created_at = result[0]["created_at"]
                return True
            return False
        except Exception as e:
            print(f"Ошибка при вставке события: {e}")
            return False

    def _update(self) -> bool:
        """обновляет существующее событие"""
        query = """
            UPDATE events
            SET book_id = %s, event_date = %s, description = %s, max_participants = %s
            WHERE id = %s;
        """
        try:
            self.db.execute_query(
                query,
                (self.book_id, self.event_date, self.description, self.max_participants, self.id),
            )
            return True
        except Exception as e:
            print(f"Ошибка при обновлении события: {e}")
            return False

    def delete(self) -> bool:
        """удаляет событие из БД"""
        if self.id is None:
            return False
        query = "DELETE FROM events WHERE id = %s;"
        try:
            self.db.execute_query(query, (self.id,))
            self.id = None
            return True
        except Exception as e:
            print(f"Ошибка при удалении события: {e}")
            return False

    # ---- Классовые методы для поиска ----

    @classmethod
    def get_by_id(self, cls, event_id: int) -> Optional["EventModel"]:
        """возвращает объект события по id, включая информацию о книге (через JOIN)"""
        query = """
            SELECT
                e.id,
                e.book_id,
                e.event_date,
                e.description,
                e.max_participants,
                e.created_at,
                b.title AS book_title,
                b.author AS book_author,
                b.year AS book_year
            FROM events e
            JOIN books b ON e.book_id = b.id
            WHERE e.id = %s;
        """
        result = self.db.execute_query(query, (event_id,), fetch=True)
        if not result:
            return None
        row = result[0]
        return cls(
            event_id=row["id"],
            book_id=row["book_id"],
            event_date=row["event_date"],
            description=row["description"],
            max_participants=row["max_participants"],
            created_at=row["created_at"],
            book_title=row["book_title"],
            book_author=row["book_author"],
            book_year=row["book_year"],
        )

    def get_all(self) -> List["EventModel"]:
        """возвращает список всех событий с данными о книге"""
        query = """
            SELECT
                e.id,
                e.book_id,
                e.event_date,
                e.description,
                e.max_participants,
                e.created_at,
                b.title AS book_title,
                b.author AS book_author,
                b.year AS book_year
            FROM events e
            JOIN books b ON e.book_id = b.id
            ORDER BY e.event_date;
        """
        rows = self.db.execute_query(query, fetch=True)
        # events = []
        # for row in rows:
        #     events.append(
        #         cls(
        #             event_id=row["id"],
        #             book_id=row["book_id"],
        #             event_date=row["event_date"],
        #             description=row["description"],
        #             max_participants=row["max_participants"],
        #             created_at=row["created_at"],
        #             book_title=row["book_title"],
        #             book_author=row["book_author"],
        #             book_year=row["book_year"],
        #         )
        #     )
        return rows

    def get_by_date(self, date_str: str) -> Optional["EventModel"]:
        """возвращает первое событие на указанную дату с данными о книге"""
        query = """
            SELECT
                e.id,
                e.book_id,
                e.event_date,
                e.description,
                e.max_participants,
                e.created_at,
                b.title AS book_title,
                b.author AS book_author,
                b.year AS book_year
            FROM events e
            JOIN books b ON e.book_id = b.id
            WHERE e.event_date = %s
            LIMIT 1;
        """
        result = self.db.execute_query(query, (date_str,), fetch=True)
        if not result:
            return None
        row = result[0]
        # return cls(
        #     event_id=row["id"],
        #     book_id=row["book_id"],
        #     event_date=row["event_date"],
        #     description=row["description"],
        #     max_participants=row["max_participants"],
        #     created_at=row["created_at"],
        #     book_title=row["book_title"],
        #     book_author=row["book_author"],
        #     book_year=row["book_year"],
        # )
        return row

    def get_available_slots(self, event_id: int) -> int:
        """возвращает количество свободных мест на событие (0, если событие не найдено)"""
        query = """
            SELECT
                e.max_participants - COUNT(bk.id) AS available_slots
            FROM events e
            LEFT JOIN bookings bk ON e.id = bk.event_id
            WHERE e.id = %s
            GROUP BY e.id, e.max_participants;
        """
        result = self.db.execute_query(query, (event_id,), fetch=True)
        return result[0]["available_slots"] if result else 0
