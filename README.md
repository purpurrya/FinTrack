# FinTrack

Пет-проект для практики.
FinTrack — API для учёта финансов, включающий мультивалютные кошельки, доходы/расходы, переводы между кошельками с конвертацией и журнал операций.

Курсы валют берутся из [fawazahmed0/exchange-api](https://github.com/fawazahmed0/exchange-api); если API недоступен, используется встроенный набор курсов.

## Технологии

- Python
- FastAPI
- SQLAlchemy
- Pydantic / pydantic-settings
- SQLite
- aiohttp
- pytest
- ruff
- uv

## Развёртывание

### Клонирование репозитория

```bash
git clone <repo-url>
cd Test
```

### Установка зависимостей

```bash
uv sync
```

### Настройка окружения

```bash
cp .env.example .env
```

### Запуск приложения

Таблицы БД создаются автоматически при старте приложения.

```bash
uv run fastapi dev main.py
```

API будет доступно по адресу:

```
http://localhost:8000/docs
```

## Запуск тестов

```bash
uv run pytest tests/ -v
```

## API

### Пользователи

- `POST /api/v1/users` — регистрация пользователя
- `GET /api/v1/users/me` — данные текущего пользователя

### Кошельки

- `POST /api/v1/wallets` — создание кошелька (с указанием валюты: `rub`, `usd`, `eur`)
- `GET /api/v1/wallets` — список кошельков пользователя
- `GET /api/v1/balance` — суммарный баланс по всем кошелькам, приведённый к рублю

### Операции

- `POST /api/v1/operations/income` — пополнение кошелька
- `POST /api/v1/operations/expense` — списание с кошелька
- `POST /api/v1/operations/transfer` — перевод между кошельками (с конвертацией, если валюты различаются)
- `GET /api/v1/operations` — журнал операций (фильтры по `wallet_id`, `date_from`, `date_to`)

## Структура проекта

- `main.py` — точка входа FastAPI-приложения
- `app/api/v1/` — роутеры (`users`, `wallets`, `operations`)
- `app/services/` — бизнес-логика
- `app/repository/` — доступ к данным (SQLAlchemy)
- `app/models.py` — ORM-модели
- `app/schemas.py` — Pydantic-схемы запросов/ответов
- `app/enums.py` — перечисления (валюты, типы операций)
- `app/database.py` — подключение к БД
- `app/config.py` — конфигурация из переменных окружения
- `app/dependency.py` — зависимости FastAPI (сессия БД, текущий пользователь)
- `tests/` — тесты (pytest)
