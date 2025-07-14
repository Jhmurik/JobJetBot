# handlers/stats.py

from aiogram import Router, F # НОВОЕ: Добавляем F
from aiogram.types import Message
from aiogram.filters import Command # НОВОЕ: Добавляем импорт Command
from utils.stats import count_drivers # Убедитесь, что этот импорт верный

router = Router()

# НОВОЕ: Обработчик для команды /stats
@router.message(Command("stats"))
async def show_stats_command(message: Message):
    # НОВОЕ: Правильный способ получить pool из приложения aiohttp
    pool = message.bot.get('__APP__').get("db")
    if not pool:
        await message.answer("❌ Ошибка: Подключение к базе данных недоступно.")
        return

    total_drivers = await count_drivers(pool)
    await message.answer(f"📊 Всего заполнено анкет: {total_drivers}")

# НОВОЕ: Обработчик для текстового сообщения "Статистика" (если используется кнопка)
@router.message(F.text.lower() == "статистика")
async def show_stats_text(message: Message):
    # Можно просто вызвать основной обработчик команды /stats
    await show_stats_command(message)
