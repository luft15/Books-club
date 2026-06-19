import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../assets/css/style.css';
import foto from '../assets/img/foto.jpg';
import foto2 from '../assets/img/foto_2.jpg';

const InformationPage = () => {
  const { user } = useAuth();

  return (
    <div className="info-page">
      
      <main>
        <div className="container">
          <article className="article">
            <div className="article-text">
              <p>Книжный клуб «BOOKSclub» — это место, где собираются те, кто любит читать и готов делиться своими впечатлениями. Мы встречаемся раз в две недели, чтобы обсудить одну книгу, которую заранее выбираем вместе голосованием. Никаких строгих правил, никаких оценок и обязательных списков литературы — только живое общение, чай и интересные разговоры. Можно прийти, даже если не успел дочитать книгу до конца, или просто послушать, что говорят другие. Встречи проходят как офлайн в уютном пространстве, так и онлайн в Zoom, чтобы участники из разных городов тоже могли присоединиться. Ближайшая встреча состоится 20.03 в 18:00, обсуждаем книгу «Джейн Эйр» . Место встречи или ссылка на трансляцию придут после регистрации. Если вы давно искали компанию, с которой можно поговорить о любимых героях, поспорить о сюжете или просто провести вечер в кругу книжных людей — добро пожаловать.</p>
            </div>
            <div className="article-with-images">
              <div className="article-images">
                <img src={foto2} alt="Встреча" className="side-image" />
                <img src={foto} alt="Книжный клуб" className="side-image" />
              </div>
            </div>
          </article>
        </div>
      </main>

    </div>
  );
};

export default InformationPage;