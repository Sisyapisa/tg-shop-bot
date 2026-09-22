import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database.models import Category, Item

async def seed():
    engine = create_async_engine("sqlite+aiosqlite:///item_shop.db")
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async with session_maker() as session:
        shoes = Category(name="Кросовки", description="Кросовки спортивные")
        boots = Category(name="Ботинки", description="Ботинки")
        slippers = Category(name="Тапочки", description="Домашние тапочки")

        session.add_all([shoes, boots, slippers])
        await session.flush()

        items =  [Item(
                category_id=shoes.id,
                name="Nike Air Max",
                description="Легендарные кроссовки для бега и повседневной носки",
                price=10000,
                photo="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800",
            ),
            Item(
                category_id=shoes.id,
                name="Adidas Ultraboost",
                description="Топовая модель для спорта с амортизацией Boost",
                price=20000,
                photo="https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=800",
            ),
            Item(
                category_id=shoes.id,
                name="Puma RS-X",
                description="Стильные и удобные кроссовки",
                price=15000,
                photo="https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=800",
            ),

            # Ботинки
            Item(
                category_id=boots.id,
                name="Timberland",
                description="Крепкие ботинки для любой погоды",
                price=30000,
                photo="https://picsum.photos/seed/timberland/600/600",
            ),
            Item(
                category_id=boots.id,
                name="Dr. Martens",
                description="Классика стиля и комфорта",
                price=25000,
                photo="https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=800",
            ),
            Item(
                category_id=boots.id,
                name="Caterpillar",
                description="Рабочие ботинки повышенной прочности",
                price=28000,
                photo="https://picsum.photos/seed/caterpillar/600/600",
            ),

            # Тапочки
            Item(
                category_id=slippers.id,
                name="Домашние уютные",
                description="Мягкие тапочки для дома",
                price=5000,
                photo="https://images.unsplash.com/photo-1603808033192-082d6919d3e1?w=800",
            ),
            Item(
                category_id=slippers.id,
                name="Пляжные",
                description="Удобные шлёпанцы для отдыха на море",
                price=3000,
                photo="https://images.unsplash.com/photo-1603487742131-4160ec999306?w=800",
            ),
            Item(
                category_id=slippers.id,
                name="Банные",
                description="Тапочки для сауны и бани",
                price=4000,
                photo="https://images.unsplash.com/photo-1603808033192-082d6919d3e1?w=800",
            ),
        ]

        session.add_all(items)
        await session.commit()

    print("ОК! БД заполнена!")
    await engine.dispose()

if __name__ == '__main__':
    asyncio.run(seed())