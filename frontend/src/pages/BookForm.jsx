// frontend/src/components/admin/BookForm.jsx
import React, { useState } from 'react';

const BookForm = ({ onSubmit }) => {
  const [newBook, setNewBook] = useState({ title: '', author: '', year: '' });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewBook((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(newBook);
    setNewBook({ title: '', author: '', year: '' });
  };

  return (
    <div className="admin-form-container">
      <h2>Добавить книгу</h2>
      <form onSubmit={handleSubmit}>
        <div className="admin-form-group">
          <label>Название</label>
          <input
            type="text"
            name="title"
            value={newBook.title}
            onChange={handleChange}
            required
            className="admin-form-control"
          />
        </div>
        <div className="admin-form-group">
          <label>Автор</label>
          <input
            type="text"
            name="author"
            value={newBook.author}
            onChange={handleChange}
            className="admin-form-control"
          />
        </div>
        <div className="admin-form-group">
          <label>Год</label>
          <input
            type="number"
            name="year"
            value={newBook.year}
            onChange={handleChange}
            className="admin-form-control"
          />
        </div>
        <button type="submit" className="admin-btn-success">
          Добавить книгу
        </button>
      </form>
    </div>
  );
};

export default BookForm;
