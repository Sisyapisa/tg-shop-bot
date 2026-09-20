from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import BaseModel

class Order(BaseModel):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    total: Mapped[int]
    status: Mapped[str] = mapped_column(default='pending')
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    items: Mapped[list["OrderItem"]] = relationship(back_populates='order', cascade = 'all, delete-orphan')

class OrderItem(BaseModel):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'))

    item_name: Mapped[str]
    price: Mapped[int]
    quantity: Mapped[int] = mapped_column(default=1)

    order: Mapped["Order"] = relationship(back_populates='items')