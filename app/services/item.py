from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Item, User
from app.repositories import ItemRepository
from app.schemas import ItemCreate, ItemUpdate


class ItemService:
    @staticmethod
    async def get_all(session: AsyncSession) -> list[Item]:
        return (await ItemRepository.get_all(session=session)).all()

    @staticmethod
    async def get_my_items(session: AsyncSession, current_user: User) -> list[Item]:
        return (await ItemRepository.get_by_owner(session=session, owner_id=current_user.id)).all()

    @staticmethod
    async def create(session: AsyncSession, current_user: User, data: ItemCreate) -> Item:
        return await ItemRepository.create(session=session, owner_id=current_user.id, data=data)

    @staticmethod
    async def update(session: AsyncSession, current_user: User, item_id: int, data: ItemUpdate) -> Item:
        item = await ItemService._get_owned_item(session=session, current_user=current_user, item_id=item_id)
        return await ItemRepository.update(session=session, item=item, data=data)

    @staticmethod
    async def delete(session: AsyncSession, current_user: User, item_id: int) -> None:
        item = await ItemService._get_owned_item(session=session, current_user=current_user, item_id=item_id)
        await ItemRepository.delete(session=session, item=item)

    @staticmethod
    async def _get_owned_item(session: AsyncSession, current_user: User, item_id: int) -> Item:
        item = await ItemRepository.get_by_id(session=session, item_id=item_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        if item.owner_id != current_user.id and current_user.role != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return item
