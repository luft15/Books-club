import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { bookingsAPI } from '../api/endpoints';
import '../assets/css/style.css';

const ProfilePage = () => {
  const { user } = useAuth();
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchBookings = async () => {
      try {
        const response = await bookingsAPI.getMy();
        setBookings(response.data);
      } catch (err) {
        setError('Не удалось загрузить записи');
      } finally {
        setLoading(false);
      }
    };
    if (user) fetchBookings();
  }, [user]);

  const handleCancel = async (bookingId) => {
    if (!window.confirm('Вы уверены, что хотите отменить запись?')) return;
    try {
      await bookingsAPI.cancel(bookingId);
      setBookings(bookings.filter(b => b.id !== bookingId));
    } catch (err) {
      alert('Ошибка отмены: ' + (err.response?.data?.detail || 'Попробуйте позже'));
    }
  };

  if (loading) return <div className="container" style={{ padding: '40px 20px' }}>Загрузка...</div>;
  if (error) return <div className="container" style={{ padding: '40px 20px', color: 'red' }}>{error}</div>;

  return (
    <div className="container" style={{ padding: '40px 20px', minHeight: '70vh' }}>
      <h1>Мои записи</h1>
      {bookings.length === 0 ? (
        <p>У вас пока нет записей на события.</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {bookings.map((booking) => (
            <div key={booking.id} style={{
              background: 'rgba(95, 95, 95, 0.9)',
              padding: '20px',
              borderRadius: '12px',
              boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              flexWrap: 'wrap',
            }}>
              <div>
                <h3 style={{ margin: '0 0 5px 0' }}>{booking.event?.book?.title || 'Событие'}</h3>
                <p style={{ margin: '5px 0' }}>📅 {new Date(booking.event?.event_date).toLocaleDateString()}</p>
                <p style={{ margin: '5px 0' }}>🕒 {booking.time_slot || 'время не указано'}</p>
                {booking.comment && <p style={{ margin: '5px 0', fontStyle: 'italic' }}>Комментарий: {booking.comment}</p>}
              </div>
              <button
                onClick={() => handleCancel(booking.id)}
                style={{
                  padding: '8px 16px',
                  background: '#e74c3c',
                  color: 'white',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                }}
              >
                Отменить
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ProfilePage;
