from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.enum import Role
from app.db.models import User
from app.schemas import UserCreate


class UserRepository:
    @staticmethod
    async def get_all(session: AsyncSession):
        return await session.scalars(select(User).order_by(User.id))

    @staticmethod
    async def get_by_id(session: AsyncSession, user_id: int) -> User | None:
        return await session.scalar(select(User).where(User.id == user_id))

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> User | None:
        return await session.scalar(select(User).where(User.email == email))

    @staticmethod
    async def create(session: AsyncSession, data: UserCreate, hashed_password: str) -> User:
        user = User(
            email=data.email,
            full_name=data.full_name,
            hashed_password=hashed_password,
            role=Role.user,
            is_active=True,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
