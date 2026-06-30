# Internal Ticket System

Проект выполнен как тестовое задание на стек:

- Backend: `Python`, `FastAPI`, `SQLAlchemy`, `Alembic`
- Frontend: `React`, `TypeScript`, `Vite`
- Database: `SQLite`
- Auth: `JWT` для входа администратора
- Infra: `Docker Compose`, `nginx`

## Что реализовано

- Создание заявки.
- Просмотр списка заявок.
- Фильтрация по `status` и `priority`.
- Поиск по `title` и `description`.
- Сортировка по дате создания и приоритету.
- Изменение статуса заявки.
- Редактирование заявки, если она не в статусе `done`.
- Удаление заявки только администратором.
- Пагинация списка.
- Админский вход.
- Состояния загрузки, пустого списка и ошибок API.
- Модальные окна для просмотра, редактирования, создания и подтверждения удаления.
- Демо-данные для быстрого просмотра приложения.

Фронт управляет параметрами поиска, фильтрации, сортировки и пагинации, а итоговая выборка выполняется на backend.

## Бизнес-правила

- Администратор нужен только для удаления заявок.
- Дефолтные креды администратора: `admin:admin`.
- Заявку в статусе `done` нельзя редактировать.
- Заявку в статусе `done` нельзя удалить.
- Заявку нельзя перевести из `done` обратно в другой статус.
- При нарушении бизнес-правил API возвращает осмысленный HTTP-статус и сообщение об ошибке.

## Требования

- Python 3.12
- Node.js 22+
- Docker Desktop, если используется Docker-запуск

## Переменные окружения

В проекте есть два example-файла:

- `.env.example` - для локального запуска backend/frontend;
- `.env.docker.example` - для запуска через Docker Compose.

Для локального запуска можно создать рабочий `.env`:

```bash
copy .env.example .env
```

Для Docker можно запускать напрямую через example-файл:

```bash
docker compose --env-file .env.docker.example up --build
```

Локальный пример:

```env
DATABASE_URL=sqlite+aiosqlite:///./app.db
API_BASE_URL=http://localhost:8000
VITE_API_BASE_URL=http://localhost:8000
SECRET_KEY=your_super_secret_key_change_this_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin
```

Docker-пример:

```env
DATABASE_URL=sqlite+aiosqlite:////app/data/app.db
API_BASE_URL=http://app:8000
VITE_API_BASE_URL=
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin
SEED_DEMO_DATA=true
```

Рабочие `.env`-файлы не нужно коммитить.

## Быстрый запуск через Docker

Из корня проекта:

```bash
docker compose --env-file .env.docker.example up --build
```

Это основной сценарий запуска для проверки проекта. После выполнения команды приложение уже готово к работе: backend автоматически применяет миграции, создает SQLite-базу в Docker volume и при пустой таблице добавляет демо-заявки.

После запуска приложение будет доступно:

```text
http://localhost
```

Отдельно запускать миграции для Docker не нужно. Они выполняются автоматически перед стартом API:

```bash
alembic upgrade head
```

После миграций автоматически запускается заполнение демо-данными:

```bash
python -m app.utils.mock_data
```

Демо-данные добавляются только если таблица заявок пустая. При повторном запуске контейнера дубли не создаются.

Если нужно запустить без демо-данных, поменяйте в `.env.docker.example`:

```env
SEED_DEMO_DATA=false
```

Полезные Docker-команды:

```bash
docker compose ps
docker compose logs -f app
docker compose logs -f nginx
docker compose down
```

Полностью удалить SQLite volume и начать с чистой базы:

```bash
docker compose down -v
docker compose --env-file .env.docker.example up --build
```

Важно: при первой сборке Docker должен скачать образы `python`, `node` и `nginx` с Docker Hub. Если сборка падает на `failed to resolve source metadata`, проверьте интернет, DNS или proxy-настройки Docker Desktop.

## Локальный запуск backend

Создать и активировать виртуальное окружение:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

Создать локальный env-файл:

```bash
copy .env.example .env
```

Применить миграции:

```bash
alembic upgrade head
```

При необходимости добавить демо-данные:

```bash
python -m app.utils.mock_data
```

Запустить backend:

```bash
uvicorn app.api.main:app --reload
```

Backend будет доступен:

```text
http://localhost:8000
http://localhost:8000/docs
http://localhost:8000/health
```

## Локальный запуск frontend

В отдельном терминале:

```bash
cd frontendReact
npm install
npm run dev
```

Frontend будет доступен:

```text
http://localhost:5173
```

В dev-режиме Vite проксирует `/auth` и `/tickets` на backend `http://127.0.0.1:8000`.

## API endpoints

Основные endpoints:

```text
GET    /health
POST   /auth/login
GET    /tickets
GET    /tickets/{id}
POST   /tickets
PATCH  /tickets/{id}
PATCH  /tickets/{id}/status
DELETE /tickets/{id}
```

`DELETE /tickets/{id}` требует авторизации администратора.

Параметры списка заявок:

```text
status: new | in_progress | done
priority: low | normal | high
search: string
sort_by: created_at | priority | status
sort_order: asc | desc
page: number
page_size: number
```

Swagger UI доступен по адресу:

```text
http://localhost:8000/docs
```

## Тесты и проверки

Backend:

```bash
pytest
```

Frontend typecheck:

```bash
cd frontendReact
npm run typecheck
```

Frontend lint:

```bash
cd frontendReact
npm run lint
```

Frontend production build:

```bash
cd frontendReact
npm run build
```

## Миграции

Применить миграции:

```bash
alembic upgrade head
```

Создать новую миграцию:

```bash
alembic revision --autogenerate -m "migration_name"
```

Текущая SQLite-база при локальном запуске создается как `app.db` в корне проекта. В Docker база хранится в volume `sqlite_data`.

## Логи

Логи пишутся в консоль и в файл:

```text
logs/app.log
```

В Docker логи удобнее смотреть так:

```bash
docker compose logs -f app
```

Файлы логов не коммитятся.

## Структура проекта

```text
app/
  api/              FastAPI routes
  core/             config, JWT, logging
  db/               database, models, enums, SQLite helpers
  repositories/     database queries
  schemas/          Pydantic schemas
  services/         business logic
  utils/            demo seed data
alembic/            migrations
frontendReact/
  src/
    api/            запросы к backend
    components/     UI-компоненты
    hooks/          frontend logic и работа с состоянием
    pages/          страницы приложения
    styles/         CSS modules
    types/          TypeScript-типы
    utils/          frontend helpers и validation
nginx/              nginx config and frontend image
tests/              backend tests
```

Backend использует слойность:

```text
router -> service -> repository -> database
```

Frontend разделен на:

```text
page -> component -> hook -> api
```
