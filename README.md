# Internal Ticket System

Веб-приложение для регистрации и обработки внутренних заявок. Изначально проект был выполнен как тестовое задание, а затем расширен полноценным QA-контуром: API- и E2E-автотестами, Allure-отчётностью, изолированным тестовым окружением в Docker и CI pipeline.

Проект демонстрирует не только разработку приложения, но и практику ручного и автоматизированного тестирования: анализ требований, техники тест-дизайна, проверку REST API и UI, работу с accessibility-локаторами, поиск дефектов и их документирование.

## QA-возможности проекта

- API-тесты на `pytest`, `pytest-asyncio` и `HTTPX`.
- UI/E2E-тесты на `pytest-playwright` с Chromium.
- Page Object + Component Object для переиспользуемых UI-действий.
- Тестовые фабрики и фикстуры для подготовки независимых данных.
- Позитивные, негативные и граничные проверки.
- Проверки бизнес-правил, ролей и сохранения данных после перезагрузки.
- Параметризованные тесты фильтрации, сортировки и валидации.
- Allure features, stories, titles, severity и пошаговая детализация.
- Скриншот и URL страницы в Allure при падении UI-теста.
- Playwright trace и video при падении E2E в CI.
- Изолированная SQLite-база для API-тестов.
- Отдельный Docker Compose-проект и volume для E2E.
- GitHub Actions с раздельными jobs для API, frontend и E2E.
- QA-документация: тест-план, тест-кейсы, чек-лист и баг-репорты.

## Стек

### Приложение

- Backend: `Python 3.12`, `FastAPI`, `SQLAlchemy`, `Alembic`.
- Frontend: `React 19`, `TypeScript`, `Vite`.
- Database: `SQLite`.
- Auth: `JWT` для администратора.
- Infra: `Docker Compose`, `nginx`.

### Тестирование

- `pytest`, `pytest-asyncio`, `pytest-mock`.
- `HTTPX ASGITransport` для API-тестов без запуска внешнего сервера.
- `Playwright for Python`, `pytest-playwright`.
- `Allure Pytest`.
- Accessibility-локаторы Playwright: role, label и accessible name.
- GitHub Actions и Docker Compose.

## QA-документация

- [Тест-план](docs/qa/test-plan.md)
- [Тест-кейсы](docs/qa/test-cases.md)
- [Чек-лист](docs/qa/checklist.md)
- [Баг-репорты](docs/qa/bug-reports.md)

Документы отражают фактические функциональные сценарии и дефекты, обнаруженные во время разработки и тестирования проекта.

## Что реализовано

- Создание и просмотр заявок.
- Поиск по заголовку и описанию.
- Фильтрация по статусу и приоритету.
- Быстрые фильтры для типовых выборок.
- Сортировка по дате создания, приоритету и статусу.
- Изменение статуса заявки.
- Редактирование заявки.
- Удаление заявки администратором.
- Пагинация и изменение размера страницы.
- Вход и выход администратора.
- Состояния загрузки, пустого списка и ошибок API.
- Модальные окна просмотра, редактирования, создания и подтверждения удаления.
- Демо-данные для быстрого знакомства с приложением.

Параметры поиска, фильтрации, сортировки и пагинации передаются с frontend на backend, а итоговая выборка формируется на сервере.

## Бизнес-правила

- Администратор необходим для удаления заявок.
- Демо-учётные данные администратора: `admin:admin`.
- Заявку в статусе `done` нельзя редактировать.
- Заявку в статусе `done` нельзя удалить.
- Заявку нельзя перевести из `done` обратно в другой статус.
- При нарушении бизнес-правил API возвращает соответствующий HTTP-статус и сообщение об ошибке.

## Быстрый запуск приложения

Требования:

- Docker Desktop;
- свободный порт `80`.

Из корня проекта выполните:

```bash
docker compose --env-file .env.docker.example up --build
```

После запуска приложение доступно по адресу:

```text
http://localhost
```

Backend автоматически применяет миграции, создаёт SQLite-базу в Docker volume и добавляет демо-заявки, если таблица пуста.

Полезные команды:

```bash
docker compose ps
docker compose logs -f app
docker compose logs -f nginx
docker compose down
```

Удалить приложение вместе с локальной Docker-базой:

```bash
docker compose down -v
```

## Запуск API-тестов

Установите Python-зависимости:

```bash
python -m pip install -r requirements.txt
```

Запустите API-тесты:

```bash
pytest tests -v
```

Обычная команда `pytest` также запускает только каталог `tests`, поскольку он указан в `pytest.ini` как основной `testpaths`.

API-тесты не обращаются к запущенному серверу. `HTTPX` отправляет запросы непосредственно в FastAPI-приложение через `ASGITransport`. Для тестовой сессии создаётся отдельная SQLite-база в памяти, а изменения каждого теста откатываются транзакцией.

Покрываются:

- health check;
- успешная и неуспешная авторизация;
- получение списка и отдельной заявки;
- поиск без учёта регистра, включая кириллицу;
- создание и валидация заявки;
- изменение данных и статуса;
- запреты для заявки в статусе `done`;
- удаление с токеном администратора и без него;
- HTTP-статусы, схемы ответов и ключевые сообщения логов.

## Запуск E2E-тестов

E2E выполняются в настоящем браузере против полностью запущенного приложения. Чтобы тестовые заявки не попадали в локальную рабочую базу, используется отдельный Compose project с отдельным Docker volume.

### 1. Поднять E2E-окружение

```bash
docker compose -p internal-ticket-system-e2e --env-file e2e/.env.e2e.example up -d --build
```

Приложение будет доступно по адресу:

```text
http://localhost:8080
```

### 2. Установить Chromium для Playwright

```bash
python -m playwright install chromium
```

### 3. Запустить тесты

```bash
pytest e2e -v --browser=chromium --base-url=http://localhost:8080
```

Запуск только smoke-набора:

```bash
pytest e2e -v -m smoke --browser=chromium --base-url=http://localhost:8080
```

Запуск regression-набора:

```bash
pytest e2e -v -m regression --browser=chromium --base-url=http://localhost:8080
```

Запуск с видимым браузером:

```bash
pytest e2e -v --headed --browser=chromium --base-url=http://localhost:8080
```

### 4. Остановить окружение и удалить тестовую базу

```bash
docker compose -p internal-ticket-system-e2e --env-file e2e/.env.e2e.example down -v
```

E2E покрывают:

- позитивную и негативную авторизацию;
- создание заявки и клиентскую валидацию;
- граничные значения заголовка и описания;
- отображение заявки в таблице;
- изменение статуса;
- редактирование одного и нескольких полей;
- сохранение изменений после перезагрузки;
- просмотр актуальных данных в модальном окне;
- разрешённые и запрещённые сценарии удаления;
- поиск и состояние пустой выдачи;
- обычные и быстрые фильтры;
- совместное применение фильтров и их сброс;
- сортировку по дате, приоритету и статусу;
- навигацию по страницам и изменение размера страницы.

## Allure Report

Сформировать результаты:

```bash
pytest e2e -v --browser=chromium --base-url=http://localhost:8080 --alluredir=allure-results --clean-alluredir
```

Открыть интерактивный отчёт:

```bash
allure serve allure-results
```

Для второй команды должен быть отдельно установлен Allure Commandline. В отчёте тесты сгруппированы по feature и story, содержат severity и шаги. При падении теста автоматически прикладываются полноэкранный скриншот и URL страницы.

Для дополнительной диагностики можно сохранить trace и video:

```bash
pytest e2e -v --browser=chromium --base-url=http://localhost:8080 --tracing=retain-on-failure --video=retain-on-failure --alluredir=allure-results --clean-alluredir
```

## Frontend-проверки

```bash
cd frontendReact
npm ci
npm run typecheck
npm run lint
npm run build
```

## CI pipeline

Workflow `.github/workflows/ci.yml` запускается для pull request и push в ветки `main` и `refactor`.

Pipeline состоит из трёх jobs:

1. `api-tests` — устанавливает Python-зависимости и запускает API-тесты.
2. `frontend` — выполняет TypeScript typecheck, ESLint и production build.
3. `e2e-tests` — после успешных API и frontend jobs поднимает отдельное Docker-окружение, ожидает `/health`, запускает Chromium E2E и останавливает окружение.

E2E job выполняется со следующими диагностическими настройками:

- Allure results;
- Playwright trace при падении;
- video при падении;
- скриншот и URL из pytest hook;
- Docker logs при неуспешном job;
- публикация `allure-results` и `test-results` как CI-артефакта на 14 дней;
- гарантированное удаление E2E-контейнеров и volume после выполнения.

## Архитектура автотестов

```text
tests/
  conftest.py             изолированная БД и HTTPX-клиент
  test_auth.py            API авторизации
  test_health.py          health check
  test_ticket.py          API заявок и бизнес-правила

e2e/
  components/             UI-компоненты и модальные окна
  fixtures/               авторизация, фабрики и подготовка заявок
  models/                 enum и тестовые модели
  pages/                  Page Object главной страницы
  tests/                  пользовательские E2E-сценарии
  config.py               настройки E2E из environment
  conftest.py             browser context, fixtures и failure attachments

docs/qa/
  test-plan.md            стратегия и объём тестирования
  test-cases.md           подробные ручные сценарии
  checklist.md            чек-лист регрессионной проверки
  bug-reports.md          найденные дефекты и результаты ретеста
```

Локаторы строятся преимущественно через семантические границы, роли, label и accessible name. Компоненты инкапсулируют действия с конкретными областями UI, а тесты сохраняют фокус на пользовательских сценариях и проверках результата.

API используется в E2E-фикстурах только для быстрой подготовки предусловий. Ключевые пользовательские сценарии, например создание заявки и её появление в таблице, проходят полностью через UI.

## Локальный запуск для разработки

### Backend

Требования: Python 3.12.

Создайте виртуальное окружение, установите зависимости и создайте `.env` на основе `.env.example`. Затем выполните:

```bash
alembic upgrade head
uvicorn app.api.main:app --reload
```

При необходимости добавить демо-данные:

```bash
python -m app.utils.mock_data
```

Backend будет доступен по адресам:

```text
http://localhost:8000
http://localhost:8000/docs
http://localhost:8000/health
```

### Frontend

Требование: Node.js 22+.

```bash
cd frontendReact
npm install
npm run dev
```

Frontend будет доступен по адресу:

```text
http://localhost:5173
```

В dev-режиме Vite проксирует `/auth` и `/tickets` на backend `http://127.0.0.1:8000`.

## Переменные окружения

- `.env.example` — локальный запуск backend и frontend.
- `.env.docker.example` — обычный Docker-запуск с демо-данными.
- `e2e/.env.e2e.example` — изолированный Docker-запуск E2E на порту `8080` без демо-данных.

Рабочие `.env`-файлы, секреты, базы данных, логи и тестовые артефакты исключены из Git.

Основные переменные:

```text
DATABASE_URL
API_BASE_URL
VITE_API_BASE_URL
SECRET_KEY
ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
ADMIN_USERNAME
ADMIN_PASSWORD
SEED_DEMO_DATA
E2E_BASE_URL
APP_PORT
```

Приоритет конфигурации E2E: переменная окружения, значение из корневого `.env`, значение по умолчанию.

## API endpoints

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

Swagger UI доступен по адресу `http://localhost:8000/docs`.

## Структура приложения

```text
app/
  api/              FastAPI routes
  core/             config, JWT и logging
  db/               database, models, enums и SQLite helpers
  repositories/     database queries
  schemas/          Pydantic schemas
  services/         business logic
  utils/            demo seed data
alembic/            migrations
frontendReact/
  src/
    api/            запросы к backend
    components/     UI-компоненты
    hooks/          frontend logic и состояние
    pages/          страницы приложения
    styles/         CSS modules
    types/          TypeScript-типы
    utils/          frontend validation и helpers
nginx/              nginx config и frontend image
```

Backend:

```text
router -> service -> repository -> database
```

Frontend:

```text
page -> component -> hook -> api
```

## Логи и миграции

Применить миграции:

```bash
alembic upgrade head
```

Создать миграцию:

```bash
alembic revision --autogenerate -m "migration_name"
```

Логи приложения пишутся в консоль и в `logs/app.log`. В Docker их можно просмотреть командой:

```bash
docker compose logs -f app
```
