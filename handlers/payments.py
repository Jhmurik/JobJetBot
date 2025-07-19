from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from db import save_payment_log
from utils.payment import create_payment_link  # функция уже реализована
from asyncpg import Pool

router = Router()

@router.message(F.text == "💳 Купить подписку")
async def handle_buy_subscription(message: Message, state: FSMContext):
    user_id = message.from_user.id
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    data = await state.get_data()
    role = data.get("role", "driver")

    # Установим цену
    price_usd = 3.00 if role == "driver" else 25.00
    payment_type = "premium"

    # Генерация ссылки
    try:
        payment_url = await create_payment_link(user_id, role, price_usd, payment_type)
    except Exception as e:
        await message.answer("❌ Ошибка при создании ссылки на оплату. Попробуйте позже.")
        return

    # Сохраняем в лог (по желанию)
    await save_payment_log(pool, user_id, role, price_usd, "USDT", "cryptomus", payment_type)

    await message.answer(
        f"💳 Для оплаты подписки перейдите по ссылке:\n\n{payment_url}\n\n"
        f"💰 Сумма: {price_usd}$ в USDT (TRC20)\n"
        "⏳ Ссылка активна 15 минут. После оплаты вернитесь в бот."
    )
