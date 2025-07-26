from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from asyncpg import Pool
from utils.payment import create_payment_link
from db import save_payment
from utils.i18n import t  # ✅ мультиязычность

router = Router()

# 💳 Кнопка "Купить подписку"
@router.message(F.text == "💳 Купить подписку")
async def handle_buy_subscription(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    role = data.get("role")
    lang = data.get("language", "ru")

    if not role:
        await message.answer(t(lang, "role_undefined"))
        return

    # 💰 Цена и описание
    if role == "driver":
        amount = 3.0
        description = t(lang, "subscription_driver")
    elif role == "manager":
        amount = 25.0
        description = t(lang, "subscription_manager")
    else:
        await message.answer(t(lang, "subscription_invalid_role"))
        return

    try:
        # 🔗 Ссылка Cryptomus
        url = await create_payment_link(
            user_id=user_id,
            role=role,
            amount=amount,
            payment_type="premium"
        )

        # 💾 Сохранение платежа
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

        # 📤 Сообщение пользователю
        await message.answer(
            t(lang, "payment_link").format(amount=amount, url=url),
            parse_mode="HTML"
        )

    except Exception as e:
        await message.answer(t(lang, "payment_error"))
        print(f"[Cryptomus] Ошибка при создании ссылки: {e}")
