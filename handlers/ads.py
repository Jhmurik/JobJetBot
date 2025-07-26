from aiogram import Router
from aiogram.types import Message
from asyncpg import Pool

router = Router()

# 📢 Отображение активной рекламы при /start или входе
async def get_active_ads(pool: Pool) -> list:
    async with pool.acquire() as conn:
        ads = await conn.fetch("""
            SELECT title, body, button_text, button_url 
            FROM ads
            WHERE is_active = TRUE
            ORDER BY created_at DESC
            LIMIT 1
        """)
        return ads


async def send_active_ads(message: Message):
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]
    ads = await get_active_ads(pool)

    for ad in ads:
        text = f"📢 <b>{ad['title']}</b>\n\n{ad['body']}"
        if ad["button_text"] and ad["button_url"]:
            from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=ad["button_text"], url=ad["button_url"])]
            ])
            await message.answer(text, reply_markup=kb, parse_mode="HTML")
        else:
            await message.answer(text, parse_mode="HTML")
