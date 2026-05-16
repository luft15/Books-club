from db.db import execute_query


class BookModel:
    @staticmethod
    def get_all():
        query = """
            SELECT id, title, author, year
            FROM books
            ORDER BY title;
        """
        return execute_query(query, fetch=True)

    @staticmethod
    def get_by_id(book_id):
        query = """
            SELECT id, title, author, year
            FROM books
            WHERE id = %s;
        """
        result = execute_query(query, (book_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def get_by_author(author_name):
        query = """
            SELECT id, title, author, year
            FROM books
            WHERE author ILIKE %s
            ORDER BY year;
        """ # ILIKE для регистронезависимого поиска
        result = execute_query(query, (f'%{author_name}%',), fetch=True)
        return result if result else []

    @staticmethod
    def create(title, author=None, year=None):
        query = """
            INSERT INTO books (title, author, year)
            VALUES (%s, %s, %s);
        """
        execute_query(query, (title, author, year))

    @staticmethod
    def update(book_id, title, author=None, year=None):
        query = """
            UPDATE books
            SET title = %s,
                author = %s,
                year = %s
            WHERE id = %s;
        """
        execute_query(query, (title, author, year, book_id))

    @staticmethod
    def delete(book_id):
        query = "DELETE FROM books WHERE id = %s;"
        execute_query(query, (book_id,))

    @staticmethod
    def exists(book_id):
        query = "SELECT 1 FROM books WHERE id = %s LIMIT 1;"
        result = execute_query(query, (book_id,), fetch=True)
        return bool(result)