from aiogram import Router, F from aiogram.types import Message from asyncpg import Pool

router = Router()

📩 Показывает реферальную информацию пользователя

@router.message(F.text.lower().in_(["рефералы", "реферальная программа", "🔗 рефералы"])) async def show_referral_info(message: Message): user_id = message.from_user.id app = message.bot._ctx.get("application") pool: Pool = app["db"]

async with pool.acquire() as conn:
    # Определим роль пользователя
    driver = await conn.fetchrow("SELECT * FROM drivers WHERE id = $1", user_id)
    manager = await conn.fetchrow("SELECT * FROM managers WHERE user_id = $1", user_id)

    if driver:
        role = "driver"
    elif manager:
        role = "manager"
    else:
        await message.answer("❌ Вы пока не зарегистрированы.")
        return

    # Подсчёт приглашённых
    count = await conn.fetchval("""
        SELECT COUNT(*) FROM referrals
        WHERE referrer_id = $1 AND role = $2 AND premium = TRUE
    """, user_id, role)

    # Генерация реферальной ссылки
    ref_link = f"https://t.me/{(await message.bot.me()).username}?start=ref_{user_id}_{role}"

    await message.answer(
        f"🔗 Ваша реферальная ссылка:

<code>{ref_link}</code>

" f"👥 Приглашено пользователей с Premium: <b>{count}</b>", parse_mode="HTML" )

