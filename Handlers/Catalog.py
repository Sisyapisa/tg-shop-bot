from aiogram import F, Router, types, Bot
from aiogram.exceptions import TelegramBadRequest

import keyboards
from filters.check_buy_item import FilterUserCanBuyItem
from keyboards.catalog import generate_catalog_kb, CategoryCBData,generate_items_kb,ItemCBData,back_to_category_items,BuyItemCBData
from repositories import categories
from repositories.categories import CategoryRepo
from repositories.item import ItemRepo
from repositories.order import OrderRepo
from repositories.user import UserRepo
from os import getenv
from utils.notify import notify_admin

router = Router()


@router.message(F.text == "Каталог")
async def catalog_msg(message: types.Message, category_repo: CategoryRepo):
    categories = await category_repo.get_list()
    await message.answer(
        "Наш каталог:",
        reply_markup=generate_catalog_kb(categories),
    )


@router.callback_query(F.data == "catalog")
async def catalog_cb(callback: types.CallbackQuery, category_repo: CategoryRepo):
    categories = await category_repo.get_list()
    text = "Наш каталог:"
    keyboard = generate_catalog_kb(categories)

    if callback.message.photo:
        try:
            await callback.message.delete()
        except TelegramBadRequest:
            pass
        await callback.message.answer(text, reply_markup=keyboard)
    else:
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except TelegramBadRequest:
            pass
    await callback.answer()

@router.callback_query(CategoryCBData.filter())
async def catalog_info(
        callback: types.CallbackQuery,
        callback_data: CategoryCBData,
        category_repo: CategoryRepo,
        item_repo: ItemRepo):

    category = await category_repo.get_by_id(callback_data.category_id)
    if not category:
        await callback.answer("Категория не найдена", show_alert=True)
        return

    items = await item_repo.get_item(callback_data.category_id)
    keyboard = generate_items_kb(items)
    text = category.description

    if callback.message.photo:
        try:
            await callback.message.delete()
        except TelegramBadRequest:
            pass
        await callback.message.answer(text, reply_markup=keyboard)
    else:
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except TelegramBadRequest as e:
            if "message is not modified" not in str(e):
                raise

    await callback.answer()


@router.callback_query(ItemCBData.filter())
async def item_info(callback: types.CallbackQuery,callback_data: ItemCBData, item_repo: ItemRepo):
    item = await item_repo.get_item_id(callback_data.id)
    if not item:
        await callback.answer("Товар не найден", show_alert=True)
        return

    text =(
        f"Название - {item.name}\n"
        f"Описание - {item.description}\n"
        f"Стоимость - {round(item.price / 100, 2)} монет\n"
        "Хотите приобрести?"
    )
    keyboard = back_to_category_items(item.id, item.category_id)

    if item.photo:
        try:
            await callback.message.delete()
        except TelegramBadRequest:
            pass

        try:
            await callback.message.answer_photo(
                photo=item.photo,
                caption=text,
                parse_mode="html",
                reply_markup=keyboard
            )
        except TelegramBadRequest:
            try:
                await callback.message.answer(text,parse_mode="html", reply_markup=keyboard)
            except TelegramBadRequest:
                pass
    else:
        try:
            await callback.message.edit_text(text,parse_mode="html", reply_markup=keyboard)
        except TelegramBadRequest:
            pass
    await callback.answer()

@router.callback_query(BuyItemCBData.filter(), FilterUserCanBuyItem())
async def buy_item(
        callback: types.CallbackQuery,
        callback_data: BuyItemCBData,
        item_repo: ItemRepo,
        user_repo: UserRepo,
        order_repo: OrderRepo,
        bot: Bot
):
    item = await item_repo.get_item_id(callback_data.id)
    if not item:
        await callback.answer("Товар не найден", show_alert=True)
        return

    user = await user_repo.get_user_by_tg_id(callback.from_user.id)
    if not user:
        await callback.answer("Пользователь не найден", show_alert=True)
        return

    await user_repo.update_balance(callback.from_user.id, -item.price)

    order = await order_repo.create_order(
        user_id = user.id,
        item = item
    )

    await callback.message.answer(
        f"Вы купили: {item.name}\n"
        f"Списано: {round(item.price / 100, 2)} монет"
    )
    await callback.answer()

    admin_id = int(getenv("ADMIN_ID",0))
    await notify_admin(
        bot,admin_id,
        f"Новый заказ #{order.id}\n\n"
        f"{user.full_name}(@{user.username or 'Нет'})\n"
        f"{item.name}\n"
        f"{round(item.price/100,2)} монет"
    )