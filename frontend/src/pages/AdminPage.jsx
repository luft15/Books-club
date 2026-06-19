import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { adminAPI, eventsAPI, booksAPI } from '../api/endpoints';
import '../assets/css/style.css';

const AdminPage = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [events, setEvents] = useState([]);
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newEvent, setNewEvent] = useState({ book_id: '', event_date: '', description: '', max_participants: 20 });
  const [newBook, setNewBook] = useState({ title: '', author: '', year: '' });
  const [message, setMessage] = useState('');

  const fetchAllData = async () => {
    try {
      const [statsRes, eventsRes, booksRes] = await Promise.all([
        adminAPI.getStats(),
        eventsAPI.getAll(),
        booksAPI.getAll(),
      ]);
      setStats(statsRes.data);
      setEvents(eventsRes.data);
      setBooks(booksRes.data);
    } catch (err) {
      setError('Ошибка загрузки данных');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user?.is_admin) fetchAllData();
  }, [user]);

  const handleCreateEvent = async (e) => {
    e.preventDefault();
    setMessage('');
    try {
      const payload = {
        ...newEvent,
        book_id: parseInt(newEvent.book_id), // преобразуем в число
        max_participants: parseInt(newEvent.max_participants),
      };
      await eventsAPI.create(payload);
      setMessage('✅ Событие создано!');
      setNewEvent({ book_id: '', event_date: '', description: '', max_participants: 20 });
      await fetchAllData(); // обновляем все данные
    } catch (err) {
      setMessage('❌ Ошибка: ' + (err.response?.data?.detail || 'попробуйте позже'));
    }
  };

  const handleDeleteEvent = async (id) => {
    if (!window.confirm('Удалить событие?')) return;
    try {
      await eventsAPI.delete(id);
      setMessage('🗑️ Событие удалено');
      await fetchAllData();
    } catch (err) {
      setMessage('❌ Ошибка удаления');
    }
  };

  const handleCreateBook = async (e) => {
    e.preventDefault();
    setMessage('');
    try {
      await booksAPI.create(newBook);
      setMessage('✅ Книга добавлена!');
      setNewBook({ title: '', author: '', year: '' });
      await fetchAllData();
    } catch (err) {
      setMessage('❌ Ошибка добавления книги');
    }
  };

  if (loading) return <div className="container" style={{ padding: '40px 20px' }}>Загрузка...</div>;
  if (error) return <div className="container" style={{ padding: '40px 20px', color: 'red' }}>{error}</div>;
  if (!user?.is_admin) return <div className="container" style={{ padding: '40px 20px' }}>Доступ запрещён</div>;

  return (
    <div className="container" style={{ padding: '40px 20px' }}>
      <h1>Админ-панель</h1>
      {message && <div style={{ padding: '10px', marginBottom: '20px', background: '#e8f5e9', borderRadius: '4px' }}>{message}</div>}

      {/* Статистика */}
      {stats && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(150px,1fr))', gap: '20px', marginBottom: '40px' }}>
          <div style={{ background: '#63a7eb', padding: '20px', borderRadius: '8px', textAlign: 'center' }}>
            <h3>Пользователи</h3>
            <p style={{ fontSize: '24px' }}>{stats.total_users}</p>
          </div>
          <div style={{ background: '#63a7eb', padding: '20px', borderRadius: '8px', textAlign: 'center' }}>
            <h3>Книги</h3>
            <p style={{ fontSize: '24px' }}>{stats.total_books}</p>
          </div>
          <div style={{ background: '#63a7eb', padding: '20px', borderRadius: '8px', textAlign: 'center' }}>
            <h3>События</h3>
            <p style={{ fontSize: '24px' }}>{stats.total_events}</p>
          </div>
          <div style={{ background: '#63a7eb', padding: '20px', borderRadius: '8px', textAlign: 'center' }}>
            <h3>Бронирования</h3>
            <p style={{ fontSize: '24px' }}>{stats.total_bookings}</p>
          </div>
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '40px' }}>
        {/* Создание события */}
        <div style={{ background: 'white', padding: '20px', borderRadius: '12px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
          <h2>Создать событие</h2>
          <form onSubmit={handleCreateEvent}>
            <div style={{ marginBottom: '10px' }}>
              <label>Книга</label>
              <select
                value={newEvent.book_id}
                onChange={(e) => setNewEvent({ ...newEvent, book_id: e.target.value })}
                required
                style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
              >
                <option value="">Выберите книгу</option>
                {books.map(b => <option key={b.id} value={b.id}>{b.title}</option>)}
              </select>
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label>Дата</label>
              <input type="date" value={newEvent.event_date} onChange={(e) => setNewEvent({ ...newEvent, event_date: e.target.value })} required style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }} />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label>Описание</label>
              <textarea value={newEvent.description} onChange={(e) => setNewEvent({ ...newEvent, description: e.target.value })} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }} rows="2" />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label>Макс. участников</label>
              <input type="number" value={newEvent.max_participants} onChange={(e) => setNewEvent({ ...newEvent, max_participants: parseInt(e.target.value) })} min="1" style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }} />
            </div>
            <button type="submit" style={{ padding: '10px 20px', background: '#3498db', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Создать событие</button>
          </form>
        </div>

        {/* Добавление книги */}
        <div style={{ background: 'white', padding: '20px', borderRadius: '12px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
          <h2>Добавить книгу</h2>
          <form onSubmit={handleCreateBook}>
            <div style={{ marginBottom: '10px' }}>
              <label>Название</label>
              <input type="text" value={newBook.title} onChange={(e) => setNewBook({ ...newBook, title: e.target.value })} required style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }} />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label>Автор</label>
              <input type="text" value={newBook.author} onChange={(e) => setNewBook({ ...newBook, author: e.target.value })} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }} />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label>Год</label>
              <input type="number" value={newBook.year} onChange={(e) => setNewBook({ ...newBook, year: parseInt(e.target.value) })} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }} />
            </div>
            <button type="submit" style={{ padding: '10px 20px', background: '#2ecc71', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Добавить книгу</button>
          </form>
        </div>
      </div>

      {/* Список событий */}
      <div style={{ marginTop: '40px' }}>
        <h2>Управление событиями</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {events.map(event => (
            <div key={event.id} style={{ background: 'white', padding: '15px', borderRadius: '8px', boxShadow: '0 1px 5px rgba(0,0,0,0.1)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <strong>{event.book?.title}</strong> - {new Date(event.event_date).toLocaleDateString()}
                <br /><span style={{ fontSize: '0.9rem', color: '#555' }}>{event.description}</span>
              </div>
              <button onClick={() => handleDeleteEvent(event.id)} style={{ padding: '6px 12px', background: '#e74c3c', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Удалить</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AdminPage;