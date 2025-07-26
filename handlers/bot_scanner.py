from aiogram import Router, F
from aiogram.types import Message
from asyncpg import Pool

router = Router()

# 🔍 Команда запуска сканирования (в будущем — планировщик)
@router.message(F.text == "🔍 Сканировать группы")
async def start_scan(message: Message):
    # Ограничим по ID (временно)
    admin_ids = [5814167740, 787919568]  # 👉 Твои ID
    if message.from_user.id not in admin_ids:
        await message.answer("⛔ Только администраторы могут запускать сканер.")
        return

    # Заглушка под сканер (будет замена на Telethon сканер)
    await message.answer("📡 Сканирование Telegram-групп пока в разработке.\n"
                         "Позже здесь будет автоматический сбор свежих вакансий.")

    # Пример сохранения вакансии вручную:
    """
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO vacancies (id, title, truck_type, salary, region, requirements, contacts, company_id, manager_id, is_published)"
            "VALUES (gen_random_uuid(), $1, $2, $3, $4, $5, $6, $7, $8, TRUE)",
            "Водитель по ЕС", "Тент", "2800€", "EU", "Опыт 1 год", "📞 +37060000000", some_company_id, some_manager_id
        )
    """
