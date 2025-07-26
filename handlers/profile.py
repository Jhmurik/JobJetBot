from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from asyncpg import Pool

router = Router()

@router.message(F.text == "👤 Личный кабинет")
async def show_profile(message: Message):
    user_id = message.from_user.id
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        # Водитель
        driver = await conn.fetchrow("SELECT * FROM drivers WHERE id = $1", user_id)
        if driver:
            premium = await conn.fetchval("""
                SELECT TRUE FROM payments 
                WHERE user_id = $1 AND role = 'driver' AND payment_type = 'premium'
                ORDER BY created_at DESC LIMIT 1
            """, user_id)
            text = (
                f"👤 <b>Ваш профиль (Водитель)</b>\n"
                f"👨‍🚒 Имя: {driver['full_name']}\n"
                f"🚗 Тип ТС: {driver['truck_type']}\n"
                f"⏳ Опыт: {driver['experience']}\n"
                f"🌍 Регионы: {', '.join(driver['regions'] or [])}\n"
                f"🌐 Подписка: {'активна' if premium else 'нет'}"
            )
            kb = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="📄 Моя анкета")],
                    [KeyboardButton(text="🎁 Бонусы и скидки")],
                    [KeyboardButton(text="💳 Купить подписку")],
                    [KeyboardButton(text="📊 Статистика")]
                ],
                resize_keyboard=True
            )
            await message.answer(text, reply_markup=kb, parse_mode="HTML")
            return

        # Менеджер
        manager = await conn.fetchrow("SELECT * FROM managers WHERE user_id = $1", user_id)
        if manager:
            company_name = manager.get("company_name") or "—"
            position = manager.get("position") or "—"
            regions = ", ".join(manager["regions"] or [])
            premium = await conn.fetchval("""
                SELECT TRUE FROM payments 
                WHERE user_id = $1 AND role = 'manager' AND payment_type = 'premium'
                ORDER BY created_at DESC LIMIT 1
            """, user_id)
            text = (
                f"👤 <b>Ваш профиль (Менеджер)</b>\n"
                f"🏢 Компания: {company_name}\n"
                f"🧑‍💼 Должность: {position}\n"
                f"🌍 Регионы: {regions}\n"
                f"🌐 Подписка: {'активна' if premium else 'нет'}"
            )
            kb = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="📢 Опубликовать вакансию")],
                    [KeyboardButton(text="📄 Мои вакансии")],
                    [KeyboardButton(text="🎁 Бонусы и скидки")],
                    [KeyboardButton(text="💳 Купить подписку")]
                ],
                resize_keyboard=True
            )
            await message.answer(text, reply_markup=kb, parse_mode="HTML")
            return

        # Владелец компании
        company = await conn.fetchrow("SELECT * FROM companies WHERE owner_id = $1", user_id)
        if company:
            regions = ", ".join(company["regions"] or [])
            text = (
                f"🏢 <b>Профиль вашей компании</b>\n"
                f"📛 Название: {company['name']}\n"
                f"📍 Страна: {company['country']}, город: {company['city']}\n"
                f"🌍 Регионы: {regions}\n"
                f"📝 Описание: {company['description'] or '—'}"
            )
            kb = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="📄 Мои менеджеры")],
                    [KeyboardButton(text="📊 Статистика")],
                    [KeyboardButton(text="🎁 Бонусы и скидки")]
                ],
                resize_keyboard=True
            )
            await message.answer(text, reply_markup=kb, parse_mode="HTML")
            return

    await message.answer("❌ Профиль не найден.")
