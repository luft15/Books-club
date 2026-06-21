// frontend/src/components/admin/StatsCards.jsx
import React from 'react';

const StatsCards = ({ stats }) => {
  if (!stats) return null;
  const items = [
    { label: 'Пользователи', value: stats.total_users },
    { label: 'Книги', value: stats.total_books },
    { label: 'События', value: stats.total_events },
    { label: 'Бронирования', value: stats.total_bookings },
  ];
  return (
    <div className="admin-stats-grid">
      {items.map((item) => (
        <div key={item.label} className="admin-stat-card">
          <h3>{item.label}</h3>
          <p className="admin-stat-number">{item.value}</p>
        </div>
      ))}
    </div>
  );
};

export default StatsCards;
