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

    async def create_item(
            self,
            name: str,
            description: str,
            price: int,
            photo:str|None,
            category_id: int
    ):
        item = Item(
            name=name,
            description=description,
            price=price,
            photo=photo,
            category_id=category_id
        )
        self.__session.add(item)
        await self.__session.commit()
        return item

    async def delete_item(self, item_id: int):
        item = await self.get_item_id(item_id)
        if item:
            await self.__session.delete(item)
            await self.__session.commit()