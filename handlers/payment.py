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

    if not role:
        await message.answer("❌ Роль не определена. Пожалуйста, перезапустите бота через /start.")
        return

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

    try:
        # 🔗 Получаем ссылку от Cryptomus
        url = await create_payment_link(
            user_id=user_id,
            role=role,
            amount=amount,
            payment_type="premium"
        )

        # 💾 Сохраняем ожидаемый платёж
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

        # 📤 Ссылка для оплаты
        await message.answer(f"💳 Оплата подписки на сумму {amount}$\n\n"
                             f"Перейдите по ссылке для оплаты:\n{url}\n\n"
                             f"✅ Подписка активируется автоматически после оплаты.")
    except Exception as e:
        await message.answer("❌ Произошла ошибка при создании ссылки на оплату.")
        print(f"[Cryptomus] Ошибка при создании ссылки: {e}")
