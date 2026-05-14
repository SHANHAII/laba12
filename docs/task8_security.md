# Задание 8: Поиск уязвимостей в коде

## Промпт в Claude Code

> "Выступи в роли security code reviewer. Проанализируй код FastAPI-приложения
> (app/routers/accounts.py, app/schemas.py, app/crud.py).
> Найди потенциальные уязвимости: SQL-инъекции, XSS, незащищённые эндпоинты,
> отсутствие валидации, незакрытые соединения. Дай отчёт и способы исправления."

---

## Найденные проблемы и исправления

### 1. Отсутствует аутентификация на всех эндпоинтах

**Что сгенерировал ИИ:**
```python
@router.get("/", response_model=List[AccountResponse])
def list_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_accounts(db, skip=skip, limit=limit)
```

**В чём проблема:**  
Любой пользователь без авторизации может получить список всех счетов, создать или удалить счёт. Это критическая уязвимость в банковском приложении.

**Как исправить:**
```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

@router.get("/", response_model=List[AccountResponse])
def list_accounts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    # verify_token(credentials.credentials)
    return crud.get_accounts(db, skip=skip, limit=limit)
```

---

### 2. Отсутствие лимита на параметр `limit` (DoS через пагинацию)

**Что сгенерировал ИИ:**
```python
def list_accounts(skip: int = 0, limit: int = 100, ...):
```

**В чём проблема:**  
Параметр `limit` принимает любое число. Запрос `GET /accounts/?limit=1000000` заставит БД вернуть миллион строк, что может привести к исчерпанию памяти.

**Как исправил:**  
В [app/routers/accounts.py](../app/routers/accounts.py) добавлена аннотация с ограничением:
```python
from typing import Annotated
from fastapi import Query

def list_accounts(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    ...
```

---

### 3. Нет ограничения на длину строк в базе данных vs Pydantic

**Что сгенерировал ИИ:**  
В `schemas.py` поле `owner_name` имеет `max_length=100`, но в модели SQLAlchemy — `VARCHAR(100)`. Это согласовано. Однако поле `currency` в модели — `VARCHAR(3)`, а в Pydantic — `Literal["RUB","USD","EUR"]`. Если в БД попадёт невалидное значение напрямую (через миграцию), Pydantic упадёт при чтении.

**Как исправил:**  
Добавлена валидация при чтении из БД через `field_validator` в `AccountResponse`.

---

### 4. Утечка информации в сообщениях об ошибках

**Что сгенерировал ИИ:**
```python
raise HTTPException(
    status_code=409,
    detail=f"Счёт с номером {account.account_number} уже существует",
)
```

**В чём проблема:**  
Сообщение об ошибке подтверждает злоумышленнику, что такой номер счёта существует в системе (enumeration attack).

**Как исправил** (в [app/routers/accounts.py](../app/routers/accounts.py)):
```python
raise HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Счёт с таким номером уже существует",
    # Не раскрываем сам номер
)
```

---

### 5. Нет защиты от массового создания аккаунтов (rate limiting)

**В чём проблема:**  
Эндпоинт `POST /accounts/` позволяет создавать неограниченное число счетов подряд без задержки.

**Как исправить:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/")
@limiter.limit("10/minute")
def create_account(...):
```

---

## Итог

| # | Уязвимость | Критичность | Статус |
|---|-----------|-------------|--------|
| 1 | Нет аутентификации | Критическая | Описано, требует JWT |
| 2 | Безлимитная пагинация (DoS) | Средняя | Исправлено (`le=1000`) |
| 3 | Несоответствие типов БД/Pydantic | Низкая | Описано |
| 4 | Enumeration через сообщение 409 | Средняя | Исправлено |
| 5 | Нет rate limiting | Средняя | Описано, требует slowapi |
