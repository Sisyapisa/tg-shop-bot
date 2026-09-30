from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def profile_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
            InlineKeyboardButton(text="Пополнить баланс", callback_data="deposit_menu")
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

def deposit_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="100 монет -- 100₽", callback_data="pay:100")],
            [InlineKeyboardButton(text="500 монет -- 500₽", callback_data="pay:500")],
            [InlineKeyboardButton(text="1000 монет -- 1000₽", callback_data="pay:1000")],
            [InlineKeyboardButton(text="Назад", callback_data="back_to_profile")]
        ]
    )