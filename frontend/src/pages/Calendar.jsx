import React from 'react';

const Calendar = ({ eventsByDate }) => {
  const buildCalendar = (year, month) => {
    const firstDay = new Date(year, month, 1);
    const startWeekday = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1;
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const cells = [];

    for (let i = 0; i < startWeekday; i++) {
      cells.push(<div key={`empty-${i}`} className="day-cell empty"></div>);
    }

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

  return (
    <div className="calendar-wrapper">
      <div className="calendar-double">
        <div className="header-note">
          <span>Календарь литературных пометок</span> — Февраль / Март 2026
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
            <span className="legend-badge plan-legend-badge-yellow"></span> «ЛИГЕЯ» по Э.А.ПО
          </div>
          <div className="legend-item">Поэтические / прозаические пометки</div>
        </div>
      </div>
    </div>
  );
};

export default Calendar;
