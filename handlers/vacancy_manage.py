from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from asyncpg import Pool
from uuid import UUID

router = Router()

# 📄 Мои вакансии
@router.message(F.text.lower() == "📄 мои вакансии")
async def list_vacancies(message: Message):
    user_id = message.from_user.id
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        manager = await conn.fetchrow("SELECT id FROM managers WHERE user_id = $1", user_id)
        if not manager:
            await message.answer("❌ Вы не зарегистрированы как менеджер.")
            return

        vacancies = await conn.fetch("""
            SELECT id, title, is_published, created_at
            FROM vacancies
            WHERE manager_id = $1
            ORDER BY created_at DESC
            LIMIT 10
        """, manager["id"])

        if not vacancies:
            await message.answer("🔍 У вас пока нет опубликованных вакансий.")
            return

        for v in vacancies:
            status = "✅ Активна" if v["is_published"] else "⛔️ Скрыта"
            text = (
                f"*📌 {v['title']}*\n"
                f"📅 Дата: {v['created_at'].strftime('%Y-%m-%d')}\n"
                f"📍 Статус: {status}"
            )
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🛑 Скрыть", callback_data=f"hide_{v['id']}")],
                [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_{v['id']}")]
            ])
            await message.answer(text, parse_mode="Markdown", reply_markup=kb)

# ⛔️ Скрытие вакансии
@router.callback_query(F.data.startswith("hide_"))
async def hide_vacancy(callback: CallbackQuery):
    vacancy_id = UUID(callback.data.replace("hide_", ""))
    app = callback.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        await conn.execute("UPDATE vacancies SET is_published = FALSE WHERE id = $1", vacancy_id)

    await callback.message.edit_reply_markup()
    await callback.message.answer("⛔️ Вакансия скрыта.")

# 🗑 Удаление вакансии
@router.callback_query(F.data.startswith("delete_"))
async def delete_vacancy(callback: CallbackQuery):
    vacancy_id = UUID(callback.data.replace("delete_", ""))
    app = callback.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM vacancies WHERE id = $1", vacancy_id)

    await callback.message.edit_text("🗑 Вакансия удалена.")
