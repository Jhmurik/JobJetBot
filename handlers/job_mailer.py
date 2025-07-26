from aiogram import Router
from aiogram.types import Message
from asyncpg import Pool

router = Router()

# 🔔 Команда запуска рассылки (в будущем — автоматическая cron-задача)
@router.message(lambda m: m.text == "📨 Рассылка вакансий")
async def send_job_mailings(message: Message):
    admin_ids = [5814167740, 787919568]  # 👑 ID админов
    if message.from_user.id not in admin_ids:
        await message.answer("⛔ Только администраторы могут запускать рассылку.")
        return

    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        # Получаем активных водителей с Premium и регионами
        drivers = await conn.fetch("""
            SELECT id, regions FROM drivers
            WHERE is_active = TRUE AND id IN (
                SELECT user_id FROM payments 
                WHERE role = 'driver' AND payment_type = 'premium'
                  AND created_at > (CURRENT_DATE - INTERVAL '30 days')
            )
        """)

        # Получаем новые вакансии
        vacancies = await conn.fetch("""
            SELECT id, title, region, salary, truck_type, contacts 
            FROM vacancies 
            WHERE is_published = TRUE 
            ORDER BY created_at DESC 
            LIMIT 20
        """)

    if not vacancies:
        await message.answer("❌ Нет доступных вакансий.")
        return

    count = 0
    for driver in drivers:
        user_id = driver["id"]
        preferred_regions = driver["regions"] or []
        matched = [v for v in vacancies if v["region"] in preferred_regions]

        if matched:
            text = "📬 <b>Подходящие вакансии для вас:</b>\n\n"
            for v in matched[:5]:
                text += (
                    f"🔹 <b>{v['title']}</b>\n"
                    f"📍 Регион: {v['region']}\n"
                    f"💰 Зарплата: {v['salary']}\n"
                    f"🚛 Транспорт: {v['truck_type']}\n"
                    f"📱 Контакты: {v['contacts']}\n\n"
                )
            try:
                await message.bot.send_message(chat_id=user_id, text=text, parse_mode="HTML")
                count += 1
            except Exception as e:
                print(f"❌ Ошибка отправки {user_id}: {e}")

    await message.answer(f"✅ Рассылка завершена. Отправлено {count} водителям.")
