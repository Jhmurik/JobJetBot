from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from asyncpg import Pool
import uuid

router = Router()

# 📩 Отклик на вакансию
@router.callback_query(F.data.startswith("respond_"))
async def handle_response(callback: CallbackQuery):
    user_id = callback.from_user.id
    vacancy_id = callback.data.split("_")[1]

    app = callback.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        # Проверка: анкета водителя есть?
        driver = await conn.fetchrow("SELECT id FROM drivers WHERE id = $1", user_id)
        if not driver:
            await callback.answer("❌ Сначала заполните анкету водителя.", show_alert=True)
            return

        # Проверка: уже откликался?
        existing = await conn.fetchrow("SELECT 1 FROM responses WHERE vacancy_id = $1 AND driver_id = $2", vacancy_id, user_id)
        if existing:
            await callback.answer("⏳ Вы уже откликались.", show_alert=True)
            return

        # Вставка отклика
        await conn.execute("""
            INSERT INTO responses (vacancy_id, driver_id)
            VALUES ($1, $2)
        """, uuid.UUID(vacancy_id), user_id)

        # Уведомление (в будущем отправим менеджеру)
        await callback.answer("✅ Отклик отправлен!", show_alert=True)
