from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from database import Item
from database.models.category import Category

class ItemRepo:
    def __init__(self,session: AsyncSession):
        self.__session = session

    async def get_item(self,category_id):
        statement = select(Item).where(Item.category_id == category_id).order_by(Item.name)
        result = await self.__session.scalars(statement)
        return result.all()

    async def get_item_id(self, item_id):
        statement = select(Item).where(Item.id == item_id)
        return (await self.__session.scalar(statement))