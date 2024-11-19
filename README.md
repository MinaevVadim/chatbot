# Чат-бот для трекинга привычек
Этот бот разработан по заказу центра подбора психологов, который
даёт пользователям возможность эффективно управлять привычками
через Telegram.

Основные функции сервиса:
1. Добавление, редактирование и удаление привычек;
2. Фиксация выполнения привычек;
3. Регулярные оповещения для соблюдения привычек;
4. Безопасное хранение и обработка данных пользователей;
5. Аутентификация и авторизация пользователей.

Этот сервис поможет клиентам центра достичь личные цели на пути
самосовершенствования. Также телеграм-бот станет удобным
инструментом для внедрения полезных привычек в повседневность.
Пользователи будут уверены в конфиденциальности своих данных и
оценят лёгкость работы с сервисом прямо в мессенджере.

### Технологический стек

В ходе реализации использовался следующий стек технологий:

* Poetry
* Postgresql.
* SQLAlchemy
* Alembic
* Aiogram
* FastAPI
* PyJWT
* Pytest, Factory-Boy, Faker
* Apscheduler
* Docker-compose.

### Установка

Чтобы запустить приложение и базу данных, выполните следующую команду:
```
docker compose up
```
И так же в оболочке shell внутри Docker для создания таблиц с помощью Alembic следующую команду:
```
Alembic revision --message="create tables" --autogenerate
```
Затем:
```
Alembic upgrade head
```
