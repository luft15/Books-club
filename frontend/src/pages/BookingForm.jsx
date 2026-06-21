import React from 'react';
import { Link } from 'react-router-dom';

const BookingForm = ({ user, events, formData, handleChange, handleSubmit, loading, showSuccess }) => {
  return (
    <div className="booking-sidebar">
      <div className="form-wrapper">
        <h2 className="form-title">Записаться на встречу</h2>
        {showSuccess ? (
          <div className="success-message">
            <div className="success-icon">[Успешно]</div>
            <p>Запись создана!</p>
            <p>Подтверждение придет на email</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="booking-form">
            {!user && (
              <div className="auth-warning">
                <Link to="/login" className="plan-auth-warning-link">Войдите</Link>, чтобы записаться
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
  );
};

export default BookingForm;
