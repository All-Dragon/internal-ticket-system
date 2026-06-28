from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.hash import hash_password
from app.db.models import User
from app.repositories import UserRepository
from app.schemas import UserCreate


class UserService:
    @staticmethod
    async def get_all(session: AsyncSession) -> list[User]:
        return (await UserRepository.get_all(session=session)).all()

    @staticmethod
    async def get_by_id(session: AsyncSession, user_id: int) -> User:
        user = await UserRepository.get_by_id(session=session, user_id=user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    async def create(session: AsyncSession, data: UserCreate) -> User:
        existing = await UserRepository.get_by_email(session=session, email=data.email)
        if existing is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        return await UserRepository.create(
            session=session,
            data=data,
            hashed_password=hash_password(data.password),
        )
