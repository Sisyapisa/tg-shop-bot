from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from keyboards import profile as profile_kb
from repositories.user import UserRepo
from states.profile import UserDepositState
from repositories.order import OrderRepo

router = Router()

@router.message(F.text == "Профиль")
async def user_profile_info(message: types.Message, user_repo: UserRepo):
    user = await user_repo.get_user_by_tg_id(message.from_user.id)

    if not user:
        await message.answer("Пользователь не найден в базе данных.")
        return

    username_text = f"Username: {user.username or 'Пусто'}\n"

    await message.answer(
        f"<b>{message.from_user.full_name}</b>\n\n"
        f"{username_text}"
        f"ID: <code>{user.tg_id}</code>\n"
        f"Ваш баланс: {user.view_balance} монет",
        parse_mode=ParseMode.HTML,
        reply_markup=profile_kb.profile_menu()
    )

@router.callback_query(F.data == "deposit")
async def user_deposit_action(callback_query : types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.edit_text("Введите сумму пополнения:", reply_markup=profile_kb.cancel_deposit_action())
    await state.set_state(UserDepositState.INPUT_AMOUNT)

@router.callback_query(StateFilter(UserDepositState), F.data == "cancel_deposit")
async def user_deposit_action_cancel(callback_query: types.CallbackQuery, state: FSMContext, user_repo: UserRepo):
    await state.clear()
    await callback_query.answer()

    user = await user_repo.get_user_by_tg_id(callback_query.from_user.id)

    if not user:
        await callback_query.answer("Пользователь не найден в базе данных.")
        return

    username_text = f"Username: {user.username or 'Пусто'}\n"

    await callback_query.message.edit_text(
        f"<b>{callback_query.from_user.full_name}</b>\n\n"
        f"{username_text}"
        f"ID: <code>{user.tg_id}</code>\n"
        f"Ваш баланс: {user.view_balance} монет",
        parse_mode=ParseMode.HTML,
        reply_markup=profile_kb.profile_menu()
    )

@router.message(UserDepositState.INPUT_AMOUNT)
async def user_deposit_amount(message:types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите целое число")
        return
    amount = int(message.text)
    await state.set_data({"amount": amount})
    await message.answer(
        f"Подтверждаете ли вы пополнение баланса на {amount} монет?",
        reply_markup=profile_kb.apply_deposit_action()
    )
    await state.set_state(UserDepositState.APPLY_DEPOSIT)

@router.callback_query(UserDepositState.APPLY_DEPOSIT, F.data == "apply_deposit")
async def apply_user_deposit(callback_query: types.CallbackQuery, state: FSMContext, user_repo: UserRepo):
    state_data = await state.get_data()
    deposit_amount = state_data.get("amount")

    await user_repo.update_balance(callback_query.from_user.id, deposit_amount * 100)
    await callback_query.message.edit_text(
        f"Баланс успешно пополнен на {deposit_amount} монет",
        reply_markup=profile_kb.cancel_deposit_action("Профиль")
    )

    await callback_query.answer()

@router.callback_query(F.data == "my_orders")
async def my_orders(
        callback: types.CallbackQuery,
        user_repo: UserRepo,
        order_repo: OrderRepo,
):
    user = await user_repo.get_user_by_tg_id(callback.from_user.id)
    if not user:
        await callback.answer("Пользователь не найден", show_alert=True)
        return

    orders = await order_repo.get_user_orders(user.id)
    if not orders:
        await callback.message.edit_text("У вас пока нет заказов!",reply_markup = profile_kb.back_to_profile())
        await callback.answer()
        return

    text = "Ваши заказы:\n\n"
    for order in orders:
        text += f"Заказ #{order.id} - {order.status}\n"
        text += f"Сумма {round(order.total / 100)} монет\n"
        text += f"{order.created_at.strftime('%d/%m/%Y %H:%M')}\n"
        for item in order.items:
            text += f"• {item.item_name} × {item.quantity}\n"
        text += "\n"

    await callback.message.edit_text(
        text,
        reply_markup=profile_kb.back_to_profile()
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_profile")
async def back_to_profile(callback: types.CallbackQuery,
                          user_repo: UserRepo
                          ):
    user = await user_repo.get_user_by_tg_id(callback.from_user.id)
    if not user:
        await callback.answer("Пользователь не найден", show_alert=True)
        return

    username_text = f"Username: {user.username or 'Пусто'}\n"

    await callback.message.edit_text(
        f"{callback.from_user.full_name}\n\n"
        f"{username_text}"
        f"ID: <code>{user.tg_id}</code>\n"
        f"Ваш баланс: {user.view_balance} монет",
        parse_mode=ParseMode.HTML,
        reply_markup=profile_kb.profile_menu()
    )
    await callback.answer()