from aiogram import Router
from aiogram.types import Message
from asyncpg import Pool
from datetime import datetime, timedelta

router = Router()

# 🔘 Команда только для админа (в будущем будет запускаться по расписанию)
@router.message(lambda m: m.text == "/jobmailer")
async def send_new_vacancies(message: Message):
    if message.from_user.id not in [787919568, 5814167740]:  # ✅ Установленные админ ID
        return await message.answer("⛔ Доступ запрещен.")

    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        # 🕒 Только новые вакансии за последние сутки
        since = datetime.utcnow() - timedelta(days=1)
        new_vacancies = await conn.fetch("""
            SELECT v.title, v.truck_type, v.salary, v.region, v.contacts, c.name AS company_name
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE v.created_at >= $1 AND v.is_published = TRUE
        """, since)

        if not new_vacancies:
            return await message.answer("📭 Новых вакансий нет.")

        drivers = await conn.fetch("SELECT id FROM drivers WHERE is_active = TRUE")

        text = f"📢 Новые вакансии за сутки:\n\n"
        for vac in new_vacancies[:5]:  # Максимум 5 вакансий
            text += (
                f"📌 <b>{vac['title']}</b>\n"
                f"🏢 {vac['company_name']}\n"
                f"🚛 {vac['truck_type']}, 💰 {vac['salary']}, 🌍 {vac['region']}\n"
                f"📱 {vac['contacts']}\n\n"
            )

        for driver in drivers:
            try:
                await message.bot.send_message(driver["id"], text, parse_mode="HTML")
            except Exception:
                continue  # Ошибки игнорируются

        await message.answer(f"✅ Рассылка завершена ({len(drivers)} получателей)")
