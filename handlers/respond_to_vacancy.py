from aiogram import Router, F
from aiogram.types import CallbackQuery
from asyncpg import Pool
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.callback_query(F.data.startswith("respond_"))
async def respond_to_vacancy(callback: CallbackQuery):
    vacancy_id = callback.data.split("_", maxsplit=1)[1]
    driver_id = callback.from_user.id

    app = callback.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        # Проверка существования отклика
        exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT 1 FROM responses
                WHERE driver_id = $1 AND vacancy_id = $2
            )
        """, driver_id, vacancy_id)

        if exists:
            await callback.answer("❗Вы уже откликались на эту вакансию", show_alert=True)
            return

        # Запись отклика
        await conn.execute("""
            INSERT INTO responses (vacancy_id, driver_id)
            VALUES ($1, $2)
        """, vacancy_id, driver_id)

        await callback.answer("✅ Вы успешно откликнулись!")
