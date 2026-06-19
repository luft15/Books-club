import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { eventsAPI, bookingsAPI } from '../api/endpoints';
import '../assets/css/style.css';

const PlanPage = () => {
  const { user } = useAuth();
  const [events, setEvents] = useState([]);
  const [eventsByDate, setEventsByDate] = useState({});
  const [formData, setFormData] = useState({
    event_id: '',
    time_slot: '',
    comment: ''
  });
  const [showSuccess, setShowSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  // Загрузка событий
  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await eventsAPI.getAll();
        setEvents(response.data);
        // Группируем по дате для календаря
        const map = {};
        response.data.forEach(event => {
          const date = event.event_date;
          if (!map[date]) map[date] = [];
          map[date].push(event.book?.title || 'Событие');
        });
        setEventsByDate(map);
      } catch (error) {
        console.error('Ошибка загрузки событий:', error);
      }
    };
    fetchEvents();
  }, []);

  // Функция построения календаря (возвращает массив JSX-элементов)
  const buildCalendar = (year, month) => {
    const firstDay = new Date(year, month, 1);
    const startWeekday = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1;
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const cells = [];

    // Пустые ячейки до первого дня
    for (let i = 0; i < startWeekday; i++) {
      cells.push(<div key={`empty-${i}`} className="day-cell empty"></div>);
    }

    // Дни месяца
    for (let day = 1; day <= daysInMonth; day++) {
      const dateKey = `${year}-${String(month+1).padStart(2,'0')}-${String(day).padStart(2,'0')}`;
      const dayEvents = eventsByDate[dateKey] || [];
      cells.push(
        <div key={day} className="day-cell">
          <div className="day-number">{day}</div>
          {dayEvents.map((ev, idx) => (
            <div key={idx} className="event-text">{ev}</div>
          ))}
        </div>
      );
    }
    return cells;
  };

  // Обработка формы
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await bookingsAPI.create({
        event_id: parseInt(formData.event_id),
        time_slot: formData.time_slot,
        comment: formData.comment
      });
      setShowSuccess(true);
      setFormData({ event_id: '', time_slot: '', comment: '' });
      setTimeout(() => setShowSuccess(false), 5000);
    } catch (error) {
      alert('Ошибка записи: ' + (error.response?.data?.detail || 'Попробуйте позже'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="schedule-page">
      {/* <header className="header">
        <div className="nav">
          <div className="container-wide">
            <div className="row space-beetween">
              <div className="logo">BOOKSclub</div>
              <div className="nav-menu">
                <ul>
                  <li><Link to="/">Главная</Link></li>
                  <li><Link to="/information">Информация</Link></li>
                  <li><Link to="/plan">Расписание</Link></li>
                </ul>
              </div>
              {user ? (
                <Link to="/profile" className="login">{user.username}</Link>
              ) : (
                <Link to="/login" className="login">Войти</Link>
              )}
            </div>
          </div>
        </div>
      </header> */}

      <main>
        <div className="article-img">
          {/* Календарь */}
          <div className="calendar-wrapper">
            <div className="calendar-double">
              <div className="header-note">
                📖 <span>Календарь литературных пометок</span> — Февраль / Март 2026
              </div>
              <div className="two-months">
                <div className="month-card">
                  <div className="month-title">Февраль 2026</div>
                  <div className="weekdays">
                    {['Пн','Вт','Ср','Чт','Пт','Сб','Вс'].map(d => (
                      <div key={d} className="weekday">{d}</div>
                    ))}
                  </div>
                  <div className="days-grid">
                    {buildCalendar(2026, 1)}
                  </div>
                </div>
                <div className="month-card">
                  <div className="month-title">Март 2026</div>
                  <div className="weekdays">
                    {['Пн','Вт','Ср','Чт','Пт','Сб','Вс'].map(d => (
                      <div key={d} className="weekday">{d}</div>
                    ))}
                  </div>
                  <div className="days-grid">
                    {buildCalendar(2026, 2)}
                  </div>
                </div>
              </div>
              <div className="footer-legend">
                <div className="legend-item"><strong>Отмеченные события</strong></div>
                <div className="legend-item">
                  <span className="legend-badge"></span> «БЕСЫ» Достоевский Ф.М.
                </div>
                <div className="legend-item">
                  <span className="legend-badge bronte-style"></span> «ДЖЕЙН ЭЙР» Бронте Ш.
                </div>
                <div className="legend-item">
                  <span className="legend-badge" style={{background:'#faeecb'}}></span> «ЛИГЕЯ» по Э.А.ПО
                </div>
                <div className="legend-item">Поэтические / прозаические пометки</div>
              </div>
            </div>
          </div>

          {/* Форма записи */}
          <div className="booking-sidebar">
            <div className="form-wrapper">
              <h2 className="form-title">Записаться на встречу</h2>
              {showSuccess ? (
                <div className="success-message">
                  <div className="success-icon">✅</div>
                  <p>Запись создана!</p>
                  <p>Подтверждение придет на email</p>
                </div>
              ) : (
                <form onSubmit={handleSubmit} className="booking-form">
                  {!user && (
                    <div className="auth-warning">
                      ⚠️ <Link to="/login" style={{ color: '#856404', fontWeight: 'bold' }}>Войдите</Link>, чтобы записаться
                    </div>
                  )}
                  <div className="form-group">
                    <select
                      name="event_id"
                      value={formData.event_id}
                      onChange={handleChange}
                      required
                      disabled={!user}
                    >
                      <option value="">Выберите событие</option>
                      {events.map(event => (
                        <option key={event.id} value={event.id}>
                          {event.book?.title} - {new Date(event.event_date).toLocaleDateString()}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="form-group">
                    <select
                      name="time_slot"
                      value={formData.time_slot}
                      onChange={handleChange}
                      required
                      disabled={!user}
                    >
                      <option value="">Выберите время</option>
                      <option value="18:00">18:00</option>
                      <option value="19:00">19:00</option>
                      <option value="20:00">20:00</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <textarea
                      name="comment"
                      placeholder="Комментарий (необязательно)"
                      maxLength="200"
                      value={formData.comment}
                      onChange={handleChange}
                      disabled={!user}
                      rows="3"
                    />
                  </div>
                  <button type="submit" className="submit-btn" disabled={loading || !user}>
                    {loading ? 'Отправка...' : 'Записаться на встречу'}
                  </button>
                </form>
              )}
            </div>
          </div>
        </div>
      </main>

      {/* <footer className="footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-col">
              <div className="footer-logo">BOOKSclub</div>
              <p className="footer-description">Книжный клуб для тех, кто любит читать и обсуждать.</p>
            </div>
            <div className="footer-col">
              <h3 className="footer-title">Навигация</h3>
              <ul className="footer-links">
                <li><Link to="/">Главная</Link></li>
                <li><Link to="/information">Информация</Link></li>
                <li><Link to="/plan">Расписание</Link></li>
                <li><Link to="/profile">Личный кабинет</Link></li>
              </ul>
            </div>
            <div className="footer-col">
              <h3 className="footer-title">Контакты</h3>
              <ul className="footer-contacts">
                <li>club@booksclub.ru</li>
                <li>+7 (999) 123-45-67</li>
                <li>ул. Книжная, д. 10</li>
              </ul>
            </div>
            <div className="footer-col">
              <h3 className="footer-title">Мы в соцсетях</h3>
              <div className="social-links">
                <a href="#" className="social-link">Telegram</a>
                <a href="#" className="social-link">VK</a>
                <a href="#" className="social-link">YouTube</a>
              </div>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2025 BOOKSclub. Все права защищены.</p>
          </div>
        </div>
      </footer> */}
    </div>
  );
};

export default PlanPage;
