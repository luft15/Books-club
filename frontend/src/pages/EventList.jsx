// frontend/src/components/admin/EventList.jsx
import React from 'react';

const EventList = ({ events, onDelete }) => {
  return (
    <div className="admin-events-list">
      <h2>Управление событиями</h2>
      <div>
        {events.map((event) => (
          <div key={event.id} className="admin-event-item">
            <div>
              <div className="admin-event-title">
                {event.book?.title} - {new Date(event.event_date).toLocaleDateString()}
              </div>
              <div className="admin-event-desc">{event.description}</div>
            </div>
            <button
              onClick={() => onDelete(event.id)}
              className="admin-btn-danger"
            >
              Удалить
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EventList;
