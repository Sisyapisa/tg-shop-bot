from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def admin_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text = "Статистика",callback_data="admin:stats")],
            [InlineKeyboardButton(text="Заказы", callback_data="admin:orders")],
            [InlineKeyboardButton(text="Юзеры", callback_data="admin:users")],
            [InlineKeyboardButton(text="Товары", callback_data="admin:items")]
        ]
    )

def back_to_admin():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text = "Назад", callback_data="admin:menu")]
        ]
    )

def admin_items_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Добавить товар", callback_data="admin:add_item")],
            [InlineKeyboardButton(text="Удалить товар", callback_data="admin:delete_item")],
            [InlineKeyboardButton(text="Назад", callback_data="admin:menu")],
        ]
    )

