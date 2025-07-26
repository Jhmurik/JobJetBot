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
        # 👉 Водитель
        driver = await conn.fetchrow("SELECT * FROM drivers WHERE id = $1", user_id)
        if driver:
            lang = driver.get("language") or "ru"
            premium = await conn.fetchval("""
                SELECT TRUE FROM payments 
                WHERE user_id = $1 AND role = 'driver' AND payment_type = 'premium'
                ORDER BY created_at DESC LIMIT 1
            """, user_id)

            text = (
                f"👤 <b>Ваш профиль (Водитель)</b>\n"
                f"👨‍🚒 Имя: {driver.get('full_name') or '—'}\n"
                f"🚗 Тип ТС: {driver.get('truck_type') or '—'}\n"
                f"⏳ Опыт: {driver.get('experience') or '—'}\n"
                f"🌍 Регионы: {', '.join(driver.get('regions') or []) or '—'}\n"
                f"🌐 Подписка: {'активна' if premium else 'нет'}"
            )

            kb = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="📄 Моя анкета")],
                    [KeyboardButton(text="🎁 Бонусы и скидки")],
                    [KeyboardButton(text="💳 Купить подписку")],
                    [KeyboardButton(text="📊 Статистика")],
                    [KeyboardButton(text="🌐 Сменить язык")]
                ],
                resize_keyboard=True
            )
            await message.answer(text, reply_markup=kb, parse_mode="HTML")
            return

        # 👉 Менеджер
        manager = await conn.fetchrow("SELECT * FROM managers WHERE user_id = $1", user_id)
        if manager:
            lang = manager.get("language") or "ru"
            premium = await conn.fetchval("""
                SELECT TRUE FROM payments 
                WHERE user_id = $1 AND role = 'manager' AND payment_type = 'premium'
                ORDER BY created_at DESC LIMIT 1
            """, user_id)

            text = (
                f"👤 <b>Ваш профиль (Менеджер)</b>\n"
                f"🏢 Компания: {manager.get('company_name') or '—'}\n"
                f"🧑‍💼 Должность: {manager.get('position') or '—'}\n"
                f"🌍 Регионы: {', '.join(manager.get('regions') or []) or '—'}\n"
                f"🌐 Подписка: {'активна' if premium else 'нет'}"
            )

            kb = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="📢 Опубликовать вакансию")],
                    [KeyboardButton(text="📄 Мои вакансии")],
                    [KeyboardButton(text="🎁 Бонусы и скидки")],
                    [KeyboardButton(text="💳 Купить подписку")],
                    [KeyboardButton(text="🌐 Сменить язык")]
                ],
                resize_keyboard=True
            )
            await message.answer(text, reply_markup=kb, parse_mode="HTML")
            return

        # 👉 Владелец компании
        company = await conn.fetchrow("SELECT * FROM companies WHERE owner_id = $1", user_id)
        if company:
            text = (
                f"🏢 <b>Профиль вашей компании</b>\n"
                f"📛 Название: {company.get('name') or '—'}\n"
                f"📍 Страна: {company.get('country') or '—'}, город: {company.get('city') or '—'}\n"
                f"🌍 Регионы: {', '.join(company.get('regions') or []) or '—'}\n"
                f"📝 Описание: {company.get('description') or '—'}"
            )

            kb = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="📄 Мои менеджеры")],
                    [KeyboardButton(text="📊 Статистика")],
                    [KeyboardButton(text="🎁 Бонусы и скидки")],
                    [KeyboardButton(text="🌐 Сменить язык")]
                ],
                resize_keyboard=True
            )
            await message.answer(text, reply_markup=kb, parse_mode="HTML")
            return

    # ❌ Если пользователь не найден
    await message.answer("❌ Профиль не найден.")
