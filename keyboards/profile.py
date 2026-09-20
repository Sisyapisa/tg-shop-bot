from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def profile_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
            InlineKeyboardButton(text="Пополнить баланс", callback_data="deposit")
            ],

            [
                InlineKeyboardButton(text= 'Мои заказы', callback_data="my_orders")
            ]
        ]
    )

def cancel_deposit_action(text: str = "Отменить"):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=text, callback_data="cancel_deposit")
            ]
        ])

def apply_deposit_action():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да", callback_data="apply_deposit"),
                InlineKeyboardButton(text="Нет", callback_data="cancel_deposit")
            ]
        ])

def back_to_profile():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text = 'Назад', callback_data='back_to_profile'),],
        ]
    )