from database.models import BaseModel
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey


class Item(BaseModel):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int] # 1$ = 100
    photo: Mapped[str | None] = mapped_column()

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))