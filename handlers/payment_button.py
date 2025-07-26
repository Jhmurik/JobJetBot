from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.payment import create_payment_link
from utils.i18n import t

router = Router()

# 💳 Обработка нажатия на кнопку "Купить подписку"
@router.message(F.text.in_(["💳 Купить подписку", "💳 Buy Premium", "💳 Купити Premium"]))
async def handle_buy_premium(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = "ru"
    data = await state.get_data()
    lang = data.get("language", "ru")
    role = data.get("role")

    # 🧾 Проверка роли
    if role not in ["driver", "manager"]:
        await message.answer(t(lang, "subscription_invalid_role"))
        return

    # 💰 Стоимость
    price = 3 if role == "driver" else 25

    # 🔌 Получаем доступ к пулу БД
    app = message.bot._ctx.get("application")
    pool = app["db"]

    try:
        url = await create_payment_link(pool=pool, user_id=user_id, role=role, amount=price)
        await message.answer(
            t(lang, "payment_link", amount=price, url=url),
            disable_web_page_preview=False
        )
    except Exception as e:
        print(f"[Payment Error] {e}")
        await message.answer(t(lang, "payment_error"))
