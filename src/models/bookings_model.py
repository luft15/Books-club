import re
from typing import Optional, List, Dict, Any
import phonenumbers
from phonenumbers import NumberParseException
from db.db import Database



class BookingModel:
    """модель бронирования"""

    def __init__(
        self,
        event_id: int,
        user_name: str,
        user_email: str,
        db: Database,  # DI
        user_phone: Optional[str] = None,
        time_slot: Optional[str] = None,
        comment: Optional[str] = None,
        booking_id: Optional[int] = None,
        created_at: Optional[str] = None
    ):
        self.id = booking_id
        self.event_id = event_id
        self.user_name = user_name.strip() if user_name else ""
        self.user_phone = user_phone.strip() if user_phone else None
        self.user_email = user_email.strip() if user_email else ""
        self.time_slot = time_slot.strip() if time_slot else None
        self.comment = comment.strip() if comment else None
        self.created_at = created_at, 
        self.db = db

        # Валидация данных при создании объекта
        self.validate()

    def validate(self) -> None:
        """проверяет корректность всех полей"""
        errors = []

        if not self.user_name:
            errors.append("Имя не может быть пустым")
        elif len(self.user_name) > 100:  # предположительный лимит в БД
            errors.append("Имя не должно превышать 100 символов")

        if not self.user_email:
            errors.append("Email не может быть пустым")
        # Только при помщи регулярок можно проверить валиндость email
        elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', self.user_email):
            errors.append("Неверный формат email")

        # валидация российского(!) номера через phonenumbers
        if self.user_phone:
            try:
                parsed = phonenumbers.parse(self.user_phone, "RU")
                if not phonenumbers.is_valid_number(parsed):
                    errors.append("Неверный формат телефона")
            except NumberParseException:
                errors.append("Неверный формат телефона")

        if not isinstance(self.event_id, int) or self.event_id <= 0:
            errors.append("ID события должен быть положительным числом")

        if errors:
            raise ValueError(f"Ошибки валидации: {', '.join(errors)}")

    def save(self) -> bool:
        """
        Сохраняет объект в БД (вставка или обновление).
        Возвращает True при успехе.
        """
        if self.id is None:
            return self._insert()
        else:
            return self._update()

    def _insert(self) -> bool:
        """Вставляет новую запись в БД"""
        query = """
            INSERT INTO bookings (
                event_id, user_name, user_phone, user_email, time_slot, comment
            ) VALUES (%s, %s, %s, %s, %s, %s);
        """
        try:
            self.db.execute_query(
                query,
                (
                    self.event_id,
                    self.user_name,
                    self.user_phone,
                    self.user_email,
                    self.time_slot,
                    self.comment,
                ),
            )
            # После вставки нужно получить назначенный ID
            # Предполагаем, что execute_query возвращает последний вставленный ID
            # Если нет, адаптируйте под свою реализацию
            self.id = self._get_last_insert_id()
            return True
        except Exception as e:
            print(f"Ошибка при вставке бронирования: {e}")
            return False

    def _update(self) -> bool:
        """Обновляет существующую запись"""
        query = """
            UPDATE bookings
            SET event_id = %s,
                user_name = %s,
                user_phone = %s,
                user_email = %s,
                time_slot = %s,
                comment = %s
            WHERE id = %s;
        """
        try:
            self.db.execute_query(
                query,
                (
                    self.event_id,
                    self.user_name,
                    self.user_phone,
                    self.user_email,
                    self.time_slot,
                    self.comment,
                    self.id,
                ),
            )
            return True
        except Exception as e:
            print(f"Ошибка при обновлении бронирования: {e}")
            return False

    def delete(self) -> bool:
        """Удаляет запись из БД"""
        if self.id is None:
            return False
        query = "DELETE FROM bookings WHERE id = %s;"
        try:
            self.db.execute_query(query, (self.id,))
            self.id = None
            return True
        except Exception as e:
            print(f"Ошибка при удалении бронирования: {e}")
            return False

    # ---- Статические/классовые методы для поиска ----

    @classmethod
    def get_by_id(self, cls, booking_id: int) -> Optional["BookingModel"]:
        """Возвращает объект Booking по ID или None"""
        query = """
            SELECT id, event_id, user_name, user_phone, user_email,
                   time_slot, comment, created_at
            FROM bookings
            WHERE id = %s;
        """
        result = self.db.execute_query(query, (booking_id,), fetch=True)
        if not result:
            return None
        row = result[0]
        return cls(
            booking_id=row["id"],
            event_id=row["event_id"],
            user_name=row["user_name"],
            user_phone=row["user_phone"],
            user_email=row["user_email"],
            time_slot=row["time_slot"],
            comment=row["comment"],
            created_at=row["created_at"],
        )

    @classmethod
    def get_all(self, cls) -> List["BookingModel"]:
        """Возвращает список всех бронирований"""
        query = """
            SELECT id, event_id, user_name, user_phone, user_email,
                   time_slot, comment, created_at
            FROM bookings
            ORDER BY created_at DESC;
        """
        rows = self.db.execute_query(query, fetch=True)
        return [
            cls(
                booking_id=row["id"],
                event_id=row["event_id"],
                user_name=row["user_name"],
                user_phone=row["user_phone"],
                user_email=row["user_email"],
                time_slot=row["time_slot"],
                comment=row["comment"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    @classmethod
    def get_by_event_id(self, cls, event_id: int) -> List["BookingModel"]:
        """Возвращает список бронирований для конкретного события"""
        query = """
            SELECT id, user_name, user_phone, user_email, time_slot,
                   comment, created_at
            FROM bookings
            WHERE event_id = %s
            ORDER BY created_at;
        """
        rows = self.db.execute_query(query, (event_id,), fetch=True)
        return [
            cls(
                booking_id=row["id"],
                event_id=event_id,
                user_name=row["user_name"],
                user_phone=row["user_phone"],
                user_email=row["user_email"],
                time_slot=row["time_slot"],
                comment=row["comment"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    @classmethod
    def count_by_event(self, cls, event_id: int) -> int:
        """Возвращает количество бронирований для события"""
        query = """
            SELECT COUNT(*) AS cnt
            FROM bookings
            WHERE event_id = %s;
        """
        result = self.db.execute_query(query, (event_id,), fetch=True)
        return result[0]["cnt"] if result else 0

    # вспомогательный метод для получения последнего ID (зависит от execute_query)
    @staticmethod
    def _get_last_insert_id(self) -> int:
        """получить последний вставленный ID"""
        # Если execute_query возвращает курсор с lastrowid
        # Здесь заглушка – адаптируйте под свой db модуль.
        result = self.db.execute_query("INSERT INTO bookings (...) VALUES (...) RETURNING id;", fetch=True)
        return result[0]["id"] if result else 0