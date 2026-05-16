import psycopg2
import os
import time
from psycopg2.extras import RealDictCursor


def connect_db(retries=5, delay=2):
    for attempt in range(retries):
        try:
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'postgres'),
                port=os.getenv('DB_PORT', '5432'),
                database=os.getenv('DB_NAME', 'postgres'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'postgres')
            )
            return conn
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            print(f"ошибка подсоединение к базе данных: {e}")
            return None   

def execute_query(query, params=None, fetch=False):
    """
    Универсальная функция для выполнения SQL-запросов.
    """
    connection = connect_db()

    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)

            result = cursor.fetchall() if fetch else None

        connection.commit()
        return result

    finally:
        connection.close()