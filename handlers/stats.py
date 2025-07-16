# handlers/stats.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from utils.stats import count_drivers

router = Router()

# ✅ Обработчик команды /stats
@router.message(Command("stats"))
async def show_stats_command(message: Message):
    # Получаем aiohttp-приложение из контекста
    app = message.bot._ctx.get("application")
    if not app or "db" not in app:
        await message.answer("❌ Ошибка: Подключение к базе данных недоступно.")
        return

    pool = app["db"]
    total_drivers = await count_drivers(pool)
    await message.answer(f"📊 Всего заполнено анкет: {total_drivers}")

# ✅ Обработчик текста "Статистика" (при нажатии кнопки)
@router.message(F.text.lower() == "статистика")
async def show_stats_text(message: Message):
    await show_stats_command(message)
