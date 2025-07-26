from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from asyncpg import Pool

router = Router()

@router.message(F.text == "🏢 Моя компания")
async def show_company_profile(message: Message):
    user_id = message.from_user.id
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        owner = await conn.fetchrow("""
            SELECT id, name, description, country, city, regions 
            FROM companies WHERE owner_id = $1
        """, user_id)

        if not owner:
            await message.answer("❌ Вы не зарегистрированы как владелец компании.")
            return

        managers = await conn.fetch("""
            SELECT full_name, position, is_active 
            FROM managers WHERE company_id = $1
        """, owner["id"])

        managers_list = "\n".join([
            f"— {m['full_name']} ({m['position'] or '—'}) — {'✅' if m['is_active'] else '❌'}"
            for m in managers
        ]) or "— Нет менеджеров"

        text = (
            f"🏢 <b>Компания: {owner['name']}</b>\n"
            f"🌍 Страна/Город: {owner['country']}, {owner['city']}\n"
            f"📍 Регионы: {', '.join(owner['regions'] or [])}\n"
            f"🧾 Описание: {owner['description'] or '—'}\n\n"
            f"👥 <b>Менеджеры:</b>\n{managers_list}"
        )

        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="👥 Менеджеры")],
                [KeyboardButton(text="📄 Вакансии компании")],
                [KeyboardButton(text="➕ Пригласить менеджера")],
                [KeyboardButton(text="⚙️ Редактировать")]
            ],
            resize_keyboard=True
        )

        await message.answer(text, reply_markup=kb, parse_mode="HTML")
