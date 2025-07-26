from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from asyncpg import Pool

router = Router()


@router.message(F.text == "📬 Отклики на вакансии")
async def list_manager_vacancies(message: Message, state: FSMContext):
    user_id = message.from_user.id
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        # Проверка подписки менеджера
        has_premium = await conn.fetchval("""
            SELECT TRUE FROM payments 
            WHERE user_id = $1 AND role = 'manager' 
              AND payment_type = 'premium'
              AND created_at > (CURRENT_DATE - INTERVAL '30 days')
            LIMIT 1
        """, user_id)

        if not has_premium:
            await message.answer("🔒 Просмотр откликов доступен только менеджерам с активной подпиской.")
            return

        # Получение вакансий менеджера
        vacancies = await conn.fetch("""
            SELECT v.id, v.title
            FROM vacancies v
            JOIN managers m ON v.manager_id = m.id
            WHERE m.user_id = $1
            ORDER BY v.created_at DESC
        """, user_id)

        if not vacancies:
            await message.answer("❌ У вас пока нет опубликованных вакансий.")
            return

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=v['title'], callback_data=f"view_responses_{v['id']}")]
            for v in vacancies
        ])

        await message.answer("📋 Выберите вакансию для просмотра откликов:", reply_markup=kb)


@router.callback_query(F.data.startswith("view_responses_"))
async def show_responses(call: CallbackQuery):
    vacancy_id = call.data.split("_", 2)[2]
    app = call.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        responses = await conn.fetch("""
            SELECT d.full_name, d.experience, d.truck_type, d.contacts
            FROM vacancy_responses r
            JOIN drivers d ON r.driver_id = d.id
            WHERE r.vacancy_id = $1
            ORDER BY r.created_at DESC
        """, vacancy_id)

        if not responses:
            await call.message.edit_text("❌ Пока нет откликов на эту вакансию.")
            await call.answer()
            return

        text = "📬 <b>Отклики на вакансию:</b>\n\n"
        for i, r in enumerate(responses, start=1):
            text += (
                f"<b>{i}. {r['full_name']}</b>\n"
                f"🚛 Тип ТС: {r['truck_type']}\n"
                f"⏳ Опыт: {r['experience']}\n"
                f"📱 Контакты: {r['contacts']}\n\n"
            )

        await call.message.edit_text(text, parse_mode="HTML")
        await call.answer()
