# StarterKit

Full-stack starter kit в стиле проекта GTO: FastAPI API, React frontend, PostgreSQL, Redis, Alembic, Docker, nginx и CI.

## Что внутри

```text
app/
  api/main.py              # точка входа FastAPI
  api/routers/             # HTTP routes
  core/config_app.py       # чтение env и сборка DB URL
  core/JWT/                # JWT token, current user, role guard
  db/database.py           # async SQLAlchemy engine/session
  db/enum/                 # enum-типы приложения
  db/models/               # SQLAlchemy models
  repositories/            # запросы к базе
  schemas/                 # Pydantic request/response схемы
  services/                # бизнес-логика
  scripts/                 # seed/init scripts
alembic/                   # миграции Alembic
frontendReact/
  src/api/                 # функции запросов к backend
  src/components/          # UI-компоненты
  src/context/             # AuthContext
  src/hooks/               # формы и загрузка данных
  src/layouts/             # layout приложения
  src/pages/               # страницы роутинга
  src/styles/              # CSS
  src/utiles/              # frontend helpers
nginx/                     # nginx reverse proxy + static frontend
.github/workflows/ci.yml   # базовый CI
Dockerfile                 # backend image
docker-compose.yaml        # db + redis + app + nginx
requirements.txt           # Python dependencies
```

Backend-поток:

```text
router -> service -> repository -> model -> database
```

Frontend-поток:

```text
page -> component -> hook -> api module -> authFetch -> backend
```

## Env-файлы

В репозиторий коммитятся только examples:

- `.env.example` для локального запуска без Docker.
- `.env.docker.example` для запуска через `docker compose`.

Рабочие файлы создаются копированием:

```bash
copy .env.example .env
```

или для Docker:

```bash
copy .env.docker.example .env
```

Сам `.env` не коммитить.

## Где задавать данные БД

Все настройки backend читаются в `app/core/config_app.py`.

Главные переменные:

```env
DB_NAME=starterkit
DB_HOST=localhost
DB_PORT=5432
DB_USER=starterkit
DB_PASSWORD=starterkit
```

Для локального запуска `DB_HOST=localhost`.

Для Docker `DB_HOST=db`, потому что сервис Postgres в `docker-compose.yaml` называется `db`.

Итоговый async URL собирается функцией:

```python
generate_url_db()
```

Она используется в:

- `app/db/database.py`
- `alembic/env.py`

## JWT-настройки

В `.env`:

```env
SECRET_KEY=change_me_to_a_long_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

JWT-код лежит в:

```text
app/core/JWT/security.py
app/core/JWT/auth.py
app/core/JWT/token_shemas.py
```

## Redis-настройки

Redis уже есть в `docker-compose.yaml`, но в шаблоне он пока только подготовлен в конфиге.

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DATABASE=0
REDIS_USERNAME=
REDIS_PASSWORD=
```

Для Docker:

```env
REDIS_HOST=redis
```

## Локальный запуск backend

1. Создать виртуальное окружение:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Установить зависимости:

```bash
pip install -r requirements.txt
```

3. Создать `.env`:

```bash
copy .env.example .env
```

4. Убедиться, что PostgreSQL запущен и база из `.env` создана.

5. Применить миграции:

```bash
alembic upgrade head
```

6. Запустить API:

```bash
uvicorn app.api.main:app --reload
```

API будет доступно:

```text
http://localhost:8000
http://localhost:8000/docs
http://localhost:8000/health
```

## Локальный запуск frontend

```bash
cd frontendReact
npm install
npm run dev
```

Frontend будет доступен обычно на:

```text
http://localhost:5173
```

`frontendReact/vite.config.js` проксирует backend routes на `http://127.0.0.1:8000`.

## Docker-запуск

1. Создать `.env` для Docker:

```bash
copy .env.docker.example .env
```

2. Собрать и запустить:

```bash
docker compose up --build
```

В Docker поднимаются:

- `db` PostgreSQL
- `redis`
- `app` FastAPI
- `nginx` frontend + reverse proxy

Контейнер `app` перед запуском API выполняет:

```bash
alembic upgrade head
```

После запуска приложение будет доступно через nginx:

```text
http://localhost
```

## Alembic

Alembic уже подключен к проекту.

`alembic/env.py` берет:

- URL базы из `app.core.config_app.generate_url_db()`
- metadata моделей из `app.db.models.Base.metadata`

Создать миграцию:

```bash
alembic revision --autogenerate -m "initial"
```

Применить миграции:

```bash
alembic upgrade head
```

Откатить последнюю миграцию:

```bash
alembic downgrade -1
```

Папка миграций:

```text
alembic/versions/
```

## Как добавить новую backend-сущность

Допустим, нужна сущность `Product`.

1. Создать модель:

```text
app/db/models/product.py
```

2. Добавить импорт модели в:

```text
app/db/models/__init__.py
```

3. Создать Pydantic-схемы:

```text
app/schemas/product.py
```

4. Добавить exports в:

```text
app/schemas/__init__.py
```

5. Создать репозиторий:

```text
app/repositories/product.py
```

6. Добавить export в:

```text
app/repositories/__init__.py
```

7. Создать сервис:

```text
app/services/product.py
```

8. Добавить export в:

```text
app/services/__init__.py
```

9. Создать роутер:

```text
app/api/routers/product.py
```

10. Подключить роутер в:

```text
app/api/routers/__init__.py
app/api/main.py
```

11. Создать миграцию:

```bash
alembic revision --autogenerate -m "add products"
alembic upgrade head
```

## Как добавить frontend-экран для новой сущности

Для `Product` обычно нужны:

```text
frontendReact/src/api/products.js
frontendReact/src/hooks/useProducts.js
frontendReact/src/pages/ProductsPage.jsx
```

Потом добавить route в:

```text
frontendReact/src/App.jsx
```

И ссылку в меню:

```text
frontendReact/src/components/Header.jsx
```

## Auth flow

Регистрация:

```text
frontend RegisterForm -> useRegisterForm -> api/users.createUser -> POST /users
```

Логин:

```text
frontend LoginForm -> useLoginForm -> api/users.loginUser -> POST /auth/login
```

Профиль:

```text
AuthContext -> api/users.getUserProfile -> GET /users/me
```

Защищенные backend routes используют:

```python
current_user = Depends(get_current_user)
```

Ролевые routes используют:

```python
current_user = Depends(require_role("admin"))
```

## Тесты

Запуск:

```bash
pytest tests/ -v
```

CI находится здесь:

```text
.github/workflows/ci.yml
```

CI поднимает PostgreSQL и Redis, ставит зависимости, создает тестовую базу и запускает тесты.

## Полезные команды

Backend:

```bash
uvicorn app.api.main:app --reload
```

Frontend:

```bash
cd frontendReact
npm run dev
```

Docker:

```bash
docker compose up --build
```

Миграции:

```bash
alembic revision --autogenerate -m "message"
alembic upgrade head
```

Тесты:

```bash
pytest tests/ -v
```

## Перед первым коммитом

Рекомендуемый порядок:

```bash
git init
git add .
git commit -m "Create GTO-style fullstack starter kit"
```

Если уже создана первая миграция, проверь, что файл из `alembic/versions/` тоже попал в коммит.
