from aiogram import Router
from aiogram.types import Message
from asyncpg import Pool

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# 📢 Получение активных рекламных блоков
async def get_active_ads(pool: Pool, limit: int = 1) -> list:
    async with pool.acquire() as conn:
        return await conn.fetch("""
            SELECT title, body, button_text, button_url 
            FROM ads
            WHERE is_active = TRUE
            ORDER BY created_at DESC
            LIMIT $1
        """, limit)

# 📩 Отправка рекламы пользователю
async def send_active_ads(message: Message):
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    ads = await get_active_ads(pool)

    if not ads:
        return

    for ad in ads:
        text = f"📢 <b>{ad['title']}</b>\n\n{ad['body']}"
        if ad["button_text"] and ad["button_url"]:
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=ad["button_text"], url=ad["button_url"])]
            ])
            await message.answer(text, reply_markup=kb, parse_mode="HTML")
        else:
            await message.answer(text, parse_mode="HTML")
