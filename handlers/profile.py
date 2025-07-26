📁 handlers/profile.py

from aiogram import Router, F from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton from asyncpg import Pool

router = Router()

@router.message(F.text == "👤 Личный кабинет") async def show_profile(message: Message): user_id = message.from_user.id app = message.bot._ctx.get("application") pool: Pool = app["db"]

async with pool.acquire() as conn:
    driver = await conn.fetchrow("SELECT * FROM drivers WHERE id = $1", user_id)
    if driver:
        premium = await conn.fetchval("SELECT TRUE FROM payments WHERE user_id = $1 AND role = 'driver' AND payment_type = 'premium' ORDER BY created_at DESC LIMIT 1", user_id)
        text = (
            f"👤 <b>Ваш профиль (Водитель)</b>\n"
            f"👨‍🚒 Имя: {driver['full_name']}\n"
            f"🚗 Тип ТС: {driver['truck_type']}\n"
            f"⏳ Опыт: {driver['experience']}\n"
            f"🌍 Регионы: {', '.join(driver['regions'] or [])}\n"
            f"🌐 Подписка: {'активна' if premium else 'нет'}"
        )
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📄 Моя анкета")],
                [KeyboardButton(text="
