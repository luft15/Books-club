-- 1. Создание таблиц
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT,
    year INTEGER
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    event_date DATE NOT NULL,
    description TEXT,
    max_participants INTEGER DEFAULT 20,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    user_name TEXT NOT NULL,
    user_phone TEXT,
    user_email TEXT NOT NULL,
    time_slot TIME,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Добавляем тестовые книги
INSERT INTO books (title, author, year) VALUES
('Джейн Эйр', 'Шарлотта Бронте', 1847),
('Бесы', 'Ф.М. Достоевский', 1872),
('Лигея', 'Эдгар Аллан По', 1838);

-- 3. Добавляем тестовые события
INSERT INTO events (book_id, event_date, description, max_participants) VALUES
(1, '2026-03-20', 'Zoom-встреча, обсуждение «Джейн Эйр»', 30),
(2, '2026-02-15', 'Офлайн в клубе на ул. Книжная, 10', 20),
(3, '2026-03-06', 'Поэтический вечер по рассказу «Лигея»', 15);

-- 4. Добавляем тестовые записи пользователей
INSERT INTO bookings (event_id, user_name, user_phone, user_email, time_slot, comment) VALUES
(1, 'Анна Петрова', '+79161234567', 'anna@example.com', '18:00', 'Приду с подругой'),
(1, 'Иван Сидоров', '', 'ivan@example.com', '19:00', NULL),
(2, 'Мария Иванова', '+79221234567', 'maria@example.com', '18:00', 'Буду онлайн');

-- SELECT e.event_date, b.title, b.author, e.description FROM events e JOIN books b ON e.book_id = b.id ORDER BY e.event_date;
-- Посмотреть записи на конкретное событие (id=1):
-- SELECT * FROM bookings WHERE event_id = 1;