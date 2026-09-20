from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from database.models.category import Category

class CategoryRepo:
    def __init__(self,session: AsyncSession):
        self.__session = session

    async def get_list(self):
        statement = select(Category).order_by(Category.name)
        result =     await self.__session.scalars(statement)
        return result.all()

    async def get_by_id(self,category_id:int):
        statement = select(Category).where(Category.id == category_id)
        return await self.__session.scalar(statement)

    # async def get_by_id(self,category_id:int):
    #     statement = select(Category).where(Category.id == category_id)
    #     return self.__session.scalar(statement)