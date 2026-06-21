import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { adminAPI, eventsAPI, booksAPI } from '../api/endpoints';
import StatsCards from '../components/admin/StatsCards';
import EventForm from '../components/admin/EventForm';
import BookForm from '../components/admin/BookForm';
import EventList from '../components/admin/EventList';
import '../assets/css/style.css';

const AdminPage = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [events, setEvents] = useState([]);
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
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

  const handleCreateEvent = async (payload) => {
    setMessage('');
    try {
      await eventsAPI.create(payload);
      setMessage('Событие создано!');
      await fetchAllData();
    } catch (err) {
      setMessage('Ошибка: ' + (err.response?.data?.detail || 'попробуйте позже'));
    }
  };

  const handleDeleteEvent = async (id) => {
    if (!window.confirm('Удалить событие?')) return;
    try {
      await eventsAPI.delete(id);
      setMessage('Событие удалено');
      await fetchAllData();
    } catch (err) {
      setMessage('Ошибка удаления');
    }
  };

  const handleCreateBook = async (payload) => {
    setMessage('');
    try {
      await booksAPI.create(payload);
      setMessage('Книга добавлена!');
      await fetchAllData();
    } catch (err) {
      setMessage('Ошибка добавления книги');
    }
  };

  if (loading) return <div className="loading-text">Загрузка...</div>;
  if (error) return <div className="error-text">{error}</div>;
  if (!user?.is_admin) return <div className="forbidden-text">Доступ запрещён</div>;

  return (
    <div className="admin-container">
      <h1>Админ-панель</h1>
      {message && <div className="admin-message">{message}</div>}

      <StatsCards stats={stats} />

      <div className="admin-forms-grid">
        <EventForm books={books} onSubmit={handleCreateEvent} />
        <BookForm onSubmit={handleCreateBook} />
      </div>

      <EventList events={events} onDelete={handleDeleteEvent} />
    </div>
  );
};

export default AdminPage;
