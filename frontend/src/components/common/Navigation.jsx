// frontend/src/components/common/Navigation.jsx
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Navigation = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="header">
      <div className="nav">
        <div className="container-wide">
          <div className="row space-beetween">
            <div className="logo">BOOKSclub</div>
            <div className="nav-menu">
              <ul>
                <li><Link to="/">Главная</Link></li>
                <li><Link to="/information">Информация</Link></li>
                <li><Link to="/plan">Расписание</Link></li>
                {user && (
                  <>
                    <li><Link to="/profile">Мои записи</Link></li>
                    {user.is_admin && <li><Link to="/admin">Админ панель</Link></li>}
                  </>
                )}
              </ul>
            </div>
            <div>
              {user ? (
                <>
                  <span style={{ marginRight: '10px', color: 'white' }}>{user.username}</span>
                  <button
                    onClick={handleLogout}
                    className="login"
                    style={{ background: 'none', border: 'none', cursor: 'pointer' }}
                  >
                    Выйти
                  </button>
                </>
              ) : (
                <Link to="/login" className="login">Войти</Link>
              )}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navigation;
