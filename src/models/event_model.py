from db.db import execute_query


class EventModel:
    @staticmethod
    def get_all():
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
        return execute_query(query, fetch=True)

    @staticmethod
    def get_by_id(event_id):
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
        result = execute_query(query, (event_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create(book_id, event_date, description, max_participants=20):
        query = """
            INSERT INTO events (
                book_id,
                event_date,
                description,
                max_participants
            )
            VALUES (%s, %s, %s, %s);
        """
        execute_query(
            query,
            (book_id, event_date, description, max_participants)
        )

    @staticmethod
    def update(event_id, book_id, event_date, description, max_participants):
        query = """
            UPDATE events
            SET
                book_id = %s,
                event_date = %s,
                description = %s,
                max_participants = %s
            WHERE id = %s;
        """
        execute_query(
            query,
            (
                book_id,
                event_date,
                description,
                max_participants,
                event_id
            )
        )

    @staticmethod
    def delete(event_id):
        query = "DELETE FROM events WHERE id = %s;"
        execute_query(query, (event_id,))

    @staticmethod
    def get_available_slots(event_id):
        query = """
            SELECT
                e.max_participants
                - COUNT(bk.id) AS available_slots
            FROM events e
            LEFT JOIN bookings bk ON e.id = bk.event_id
            WHERE e.id = %s
            GROUP BY e.id, e.max_participants;
        """
        result = execute_query(query, (event_id,), fetch=True)
        return result[0]["available_slots"] if result else 0
    
    @staticmethod
    def get_by_date(date_str):
        query = """
            SELECT e.id, e.book_id, e.event_date, e.description, e.max_participants,
                b.title AS book_title, b.author AS book_author
            FROM events e
            JOIN books b ON e.book_id = b.id
            WHERE e.event_date = %s
            LIMIT 1;
        """
        result = execute_query(query, (date_str,), fetch=True)
        return result[0] if result else None

# from db.db import connect_db
# event_model = EventModel(connect_db)  # у меня статистический подхд, так что это лишнее