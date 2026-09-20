from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Каталог")],
            [KeyboardButton(text="Профиль"), KeyboardButton(text="О нас")]
        ],
        resize_keyboard=True
    )