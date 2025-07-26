from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from asyncpg import Pool

router = Router()

# 💼 Команда "Партнёрская программа"
@router.message(F.text.lower() == "🤝 партнёрская программа")
async def show_partner_info(message: Message):
    user_id = message.from_user.id
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        # Проверка, есть ли уже запись
        ref_code = await conn.fetchval("SELECT code FROM referrals WHERE user_id = $1", user_id)

        if not ref_code:
            # Генерация кода: REF_12345678
            ref_code = f"REF_{user_id}"
            await conn.execute("INSERT INTO referrals (user_id, code) VALUES ($1, $2)", user_id, ref_code)

        link = f"https://t.me/JobJetStarBot?start={ref_code}"

    text = (
        f"🤝 <b>Партнёрская программа JobJet AI</b>\n\n"
        f"🔗 Ваша реферальная ссылка:\n<code>{link}</code>\n\n"
        f"💰 Вы получаете бонусы за каждого пользователя, который оформит подписку по вашей ссылке.\n"
        f"👥 Приглашайте водителей и компании и зарабатывайте вместе с нами!"
    )

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📊 Статистика")]],
        resize_keyboard=True
    )

    await message.answer(text, reply_markup=kb, parse_mode="HTML")
