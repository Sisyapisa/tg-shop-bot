from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def admin_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text = "Статистика",callback_data="admin:stats")],
            [InlineKeyboardButton(text="Заказы", callback_data="admin:orders")],
            [InlineKeyboardButton(text="Юзеры", callback_data="admin:users")]
        ]
    )

def back_to_admin():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text = "Назад", callback_data="admin:menu")]
        ]
    )

