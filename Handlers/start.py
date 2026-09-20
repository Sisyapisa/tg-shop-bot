from aiogram import Router, types
from aiogram.filters import Command
from keyboards.menu import main_menu_kb
from repositories.user import UserRepo

router = Router()

@router.message(Command('start'))
async def start_bot(message: types.Message, user_repo: UserRepo):
    await user_repo.create_or_update_user(message.from_user.id, message.from_user.full_name,message.from_user.username)
    await message.answer(f"Привет,{message.from_user.first_name}\n я магазин обуви, выбери нужное меню снизу",
    reply_markup =main_menu_kb()
    )
