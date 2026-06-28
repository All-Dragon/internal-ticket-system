from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.JWT.auth import get_current_user, require_role
from app.db.database import get_async_session
from app.db.models import User
from app.schemas import UserCreate, UserRead
from app.services import UserService

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("", response_model=list[UserRead])
async def get_users(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_role("admin")),
):
    users = await UserService.get_all(session=session)
    return [UserRead.model_validate(user) for user in users]


@users_router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserRead.model_validate(current_user)


@users_router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_role("admin")),
):
    user = await UserService.get_by_id(session=session, user_id=user_id)
    return UserRead.model_validate(user)


@users_router.post("", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def create_user(data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    user = await UserService.create(session=session, data=data)
    return UserRead.model_validate(user)
