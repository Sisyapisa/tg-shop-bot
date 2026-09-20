from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class CategoryCBData(CallbackData,prefix="category"):
    category_id: int

class ItemCBData(CallbackData,prefix="item"):
    id : int

class BuyItemCBData(CallbackData,prefix="buy"):
    id : int

def generate_catalog_kb(categories):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for category in categories:
        keyboard.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=category.name,
                    callback_data=CategoryCBData(category_id=category.id).pack())
            ]
        )

    return keyboard

def generate_items_kb(items):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for item in items:
        keyboard.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=item.name,
                    callback_data= ItemCBData(id = item.id).pack()
                )
            ]
        )


    keyboard.inline_keyboard.append(
        [
            InlineKeyboardButton(text="Назад", callback_data="catalog")
        ]
    )


    return keyboard

def back_to_category_items(item_id, category_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Купить",
                callback_data = BuyItemCBData(id=item_id).pack()
            )],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data= CategoryCBData(category_id=category_id).pack()
                )
            ]
        ]
    )