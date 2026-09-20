from sqlalchemy import BigInteger

from database.models import BaseModel
from sqlalchemy.orm import mapped_column, Mapped

class User(BaseModel):
    __tablename__ = 'users'

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id:Mapped[int] = mapped_column(BigInteger, unique=True)

    username:Mapped[str | None] = mapped_column()
    full_name: Mapped[str]

    balance:Mapped[int] = mapped_column(default=0)

    @property
    def view_balance(self):
        return round(self.balance / 100, 4)