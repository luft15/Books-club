// frontend/src/pages/HomePage.jsx
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Navigation from '../components/common/Navigation';
import Footer from '../components/common/Footer';
import '../assets/css/style.css';
import { useAuth } from '../context/AuthContext';
import { eventsAPI } from '../api/endpoints';

const HomePage = () => {
  const { user } = useAuth();
  const [upcomingEvents, setUpcomingEvents] = useState([]);
  const [isDarkTheme, setIsDarkTheme] = useState(false);

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      setIsDarkTheme(true);
      document.body.classList.add('dark-theme');
    }
  }, []);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await eventsAPI.getAll({ upcoming: true, limit: 3 });
        setUpcomingEvents(response.data);
      } catch (error) {
        console.error('Error fetching events:', error);
      }
    };
    fetchEvents();
  }, []);

  const toggleTheme = () => {
    const newTheme = !isDarkTheme;
    setIsDarkTheme(newTheme);
    document.body.classList.toggle('dark-theme');
    localStorage.setItem('theme', newTheme ? 'dark' : 'light');
  };

  return (
  <div className="fon1">
    <button className="theme-toggle" onClick={toggleTheme}>
      {isDarkTheme ? '☀️ Светлая тема' : '🌙 Тёмная тема'}
    </button>
    
    <div className="hero-title">
      <h1 className="high-text">Книжный клуб</h1>
      <h2 className="smal-text">погрузись в мир книг с нами</h2>
    </div>

    <div className="events-section">
      <div className="container">
        <h2 style={{ color: 'white' }}>Ближайшие события</h2>
        <div className="events-grid">
          {upcomingEvents.map(event => (
            <div key={event.id} className="event-card">
              <h3>{event.book?.title}</h3>
              <p>{new Date(event.event_date).toLocaleDateString()}</p>
              <p>{event.description}</p>
              <Link to={`/events/${event.id}`}>Подробнее</Link>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
);
};

export default HomePage;
