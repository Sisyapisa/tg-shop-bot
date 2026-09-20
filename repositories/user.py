from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from sqlalchemy.sql import select
from database.models.user import User
from sqlalchemy import func

class UserRepo:
    def __init__(self,session: AsyncSession):
        self.__session = session


    async def get_user_by_tg_id(self,tg_id: int):
        statement = select(User).where(User.tg_id==tg_id)

        return await self.__session.scalar(statement)

    async def create_or_update_user(self,tg_id:int, full_name:str, username:str):
        user = await self.get_user_by_tg_id(tg_id)

        if not user:
            await self.create_user(tg_id,full_name,username)
        else:
            user.full_name = full_name
            user.username = username

            await self.__session.commit()


    async def create_user(self,tg_id:int,full_name:str,username:str):
        user = User(tg_id=tg_id,full_name=full_name,username=username)
        self.__session.add(user)
        await self.__session.commit()

    async def update_balance(self, tg_id:int, amount:int):

        statement = update(User).where(User.tg_id==tg_id).values(balance=User.balance + amount)
        await self.__session.execute(statement)
        await self.__session.commit()

    async def get_all_users(self,limit:int = 20):
        statement = select(User).order_by(User.id.desc()).limit(limit)
        result = await self.__session.scalars(statement)
        return result.all()

    async def get_user_count(self):
        statement = select(func.count(User.id))
        return await self.__session.scalar(statement)
