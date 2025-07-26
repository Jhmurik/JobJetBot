from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from asyncpg import Pool

router = Router()

# 👤 Личный кабинет водителя
@router.message(F.text == "👤 Личный кабинет")
async def show_profile(message: Message):
    user_id = message.from_user.id
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        driver = await conn.fetchrow("SELECT * FROM drivers WHERE id = $1", user_id)
        if driver:
            premium = await conn.fetchval("""
                SELECT TRUE FROM payments
                WHERE user_id = $1 AND role = 'driver' AND payment_type = 'premium'
                ORDER BY created_at DESC LIMIT 1
            """, user_id)

            text = (
                f"👤 <b>Ваш профиль (Водитель)</b>\n"
                f"👨‍🚒 Имя: {driver['full_name']}\n"
                f"🚗 Тип ТС: {driver['truck_type'] or '—'}\n"
                f"⏳ Опыт: {driver['experience'] or '—'}\n"
                f"🌍 Регионы: {', '.join(driver['regions'] or [])}\n"
                f"🌐 Подписка: {'активна ✅' if premium else 'неактивна ❌'}"
            )

            kb = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="🧾 Моя анкета"), KeyboardButton(text="💳 Подписка")],
                    [KeyboardButton(text="🎁 Бонусы и скидки")],
                    [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="🌐 Сменить язык")]
                ],
                resize_keyboard=True
            )

            await message.answer(text, reply_markup=kb, parse_mode="HTML")
        else:
            await message.answer("❌ Профиль не найден. Пожалуйста, заполните анкету.")

# 🎁 Полезные бонусы и ссылки
@router.message(F.text == "🎁 Бонусы и скидки")
async def show_bonuses(message: Message):
    bonuses = [
        ("WhiteBird", "https://whitebird.io/?refid=jEYdB", "Переводы, обмен, крипта — быстро и выгодно"),
        ("PaySend", "https://paysend.com/referral/05ql7b", "Мгновенные переводы с карты на карту по всему миру"),
        ("OKX", "https://okx.com/join/72027985", "Надёжная криптобиржа с бонусами за регистрацию"),
        ("Cryptomus", "https://app.cryptomus.com/signup?ref=wxkylP", "Платёжная платформа для крипты и бизнеса")
    ]

    buttons = [
        [InlineKeyboardButton(text=f"{name} →", url=url)]
        for name, url, desc in bonuses
    ]

    await message.answer(
        "🎁 <b>Полезные сервисы с бонусами:</b>\n\n" + "\n".join(
            [f"• <b>{name}</b>: {desc}" for name, url, desc in bonuses]
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )
