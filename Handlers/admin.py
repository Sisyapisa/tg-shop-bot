from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import keyboard

from filters.is_admin import IsAdmin
from keyboards.admin import admin_menu,back_to_admin,admin_items_menu
from repositories.order import OrderRepo
from repositories.user import UserRepo
from repositories.item import ItemRepo
from repositories.categories import CategoryRepo
from states.admin import AddItemsState,DeleteItemsState

router = Router()

router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())

@router.message(F.text == "/admin")
async def admin_panel(message: types.Message):
    await message.answer(
        "Админ-панель\nВыберите раздел:",
        reply_markup = admin_menu()
    )

@router.callback_query(F.data == "admin:menu")
async def admin_menu_kb(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Админ-Панель\n\nВыберите раздел:",
        reply_markup = admin_menu()
    )
    await callback.answer()

@router.callback_query(F.data == "admin:stats")
async def admin_stats(
        callback: types.CallbackQuery,
        order_repo: OrderRepo,
        user_repo: UserRepo
    ):
    orders_count,total_sum = await order_repo.get_stats()
    user_count = await user_repo.get_user_count()

    await callback.message.edit_text(
        f"Статистикa\n\n"
        f"Юзеров: {user_count}\n"
        f"Заказов: {orders_count}\n"
        f"Общая сумма: {round(total_sum / 100, 2)} монет",
        reply_markup=back_to_admin()
    )
    await callback.answer()

@router.callback_query(F.data == "admin:orders")
async def admin_orders(
        callback: types.CallbackQuery,
        order_repo: OrderRepo
):
    orders = await order_repo.get_all_orders(limit=10)

    if not orders:
        await callback.message.edit_text(
            "Заказов пока нет",
            reply_markup = back_to_admin()
        )
        await callback.answer()
        return

    text = ("Последние заказы\n\n")
    for order in orders:
        text += f"#{order.id} -- {order.status}\n"
        text += f"{round(order.total / 100, 2)} монет \n"
        text += f"{order.created_at.strftime('%d/%m/%Y %H:%M')}\n"
        for item in order.items:
            text += f" • {item.item_name} × {item.quantity}\n"
        text +="\n"

    await callback.message.edit_text(
        text,
        reply_markup = back_to_admin()
    )
    await callback.answer()

@router.callback_query(F.data == "admin:users")
async def admin_users(
        callback: types.CallbackQuery,
        user_repo: UserRepo
):
    users = await user_repo.get_all_users(limit=10)

    if not users:
        await callback.message.edit_text(
            "Юзеров пока нет",
            reply_markup = back_to_admin()
        )
        await callback.answer()
        return

    text = "Последние юзеры\n\n"
    for user in users:
        text += f"{user.full_name} \n"
        text += f"@{user.username or 'Нет'}\n"
        text += f"{user.view_balance} монет\n"

    await callback.message.edit_text(
        text,
        reply_markup = back_to_admin()
    )
    await callback.answer()

@router.callback_query(F.data == "admin:items")
async def admin_items(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Управление товарами\n Выберите действие:",
        reply_markup = admin_items_menu()
    )
    await callback.answer()

@router.callback_query(F.data == "admin:add_item")
async def admin_add_items(callback: types.CallbackQuery,state: FSMContext):
    await state.set_state(AddItemsState.INPUT_NAME)
    await callback.message.edit_text("Введите название товара:")
    await callback.answer()

@router.message(AddItemsState.INPUT_NAME)
async def admin_add_items(message: types.Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer("Введите описание:")
    await state.set_state(AddItemsState.INPUT_DESCRIPTION)

@router.message(AddItemsState.INPUT_DESCRIPTION)
async def add_item_description(message: types.Message, state: FSMContext):
    await state.update_data(description = message.text)
    await message.answer("Введите цену в монетах (например 100):")
    await state.set_state(AddItemsState.INPUT_PRICE)

@router.message(AddItemsState.INPUT_PRICE)
async def add_item_price(message: types.Message, state: FSMContext, category_repo: CategoryRepo):
    if not message.text.isdigit():
        await message.answer("Введите число:")
        return
    await state.update_data(price = int(message.text) * 100 )

    categories = await category_repo.get_list()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(text = c.name, callback_data=f"admin:add_cat:{c.id}")]
            for c in categories
        ]
    )
    await message.answer("Выберите категорию:", reply_markup = keyboard)
    await state.set_state(AddItemsState.INPUT_CATEGORY)

@router.callback_query(AddItemsState.INPUT_CATEGORY, F.data.startswith("admin:add_cat:"))
async def add_item_category(callback: types.CallbackQuery, state: FSMContext):
    cat_id = int (callback.data.split(":")[-1])
    await state.update_data(category = cat_id)
    await callback.message.edit_text(
        "Отправьте фото товара (или напишите нет)"
    )
    await state.set_state(AddItemsState.INPUT_PHOTO)
    await callback.answer()

@router.message(AddItemsState.INPUT_PHOTO, F.text.lower() == "нет")
async def add_item_no_photo(message: types.Message, state: FSMContext, item_repo: ItemRepo,category_repo: CategoryRepo):
    await state.update_data(photo = None)
    await save_item(message,state, item_repo, category_repo)

@router.message(AddItemsState.INPUT_PHOTO,F.photo)
async def add_item_photo(message: types.Message, state: FSMContext, item_repo: ItemRepo,category_repo: CategoryRepo):
    file_id = message.photo[-1].file_id
    await state.update_data(photo = file_id)
    await save_item(message,state, item_repo, category_repo)

async def save_item(message: types.Message, state: FSMContext, item_repo: ItemRepo,category_repo: CategoryRepo):
    data = await state.get_data()
    category = await category_repo.get_by_id(data['category'])

    await item_repo.create_item(
        name = data['name'],
        description = data['description'],
        price = data['price'],
        photo = data.get('photo'),
        category_id=data['category']
    )
    await message.answer(
        f"Товар добавлен!\n"
        f"{data['name']}\n"
        f"{category.name}\n"
        f"{round(data['price'], 2)}\n"
    )
    await state.clear()

@router.callback_query(F.data == "admin:delete_item")
async def delete_item(callback: types.CallbackQuery, category_repo: CategoryRepo):
    categoties = await category_repo.get_list()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(
                text = c.name,
                callback_data=f"admin:del_cat:{c.id}"
            )]
            for c in categoties
        ]
    )
    await callback.message.edit_text(
        "Выберите категорию:",
        reply_markup = keyboard
    )
    await callback.answer()

@router.callback_query(F.data.startswith("admin:del_cat:"))
async def delete_item_list(callback: types.CallbackQuery, item_repo: ItemRepo):
    cat_id = int(callback.data.split(":")[-1])
    items = await item_repo.get_item(cat_id)

    if not items:
        await callback.message.edit_text(
            "В этой категории нет товаров.",
            reply_markup = admin_items_menu()
        )
        await callback.answer()
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton( text= f"{i.name}" , callback_data=f"admin:del_item:{i.id}")]
            for i in items
        ]
    )
    await callback.message.edit_text("Выберете товар для удаления:",reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("admin:del_item:"))
async def delete_item_confirm(callback: types.CallbackQuery, item_repo: ItemRepo):
    item_id = int(callback.data.split(":")[-1])
    item = await item_repo.get_item_id(item_id)
    if not item:
        await callback.answer("Товар не найден", show_alert = True)
        return

    await item_repo.delete_item(item_id)
    await callback.message.edit_text(
        f"Товар {item.name} удален.",
        reply_markup = admin_items_menu()
    )
    await callback.answer()