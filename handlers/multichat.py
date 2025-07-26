from aiogram import Router, F
from aiogram.types import Message
from asyncpg import Pool

router = Router()

# 🔐 Только для менеджеров с Premium
@router.message(F.text.startswith("/chat "))
async def manager_chat(message: Message):
    parts = message.text.strip().split(" ", 2)
    if len(parts) < 3:
        return await message.answer("❌ Формат команды: /chat <driver_id> <сообщение>")

    _, driver_id_str, content = parts

    try:
        driver_id = int(driver_id_str)
    except ValueError:
        return await message.answer("⚠️ Неверный формат ID водителя.")

    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        # Проверка менеджера
        is_premium = await conn.fetchval("""
            SELECT TRUE FROM payments 
            WHERE user_id = $1 AND role = 'manager' AND payment_type = 'premium'
            ORDER BY created_at DESC LIMIT 1
        """, message.from_user.id)

        if not is_premium:
            return await message.answer("⛔ Чат доступен только менеджерам с Premium-подпиской.")

        driver_exists = await conn.fetchval("SELECT 1 FROM drivers WHERE id = $1", driver_id)
        if not driver_exists:
            return await message.answer("❌ Водитель с таким ID не найден.")

    try:
        await message.bot.send_message(
            chat_id=driver_id,
            text=f"💬 Сообщение от менеджера:\n\n{content}"
        )
        await message.answer("✅ Сообщение отправлено.")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка при отправке: {e}")
