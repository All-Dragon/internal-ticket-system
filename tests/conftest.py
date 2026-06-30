import logging
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("ADMIN_USERNAME", "admin")
os.environ.setdefault("ADMIN_PASSWORD", "admin")
os.environ.setdefault("LOG_TO_FILE", "false")

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from app.api.main import app
from app.db.database import get_async_session
from app.db.models import Base
from app.db.sqlite_functions import register_sqlite_functions

for logger_name in ["app", "uvicorn", "uvicorn.access", "uvicorn.error"]:
    logger = logging.getLogger(logger_name)
    for handler in logger.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            logger.removeHandler(handler)

url = os.getenv("TEST_DATABASE_URL", "sqlite+aiosqlite:///:memory:")
test_engine = create_async_engine(url, poolclass=StaticPool)
event.listen(test_engine.sync_engine, "connect", register_sqlite_functions)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture
async def db_session():
    async with test_engine.connect() as connection:
        transaction = await connection.begin()
        session = AsyncSession(bind=connection, expire_on_commit=False)
        await session.begin_nested()

        @event.listens_for(session.sync_session, "after_transaction_end")
        def restart_savepoint(sync_session, transaction_):
            parent = getattr(transaction_, "_parent", None)
            if transaction_.nested and (parent is None or not parent.nested):
                sync_session.expire_all()
                if not connection.sync_connection.in_nested_transaction():
                    connection.sync_connection.begin_nested()

        try:
            yield session
        finally:
            await session.close()
            if transaction.is_active:
                await transaction.rollback()


@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_async_session():
        yield db_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        yield async_client

    app.dependency_overrides.clear()
