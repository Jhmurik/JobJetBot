from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

# 📦 Тестовая команда автосинхронизации
@router.message(Command("sync_jobs"))
async def sync_jobs(message: Message):
    # ⚙️ Здесь будет логика парсинга или API-запросов к внешним источникам
    await message.answer("🔄 Вакансии обновлены (эмуляция).")
