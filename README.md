# Banking API — Лабораторная работа №12

**ФИО:** Шанхаи Рома  
**Группа:** (укажите группу)  
**Вариант:** 10 — Банковское приложение  
**Предметная область:** Счета, карты, переводы, платежи, история

---

## Описание проекта

REST API для управления банковскими счетами на FastAPI + SQLAlchemy + SQLite/PostgreSQL.

**Функционал:**
- CRUD для банковских счетов
- Валидация номера счёта по формату `XX000000000000000000` (2 буквы + 18 цифр)
- Поддержка валют: RUB, USD, EUR
- Типы счетов: checking (расчётный), savings (накопительный)

---

## Установка и запуск

### Локально

```bash
# Создать виртуальное окружение
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS

# Установить зависимости
pip install -r requirements.txt

# Запустить сервер
uvicorn app.main:app --reload
```

API будет доступен по адресу: http://localhost:8000  
Swagger UI: http://localhost:8000/docs

### Docker

```bash
docker-compose up --build
```

### Переменные окружения

| Переменная     | Значение по умолчанию        | Описание            |
|----------------|------------------------------|---------------------|
| DATABASE_URL   | sqlite:///./banking.db       | URL базы данных     |

Скопируйте `.env.example` в `.env` и при необходимости измените значения.

---

## Запуск тестов

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

Покрытие: **96%**

---

## API Endpoints

### GET /accounts/
Список всех счетов.

**Query параметры:** `skip` (int, default 0), `limit` (int, default 100)

**Пример ответа:**
```json
[
  {
    "id": 1,
    "owner_name": "Иван Иванов",
    "account_number": "RU123456789012345678",
    "balance": 1000.0,
    "currency": "RUB",
    "account_type": "checking",
    "is_active": true,
    "created_at": "2026-05-14T12:00:00"
  }
]
```

### POST /accounts/
Создать новый счёт.

**Тело запроса:**
```json
{
  "owner_name": "Иван Иванов",
  "account_number": "RU123456789012345678",
  "balance": 1000.0,
  "currency": "RUB",
  "account_type": "checking"
}
```

**Коды ответа:** `201 Created`, `409 Conflict` (дубликат номера), `422 Unprocessable Entity`

### GET /accounts/{id}
Получить счёт по ID.

**Коды ответа:** `200 OK`, `404 Not Found`

### PUT /accounts/{id}
Обновить данные счёта (частичное обновление).

**Тело запроса** (все поля опциональны):
```json
{
  "balance": 5000.0,
  "is_active": false
}
```

### DELETE /accounts/{id}
Удалить счёт. Возвращает удалённый объект.

**Коды ответа:** `200 OK`, `404 Not Found`

---

## Структура проекта

```
.
├── app/
│   ├── main.py          # Точка входа FastAPI
│   ├── database.py      # Подключение к БД
│   ├── models.py        # SQLAlchemy модели
│   ├── schemas.py       # Pydantic схемы
│   ├── crud.py          # CRUD операции
│   └── routers/
│       └── accounts.py  # Роутер для счетов
├── tests/
│   ├── conftest.py      # Фикстуры pytest
│   └── test_accounts.py # 19 тестов, покрытие 96%
├── docs/
│   ├── task3_refactoring.py      # Задание 3
│   ├── task5_code_explanation.md # Задание 5
│   ├── task7_migrations.sql      # Задание 7
│   ├── task8_security.md         # Задание 8
│   ├── task9_sql_query.sql       # Задание 9
│   └── task10_regex.py           # Задание 10
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── PROMPT_LOG.md
```
