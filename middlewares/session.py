from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message

from repositories.categories import CategoryRepo
from repositories.user import UserRepo
from repositories.item import ItemRepo
from repositories.order import OrderRepo


class DatabaseSessionMiddleware(BaseMiddleware):
    def __init__(self, session_maker)->None:
        self.session_maker = session_maker

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str,Any]], Awaitable[Any]],
            event:Message,
            data:Dict[str,Any]
    )->Any:
        async with self.session_maker() as session:
            data['user_repo']= UserRepo(session=session)
            data['category_repo'] = CategoryRepo(session=session)
            data['item_repo'] = ItemRepo(session=session)
            data['order_repo'] = OrderRepo(session=session)
            return await handler(event, data)