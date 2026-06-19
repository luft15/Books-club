// frontend/src/components/common/Footer.jsx
import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-col">
            <div className="footer-logo">BOOKSclub</div>
            <p className="footer-description">
              Книжный клуб для тех, кто любит читать и обсуждать. Встречи, обсуждения, новые знакомства и хорошие книги.
            </p>
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
    </footer>
  );
};

export default Footer;
