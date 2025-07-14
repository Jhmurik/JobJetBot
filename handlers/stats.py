# handlers/stats.py

from aiogram import Router
from aiogram.types import Message
from utils.stats import count_drivers

router = Router()

@router.message(lambda msg: msg.text.lower() in ["/статистика", "статистика"])
async def show_stats(message: Message):
    pool = message.bot.get("db")
    if not pool:
        await message.answer("❌ Нет подключения к базе данных.")
        return

    total_drivers = await count_drivers(pool)
    await message.answer(f"📊 Всего заполнено анкет: {total_drivers}")
