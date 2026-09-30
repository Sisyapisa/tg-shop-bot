from aiogram import types, F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from os import getenv

from telebot.apihelper import answer_web_app_query

from database import Order
from repositories.item import ItemRepo
from repositories.order import OrderRepo
from repositories.user import UserRepo
from states.order import OrderState
from utils.notify import notify_admin
from pathlib import Path
from dotenv import dotenv_values

env_path = Path(__file__).parent.parent / ".env"
config = dotenv_values(env_path)

router = Router()

@router.callback_query(F.data.startswith("start_order"))
async def start_order(callback: types.CallbackQuery, state: FSMContext, item_repo: ItemRepo):
    item_id = int(callback.data.split(":")[-1])

    item = await item_repo.get_item_id(item_id)
    if not item:
        await callback.answer("Товар не найден", show_alert=True)
        return

    await state.update_data(item_id=item_id)
    await state.set_state(OrderState.INPUT_NAME)

    await callback.message.answer(
        f"Оформляем заказ: {item.name}\n\n"
        f"Введите ваше имя ФИО:"
    )
    await callback.answer()

@router.message(OrderState.INPUT_NAME)
async def order_name(message: types.Message, state: FSMContext):
    if len(message.text) < 2:
        await message.answer("Введите корректное ФИО:")
        return

    await state.update_data(name = message.text)
    await message.answer("Введите ваш номер телефона:")
    await state.set_state(OrderState.INPUT_PHONE)

@router.message(OrderState.INPUT_PHONE)
async def order_phone(message: types.Message, state: FSMContext):
    if len(message.text) < 5:
        await message.answer("Введите корректный номер:")
        return
    await state.update_data(phone = message.text)
    await message.answer("Введите адресс доставки:")
    await state.set_state(OrderState.INPUT_ADDRESS)

@router.message(OrderState.INPUT_ADDRESS)
async def order_address(message: types.Message, state: FSMContext, item_repo: ItemRepo):
    if len(message.text) < 5:
        await message.answer("Введите корректный адрес:")
        return
    await state.update_data(address = message.text)

    data = await state.get_data()
    item = await item_repo.get_item_id(data['item_id'])

    await message.answer(
        f"Проверьте заказ:\n\n"
        f"Товар: {item.name}\n"
        f"Цена: {round(item.price / 100, 2)}\n"
        f"ФИО: {data['name']}\n"
        f"Телефон: {data['phone']}\n"
        f"Адрес: {data['address']}\n\n"
        f"Подтверждаете?",
        reply_markup = confirm_keyboard()
    )
    await state.set_state(OrderState.CONFIRM)

def confirm_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(text= "Подтвердить", callback_data="confirm_order")],
            [InlineKeyboardButton(text= "Отменить", callback_data="cancel_order")],
        ]
    )

@router.callback_query(OrderState.CONFIRM, F.data == "confirm_order")
async def confirm_order(
        callback: types.CallbackQuery,
        state: FSMContext,
        item_repo: ItemRepo,
        user_repo: UserRepo,
        order_repo: OrderRepo,
        bot: Bot,
):
    data = await state.get_data()
    item = await item_repo.get_item_id(data['item_id'])

    user = await user_repo.get_user_by_tg_id(callback.from_user.id)
    if not user:
        await callback.answer("Пользователь не найден", show_alert=True)
        return

    if user.balance < item.price:
        await callback.message.edit_text("Недостаточно монет на балансе!")
        await callback.answer()
        await state.clear()
        return

    await  user_repo.update_balance(callback.from_user.id, -item.price)

    order = await order_repo.create_order_with_details(
        user_id = user.id,
        item = item,
        customer_name = data['name'],
        customer_phone = data['phone'],
        delivery_address= data['address'],
    )

    await callback.message.edit_text(
        f"Заказ оформлен!!!\n\n"
        f"{item.name}\n"
        f"{round(item.price / 100, 2)}\n"
        f"Мы свяжемся для уточнения деталей."
    )
    await callback.answer()
    await state.clear()

    admin_id = int(config.get("ADMIN_ID", 0))
    await notify_admin(bot, admin_id,

                        f"Новый заказ #{order.id}\n\n"
                        f"<a href='tg://user?id={user.tg_id}'>{data['name']}</a>\n"
                        f"{data['name']}\n"
                       f"{data['phone']}\n"
                       f"{data['address']}\n"
                       f"{item.name}\n"
                       f"{round(item.price / 100, 2)} монет"

    )

@router.callback_query(OrderState.CONFIRM, F.data == "cancel_order")
async def cancel_order(
        callback: types.CallbackQuery,
        state: FSMContext
):
    await state.clear()
    await callback.message.edit_text("Заказ отменен")
    await callback.answer()