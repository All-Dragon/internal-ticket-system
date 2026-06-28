from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.JWT.auth import get_current_user, require_role
from app.db.database import get_async_session
from app.db.models import User
from app.schemas import ItemCreate, ItemRead, ItemUpdate
from app.services import ItemService

items_router = APIRouter(prefix="/items", tags=["items"])


@items_router.get("", response_model=list[ItemRead])
async def get_items(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_role("admin")),
):
    items = await ItemService.get_all(session=session)
    return [ItemRead.model_validate(item) for item in items]


@items_router.get("/my", response_model=list[ItemRead])
async def get_my_items(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    items = await ItemService.get_my_items(session=session, current_user=current_user)
    return [ItemRead.model_validate(item) for item in items]


@items_router.post("", status_code=status.HTTP_201_CREATED, response_model=ItemRead)
async def create_item(
    data: ItemCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    item = await ItemService.create(session=session, current_user=current_user, data=data)
    return ItemRead.model_validate(item)


@items_router.put("/{item_id}", response_model=ItemRead)
async def update_item(
    item_id: int,
    data: ItemUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    item = await ItemService.update(
        session=session,
        current_user=current_user,
        item_id=item_id,
        data=data,
    )
    return ItemRead.model_validate(item)


@items_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    await ItemService.delete(session=session, current_user=current_user, item_id=item_id)
