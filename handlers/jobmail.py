from aiogram import Router
from aiogram.types import Message
from asyncpg import Pool

router = Router()

# 🔐 Только для админов
ADMIN_IDS = [787919568, 5814167740]

@router.message(lambda msg: msg.text.startswith("/jobmail"))
async def job_mailer(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return await message.answer("⛔ У вас нет доступа.")

    args = message.text.split(" ", 1)
    if len(args) < 2:
        return await message.answer("✍️ Введите текст: /jobmail Вакансия...")

    vacancy_text = args[1]

    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    sent = 0

    async with pool.acquire() as conn:
        drivers = await conn.fetch("SELECT id FROM drivers WHERE is_active = true")

        for driver in drivers:
            try:
                await message.bot.send_message(driver["id"], f"📢 Новая вакансия:\n\n{vacancy_text}")
                sent += 1
            except:
                continue

    await message.answer(f"✅ Вакансия отправлена {sent} водителям.")
