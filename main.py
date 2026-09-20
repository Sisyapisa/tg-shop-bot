from aiogram import Bot, Dispatcher
import asyncio
from Handlers import register_router
from database.models import BaseModel
from middlewares import register_middleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from os import getenv
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в .env")

async def init_model(engine):
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

async def main():
    bot = Bot(token= TOKEN)
    dp = Dispatcher()

    engine = create_async_engine(url = "sqlite+aiosqlite:///item_shop.db")

    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    register_middleware(dp,session_maker)

    register_router(dp)

    await init_model(engine)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
