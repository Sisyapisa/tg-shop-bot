from aiogram import F, Router, types

router = Router()

@router.message(F.text == "О нас")
async def info(message: types.Message):
    await message.answer("Я крутой бот для покупки обуви, выбери что тебе понравится в Каталоге.")