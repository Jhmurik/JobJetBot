from aiogram import Router, F
from aiogram.types import Message
from asyncpg import Pool

router = Router()

# 🔐 Только для админов
ADMIN_IDS = [787919568, 5814167740]  # 👈 Добавь нужные ID

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
            return await message.answer("✅ Все анкеты проверены.")

        for driver in drivers:
            text = (
                f"👤 <b>Анкета водителя</b>\n"
                f"🆔 ID: <code>{driver['id']}</code>\n"
                f"👨‍🔧 Имя: {driver['full_name']}\n"
                f"🚚 ТС: {driver.get('truck_type') or '—'}\n"
                f"📍 Опыт: {driver.get('experience') or '—'}\n"
                f"🌍 Регионы: {', '.join(driver['regions'] or []) or '—'}\n\n"
                f"Для подтверждения отправьте:\n"
                f"<code>/approve {driver['id']}</code>\n"
                f"Для отклонения:\n"
                f"<code>/reject {driver['id']}</code>"
            )
            await message.answer(text, parse_mode="HTML")

@router.message(F.text.startswith("/approve"))
async def approve_driver(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        driver_id = int(message.text.split(" ")[1])
        app = message.bot._ctx.get("application")
        pool: Pool = app["db"]
        async with pool.acquire() as conn:
            await conn.execute("UPDATE drivers SET is_approved = true WHERE id = $1", driver_id)
        await message.answer(f"✅ Анкета {driver_id} подтверждена.")
    except Exception:
        await message.answer("⚠️ Неверная команда.")

@router.message(F.text.startswith("/reject"))
async def reject_driver(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        driver_id = int(message.text.split(" ")[1])
        app = message.bot._ctx.get("application")
        pool: Pool = app["db"]
        async with pool.acquire() as conn:
            await conn.execute("DELETE FROM drivers WHERE id = $1", driver_id)
        await message.answer(f"❌ Анкета {driver_id} удалена.")
    except Exception:
        await message.answer("⚠️ Неверная команда.")
