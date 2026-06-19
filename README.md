# Booksclub

Запустить:

```sh
docker compose up -d --build
```

```sh
docker compose logs -f
```


```sh
docker compose exec backend bash
```


```sh
docker compose exec db psql -U postgres -d barbershop
```


```sh
docker compose exec backend alembic upgrade head
```


```sh
docker compose exec backend python seed.py
```

```sh
docker compose down
```

```sh
docker compose down -v
```

`
Метод 	 URL	                   Описание
POST 	 /api/auth/register 	   Регистрация
POST     /api/auth/login	       Логин (JWT)
GET	     /api/auth/me	           Текущий пользователь
GET	     /api/services/	           Список услуг
GET	     /api/appointments/my      Мои записи
POST	 /api/appointments/	       Создать запись
GET	     /api/admin/stats	       Статистика (админ)
`

Swagger документация: http://localhost:8000/docs