from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from asyncpg import Pool

router = Router()

@router.message(F.text == "👤 Личный кабинет")
async def show_manager_profile(message: Message):
    user_id = message.from_user.id
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        manager = await conn.fetchrow("""
            SELECT full_name, position, company_name, regions, is_active 
            FROM managers WHERE user_id = $1
        """, user_id)

        if not manager:
            await message.answer("❌ Вы не зарегистрированы как менеджер.")
            return

        text = (
            f"👤 <b>Ваш профиль (Менеджер)</b>\n"
            f"👨‍💼 Имя: {manager['full_name'] or '—'}\n"
            f"📌 Должность: {manager['position'] or '—'}\n"
            f"🏢 Компания: {manager['company_name'] or '—'}\n"
            f"🌍 Регионы: {', '.join(manager['regions'] or [])}\n"
            f"🔐 Подписка: {'активна' if manager['is_active'] else 'неактивна'}"
        )

        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📄 Мои вакансии")],
                [KeyboardButton(text="➕ Опубликовать вакансию")],
                [KeyboardButton(text="🎁 Бонусы и скидки")],
                [KeyboardButton(text="💳 Подключить Premium")]
            ],
            resize_keyboard=True
        )

        await message.answer(text, reply_markup=kb, parse_mode="HTML")
