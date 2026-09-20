from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import func
from sqlalchemy.sql import select

from database import Order, OrderItem

class OrderRepo:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create_order(self, user_id: int, item, quantity: int = 1)-> Order:
        order = Order(
            user_id = user_id,
            total = item.price * quantity,
            status = "paid"
        )
        self.__session.add(order)
        await self.__session.flush()

        order_item = OrderItem(
            order_id = order.id,
            item_id = item.id,
            item_name = item.name,
            price = item.price,
            quantity = quantity
        )
        self.__session.add(order_item)

        await self.__session.commit()
        return order

    async def get_user_orders(self, user_id: int):
        statement = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.items))
            .order_by(Order.created_at.desc())
        )
        result = await self.__session.scalars(statement)
        return result.all()

    async def get_all_orders(self, limit: int = 20):
        statement = (
            select(Order)
            .options(selectinload(Order.items))
            .order_by(Order.created_at.desc())
            .limit(limit)
        )
        result = await self.__session.scalars(statement)
        return result.all()

    async def get_stats(self):
        statement = select(
            func.count(Order.id),
            func.coalesce(func.sum(Order.total), 0)
        )
        result = await self.__session.execute(statement)
        return result.one()