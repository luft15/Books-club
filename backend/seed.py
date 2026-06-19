# backend/seed.py
from sqlalchemy.orm import Session
from app.models.user_model import User_model
from app.models.book_model import Book_model
from app.models.event_model import Event_model
from app.models.booking_model import Booking_model
from app.services.auth_service import get_password_hash
from datetime import date, time, timedelta


def seed_database(db: Session):
    """Заполнение базы тестовыми данными"""
    
    # Проверяем, есть ли уже данные
    if db.query(User_model).first():
        print("База уже содержит данные, пропускаем сидирование")
        return
    
    print("📚 Заполнение базы данных тестовыми данными...")
    
    # ========== СОЗДАНИЕ ПОЛЬЗОВАТЕЛЕЙ ==========
    print("👤 Создание пользователей...")
    
    admin = User_model(
        username="admin123",
        email="admin123@bookclub.com",
        hashed_password=get_password_hash("admin123"),
        full_name="Администратор Книжного Клуба",
        is_admin=True,
        is_active=True
    )
    db.add(admin)
    
    users_data = [
        ("anna", "Анна Петрова", "+79161234567"),
        ("ivan", "Иван Сидоров", "+79261234567"),
        ("maria", "Мария Иванова", "+79221234567"),
        ("pavel", "Павел Смирнов", "+79171234567"),
        ("olga", "Ольга Козлова", "+79181234567"),
    ]
    
    users = []
    for username, full_name, phone in users_data:
        user = User_model(
            username=username,
            email=f"{username}@example.com",
            hashed_password=get_password_hash("password123"),
            full_name=full_name,
            phone=phone,
            is_active=True,
            is_admin=False
        )
        users.append(user)
    
    db.add_all(users)
    db.commit()
    
    # ========== СОЗДАНИЕ КНИГ ==========
    print("📖 Создание книг...")
    
    books_data = [
        ("Джейн Эйр", "Шарлотта Бронте", 1847),
        ("Бесы", "Ф.М. Достоевский", 1872),
        ("Лигея", "Эдгар Аллан По", 1838),
        ("Война и мир", "Л.Н. Толстой", 1869),
        ("Преступление и наказание", "Ф.М. Достоевский", 1866),
        ("Мастер и Маргарита", "М.А. Булгаков", 1967),
        ("Гарри Поттер и философский камень", "Дж.К. Роулинг", 1997),
        ("1984", "Джордж Оруэлл", 1949),
    ]
    
    books = []
    for title, author, year in books_data:
        book = Book_model(title=title, author=author, year=year)
        books.append(book)
    
    db.add_all(books)
    db.commit()
    
    # ========== СОЗДАНИЕ СОБЫТИЙ ==========
    print("📅 Создание событий...")
    
    events_data = [
        (books[0].id, date.today() + timedelta(days=30), "Zoom-встреча, обсуждение «Джейн Эйр»", 30),
        (books[1].id, date.today() + timedelta(days=15), "Офлайн в клубе на ул. Книжная, 10", 20),
        (books[2].id, date.today() + timedelta(days=45), "Поэтический вечер по рассказу «Лигея»", 15),
        (books[3].id, date.today() + timedelta(days=60), "Обсуждение романа «Война и мир»", 25),
        (books[4].id, date.today() + timedelta(days=20), "Классический вечер: Достоевский", 30),
        (books[5].id, date.today() + timedelta(days=50), "Мистический вечер по роману Булгакова", 20),
    ]
    
    events = []
    for book_id, event_date, description, max_participants in events_data:
        event = Event_model(
            book_id=book_id,
            event_date=event_date,
            description=description,
            max_participants=max_participants
        )
        events.append(event)
    
    db.add_all(events)
    db.commit()
    

    print("📝 Создание бронирований...")
    
    bookings_data = [
        (events[0].id, users[0].id, time(18, 0), "Приду с подругой"),
        (events[0].id, users[1].id, time(19, 0), None),
        (events[1].id, users[2].id, time(18, 0), "Буду онлайн"),
        (events[2].id, users[0].id, time(17, 0), "Очень жду!"),
        (events[1].id, users[3].id, time(19, 0), "Возьму книгу с собой"),
        (events[3].id, users[4].id, time(18, 0), None),
        (events[4].id, users[0].id, time(18, 30), "Интересная тема"),
        (events[4].id, users[2].id, time(19, 0), "Приду"),
    ]
    
    bookings = []
    for event_id, user_id, time_slot, comment in bookings_data:
        booking = Booking_model(
            event_id=event_id,
            user_id=user_id,
            time_slot=time_slot,
            comment=comment
        )
        bookings.append(booking)
    
    db.add_all(bookings)
    db.commit()
    
    print("\n✅ База данных успешно заполнена тестовыми данными!")
    print("\n👤 Тестовые пользователи:")
    print("  👑 Админ:    admin / admin123")
    print("  👤 Анна:      anna / password123")
    print("  👤 Иван:      ivan / password123")
    print("  👤 Мария:     maria / password123")
    print("  👤 Павел:     pavel / password123")
    print("  👤 Ольга:     olga / password123")
    print("\n📊 Статистика:")
    print(f"  - Пользователей: {len(users) + 1}")
    print(f"  - Книг: {len(books)}")
    print(f"  - Событий: {len(events)}")
    print(f"  - Бронирований: {len(bookings)}")


if __name__ == "__main__":
    from app.core.database import SessionLocal
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()