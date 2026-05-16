# src/models/booking_model.py
from db.db import execute_query


class BookingModel:
    @staticmethod
    def get_all():
        query = """
            SELECT id, event_id, user_name, user_phone, user_email,
                   time_slot, comment, created_at
            FROM bookings
            ORDER BY created_at DESC;
        """
        return execute_query(query, fetch=True)

    @staticmethod
    def get_by_id(booking_id):
        query = """
            SELECT id, event_id, user_name, user_phone, user_email,
                   time_slot, comment, created_at
            FROM bookings
            WHERE id = %s;
        """
        result = execute_query(query, (booking_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def get_by_event_id(event_id):
        query = """
            SELECT id, user_name, user_phone, user_email, time_slot,
                   comment, created_at
            FROM bookings
            WHERE event_id = %s
            ORDER BY created_at;
        """
        return execute_query(query, (event_id,), fetch=True)

    @staticmethod
    def create(event_id, user_name, user_email, user_phone=None, time_slot=None, comment=None):
        query = """
            INSERT INTO bookings (
                event_id, user_name, user_phone, user_email, time_slot, comment
            ) VALUES (%s, %s, %s, %s, %s, %s);
        """
        execute_query(query, (event_id, user_name, user_phone, user_email, time_slot, comment))

    @staticmethod
    def update(booking_id, user_name=None, user_phone=None, user_email=None,
               time_slot=None, comment=None):
        fields = []
        params = []
        if user_name is not None:
            fields.append("user_name = %s")
            params.append(user_name)
        if user_phone is not None:
            fields.append("user_phone = %s")
            params.append(user_phone)
        if user_email is not None:
            fields.append("user_email = %s")
            params.append(user_email)
        if time_slot is not None:
            fields.append("time_slot = %s")
            params.append(time_slot)
        if comment is not None:
            fields.append("comment = %s")
            params.append(comment)

        if not fields:
            return  # нечего обновлять

        query = f"""
            UPDATE bookings
            SET {', '.join(fields)}
            WHERE id = %s;
        """
        params.append(booking_id)
        execute_query(query, tuple(params))

    @staticmethod
    def delete(booking_id):
        query = "DELETE FROM bookings WHERE id = %s;"
        execute_query(query, (booking_id,))

    @staticmethod
    def count_by_event(event_id):
        query = """
            SELECT COUNT(*) AS cnt
            FROM bookings
            WHERE event_id = %s;
        """
        result = execute_query(query, (event_id,), fetch=True)
        return result[0]['cnt'] if result else 0