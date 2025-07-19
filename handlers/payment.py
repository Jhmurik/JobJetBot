from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from asyncpg import Pool
from utils.payment import create_payment_link
from db import save_payment

router = Router()

# 💳 Кнопка "Купить подписку"
@router.message(F.text == "💳 Купить подписку")
async def handle_buy_subscription(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    role = data.get("role")

    # 💰 Цена подписки
    if role == "driver":
        amount = 3.0
        description = "Подписка водителя"
    elif role == "manager":
        amount = 25.0
        description = "Подписка менеджера"
    else:
        await message.answer("❌ Подписка доступна только для водителей и менеджеров.")
        return

    # 🔗 Получаем ссылку от Cryptomus
    url = await create_payment_link(user_id=user_id, role=role, amount=amount, payment_type="premium")

    # 💾 Сохраняем ожидаемый платёж (если нужно логировать)
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]
    await save_payment(pool, {
        "user_id": user_id,
        "role": role,
        "amount": amount,
        "currency": "USDT",
        "payment_method": "cryptomus",
        "payment_type": "premium",
        "description": description
    })

    await message.answer(f"💳 Оплата подписки: {amount}$\n\nПерейдите по ссылке для оплаты:\n{url}")
