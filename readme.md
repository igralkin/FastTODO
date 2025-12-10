# FastTODO

FastTODO — сервис для управления задачами, реализованный на FastAPI.  
Хранение данных осуществляется в PostgreSQL. Поддерживается JWT-аутентификация.

## Стек технологий

- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Docker / Docker Compose
- Pytest

---

## Запуск проекта

### 1. Запуск через Docker Compose (рекомендуется)

```bash
docker compose up --build
```

После запуска:

- API доступен по адресу: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

Файл `.env` генерируется автоматически из `.env.example`, если отсутствует.

---

## Аутентификация

Для доступа к эндпоинтам задач требуется JWT-токен.

### Получение токена

`POST /login`

Параметры (формат `application/x-www-form-urlencoded`):

- `username=firstuser`
- `password=first_user_password`

Пример ответа:

```json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

Использование токена:

```
Authorization: Bearer <JWT>
```

---

## Эндпоинты API

### 1. Корневой эндпоинт

**GET /**  
Возвращает сообщение о работоспособности сервиса:

```json
{"message": "FastTODO service is running"}
```

---

### 2. Аутентификация

#### **POST /login**  
Получение JWT-токена.

---

### 3. Работа с задачами (требуется Bearer-токен)

#### **POST /tasks/create**  
Создание задачи.

Тело запроса:

```json
{
  "datetime_to_do": "2025-12-31T12:00:00",
  "task_info": "Описание задачи"
}
```

Статус: `201 Created`

---

#### **GET /tasks/{task_id}**  
Получение задачи по ID.  
Если не найдено — `404 Task not found`.

---

#### **PATCH /tasks/{task_id}/update**  
Обновление задачи (частичное).

Тело запроса (поля опциональны):

```json
{
  "datetime_to_do": "2026-01-01T09:00:00",
  "task_info": "Новое описание"
}
```

---

#### **GET /tasks**  
Получение списка всех задач.

---

## Запуск тестов

### 1. Через Docker

```bash
docker compose run --rm web pytest
```

---

### 2. Без Docker

1. Создать виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
```

2. Установить зависимости:

```bash
pip install -r requirements.txt
```

3. Настроить `.env`, например:

```env
DATABASE_URL=postgresql://postgres_login:postgres_password@localhost:5432/postgres_database
JWT_SECRET_KEY=12345
```

4. Запустить тесты:

```bash
pytest
```

---

## Документация API

Swagger UI доступен по адресу:

```
http://localhost:8000/docs
```

---

## Лицензия

Проект создан в учебных целях.
