import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { eventsAPI, bookingsAPI } from '../api/endpoints';
import Calendar from '../components/plan/Calendar';
import BookingForm from '../components/plan/BookingForm';
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

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await eventsAPI.getAll();
        setEvents(response.data);
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
      <main>
        <div className="article-img">
          <Calendar eventsByDate={eventsByDate} />
          <BookingForm
            user={user}
            events={events}
            formData={formData}
            handleChange={handleChange}
            handleSubmit={handleSubmit}
            loading={loading}
            showSuccess={showSuccess}
          />
        </div>
      </main>
    </div>
  );
};

export default PlanPage;
