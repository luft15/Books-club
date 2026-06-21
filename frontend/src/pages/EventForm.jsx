// frontend/src/components/admin/EventForm.jsx
import React, { useState } from 'react';

const EventForm = ({ books, onSubmit }) => {
  const [newEvent, setNewEvent] = useState({
    book_id: '',
    event_date: '',
    description: '',
    max_participants: 20,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewEvent((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      ...newEvent,
      book_id: parseInt(newEvent.book_id),
      max_participants: parseInt(newEvent.max_participants),
    });
    setNewEvent({ book_id: '', event_date: '', description: '', max_participants: 20 });
  };

  return (
    <div className="admin-form-container">
      <h2>Создать событие</h2>
      <form onSubmit={handleSubmit}>
        <div className="admin-form-group">
          <label>Книга</label>
          <select
            name="book_id"
            value={newEvent.book_id}
            onChange={handleChange}
            required
            className="admin-form-control"
          >
            <option value="">Выберите книгу</option>
            {books.map((b) => (
              <option key={b.id} value={b.id}>
                {b.title}
              </option>
            ))}
          </select>
        </div>
        <div className="admin-form-group">
          <label>Дата</label>
          <input
            type="date"
            name="event_date"
            value={newEvent.event_date}
            onChange={handleChange}
            required
            className="admin-form-control"
          />
        </div>
        <div className="admin-form-group">
          <label>Описание</label>
          <textarea
            name="description"
            value={newEvent.description}
            onChange={handleChange}
            className="admin-form-control"
            rows="2"
          />
        </div>
        <div className="admin-form-group">
          <label>Макс. участников</label>
          <input
            type="number"
            name="max_participants"
            value={newEvent.max_participants}
            onChange={handleChange}
            min="1"
            className="admin-form-control"
          />
        </div>
        <button type="submit" className="admin-btn-primary">
          Создать событие
        </button>
      </form>
    </div>
  );
};

export default EventForm;
