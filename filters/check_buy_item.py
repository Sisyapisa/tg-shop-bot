from aiogram.filters import Filter
from aiogram import types
from repositories.item import ItemRepo
from repositories.user import UserRepo


class FilterUserCanBuyItem(Filter):
    async def __call__(self,
                       callback: types.CallbackQuery,
                       item_repo: ItemRepo,
                       user_repo: UserRepo):
        try:
            item_id = int(callback.data.split(":")[-1])
        except (ValueError,IndexError):
            await callback.answer("Некорректные данные", show_alert=True)
            return False

        item = await item_repo.get_item_id(item_id)
        if not item:
            await callback.answer("Товар не найден", show_alert=True)
            return False

        user = await user_repo.get_user_by_tg_id(callback.from_user.id)
        if not user:
            await callback.answer("Пользователь не найден",show_alert = True)
            return False

        if user.balance < item.price:
            await callback.answer("Недостаточно монет!", show_alert=True)
            return False

        return True