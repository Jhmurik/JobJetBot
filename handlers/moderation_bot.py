from aiogram import Router, F
from aiogram.types import Message
from asyncpg import Pool

router = Router()

# 🔐 Только для админов
ADMIN_IDS = [787919568, 5814167740]

# 📋 Запрос на модерацию
@router.message(F.text.startswith("/moderate"))
async def moderate_driver(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return await message.answer("⛔ У вас нет доступа к модерации.")

    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        drivers = await conn.fetch("""
            SELECT * FROM drivers 
            WHERE is_approved = false
            ORDER BY created_at ASC
            LIMIT 5
        """)
        if not drivers:
            return await message.answer("✅ Все анкеты уже проверены.")

        for driver in drivers:
            text = (
                f"👤 <b>Анкета водителя</b>\n"
                f"🆔 ID: <code>{driver['id']}</code>\n"
                f"👨‍🔧 Имя: {driver['full_name']}\n"
                f"🚚 ТС: {driver.get('truck_type') or '—'}\n"
                f"📍 Опыт: {driver.get('experience') or '—'}\n"
                f"🌍 Регионы: {', '.join(driver['regions'] or []) or '—'}\n\n"
                f"✅ /approve {driver['id']}\n"
                f"❌ /reject {driver['id']}"
            )
            await message.answer(text, parse_mode="HTML")

# ✅ Подтверждение анкеты
@router.message(F.text.startswith("/approve"))
async def approve_driver(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        parts = message.text.split(" ")
        if len(parts) != 2:
            raise ValueError("Неверный формат")

        driver_id = int(parts[1])
        app = message.bot._ctx.get("application")
        pool: Pool = app["db"]

        async with pool.acquire() as conn:
            await conn.execute("UPDATE drivers SET is_approved = true, is_active = true WHERE id = $1", driver_id)

        await message.answer(f"✅ Анкета <code>{driver_id}</code> одобрена.", parse_mode="HTML")
        await message.bot.send_message(driver_id, "✅ Ваша анкета прошла модерацию и теперь видна работодателям!")
    except Exception as e:
        await message.answer("⚠️ Ошибка. Используйте: /approve <id>")

# ❌ Отклонение анкеты
@router.message(F.text.startswith("/reject"))
async def reject_driver(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        parts = message.text.split(" ")
        if len(parts) != 2:
            raise ValueError("Неверный формат")

        driver_id = int(parts[1])
        app = message.bot._ctx.get("application")
        pool: Pool = app["db"]

        async with pool.acquire() as conn:
            await conn.execute("DELETE FROM drivers WHERE id = $1", driver_id)

        await message.answer(f"❌ Анкета <code>{driver_id}</code> удалена.", parse_mode="HTML")
        await message.bot.send_message(driver_id, "🚫 Ваша анкета была отклонена. Проверьте данные и создайте заново.")
    except Exception:
        await message.answer("⚠️ Ошибка. Используйте: /reject <id>")
