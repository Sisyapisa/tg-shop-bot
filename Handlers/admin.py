from aiogram import types, F, Router

from filters.is_admin import IsAdmin
from keyboards.admin import admin_menu,back_to_admin
from repositories.order import OrderRepo
from repositories.user import UserRepo

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