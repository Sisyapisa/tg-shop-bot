from aiogram.filters import Filter
from aiogram import types
from os import getenv

class IsAdmin(Filter):
    async def __call__(self,event: types.Message | types.CallbackQuery)-> bool:
        admin_id = int(getenv("ADMIN_ID",0))
        if not admin_id:
            return False
        user_id = event.from_user.id
        return user_id == admin_id
