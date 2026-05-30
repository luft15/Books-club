import psycopg2
import os
import time
from psycopg2.extras import RealDictCursor


class Database:
    def __init__(self):
        self.connection = None,
        self.connect()

    def connect(self):
        """Устанавливает соединение с БД, используя переменные окружения."""
        try:
            self.connection = psycopg2.connect(
                host=os.getenv('DB_HOST', 'postgres'),
                port=os.getenv('DB_PORT', '5432'),
                database=os.getenv('DB_NAME', 'postgres'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'postgres')
            )
            print("Успешное подключение к базе данных")
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")
            raise  # Прерываем запуск приложения, если БД недоступна  

    def execute_query(self, query, params=None, fetch=False):
        """Ы
        Универсальная функция для выполнения SQL-запросов.
        """
        if not self.connection or self.connection.closed:
            self.connect()

        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                if fetch:
                    result = cursor.fetchall()
                else:
                    result = None
            self.connection.commit()
            return result
        except Exception as e:
            self.connection.rollback()
            print(f'ошибка выполнения запроса {e}\nЗЗапрос: {query}\n Params:{params}')
            raise

    def close(self):
        '''закрывает соединение с БД'''
        if self.connection and not self.connection.closed:
            self.connection.close()
            print('сооедениение с БД закрыто')
            