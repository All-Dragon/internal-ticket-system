from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config_app import Config, generate_url_db, load_config
from app.db.models import Base
from app.db.sqlite_functions import register_sqlite_functions

config: Config = load_config()
url = generate_url_db()
engine = create_async_engine(url)
event.listen(engine.sync_engine, "connect", register_sqlite_functions)
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
