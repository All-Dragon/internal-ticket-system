from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Item
from app.schemas import ItemCreate, ItemUpdate


class ItemRepository:
    @staticmethod
    async def get_all(session: AsyncSession):
        return await session.scalars(select(Item).order_by(Item.id.desc()))

    @staticmethod
    async def get_by_id(session: AsyncSession, item_id: int) -> Item | None:
        return await session.scalar(select(Item).where(Item.id == item_id))

    @staticmethod
    async def get_by_owner(session: AsyncSession, owner_id: int):
        return await session.scalars(
            select(Item).where(Item.owner_id == owner_id).order_by(Item.id.desc())
        )

    @staticmethod
    async def create(session: AsyncSession, owner_id: int, data: ItemCreate) -> Item:
        item = Item(owner_id=owner_id, title=data.title, description=data.description)
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item

    @staticmethod
    async def update(session: AsyncSession, item: Item, data: ItemUpdate) -> Item:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)
        await session.commit()
        await session.refresh(item)
        return item

    @staticmethod
    async def delete(session: AsyncSession, item: Item) -> None:
        await session.delete(item)
        await session.commit()
