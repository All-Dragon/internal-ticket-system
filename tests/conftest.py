import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.sql.sqltypes import Enum as SQLAlchemyEnum

from app.api.main import app
from app.core.config_app import generate_url_db
from app.db.database import get_async_session
from app.db.models import Base

for logger_name in ["api", "Bot", "uvicorn", "uvicorn.access", "uvicorn.error"]:
    logger = logging.getLogger(logger_name)
    for handler in logger.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            logger.removeHandler(handler)

url = generate_url_db() + "_Test"
test_engine = create_async_engine(url, poolclass=NullPool)


def _get_metadata_enum_names() -> list[str]:
    enum_names: set[str] = set()
    for table in Base.metadata.tables.values():
        for column in table.columns:
            if isinstance(column.type, SQLAlchemyEnum) and column.type.name:
                enum_names.add(column.type.name)
    return sorted(enum_names)


METADATA_ENUM_NAMES = _get_metadata_enum_names()


async def _drop_postgres_enum_types(conn) -> None:
    for enum_name in METADATA_ENUM_NAMES:
        await conn.execute(text(f'DROP TYPE IF EXISTS "{enum_name}" CASCADE'))


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await _drop_postgres_enum_types(conn)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await _drop_postgres_enum_types(conn)
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
