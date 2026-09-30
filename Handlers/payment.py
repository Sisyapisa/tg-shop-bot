from aiogram import types, F, Router
from aiogram.types import LabeledPrice, PreCheckoutQuery
from pathlib import Path
from dotenv import dotenv_values

from repositories.user import UserRepo

env_path = Path(__file__).parent.parent / ".env"
config = dotenv_values(env_path)

PROVIDER_TOKEN = config.get("PROVIDER_TOKEN")

router = Router()

@router.callback_query(F.data.startswith("pay:"))
async def pay_invoice(callback:types.CallbackQuery):
    if not PROVIDER_TOKEN:
        await callback.answer("Оплата временно недоступна", show_alert=True)
        return

    amount = int(callback.data.split(":")[-1])

    await callback.message.answer_invoice(
        title="Пополнение баланса",
        description=f"Пополнение на {amount} монет",
        payload=f"deposit:{amount}",
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        prices=[
            LabeledPrice(label="Пополнение", amount=amount * 100),
        ],
        start_parameter="deposit",
    )
    await callback.answer()

@router.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok = True)

@router.message(F.successful_payment)
async def successful_payment(message: types.Message, user_repo: UserRepo):
    payment = message.successful_payment
    payload = payment.invoice_payload

    try:
        amount = int(payload.split(":")[-1])
    except(ValueError, IndexError):
        await message.answer("Ошибка обработки платежа, обратитесь в поддержку")
        return

    await user_repo.update_balance(message.from_user.id,amount * 100)

    await message.answer(
        f"Оплата прошла успешно!\n"
        f"Баланс пополнен на {amount} монет\n\n"
        f"Спасибо за покупку!"
    )