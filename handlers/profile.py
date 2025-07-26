from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from asyncpg import Pool
from utils.i18n import t

router = Router()

@router.message(F.text.in_(["👤 Личный кабинет", "👤 Profile"]))
async def show_profile(message: Message):
    user_id = message.from_user.id
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        # 👉 Водитель
        driver = await conn.fetchrow("SELECT * FROM drivers WHERE id = $1", user_id)
        if driver:
            lang = driver.get("language", "ru")
            premium = await conn.fetchval("""
                SELECT TRUE FROM payments 
                WHERE user_id = $1 AND role = 'driver' AND payment_type = 'premium'
                ORDER BY created_at DESC LIMIT 1
            """, user_id)

            text = (
                f"👤 <b>{t(lang, 'profile_driver')}</b>\n"
                f"{t(lang, 'full_name')}: {driver.get('full_name') or '—'}\n"
                f"{t(lang, 'truck_type')}: {driver.get('truck_type') or '—'}\n"
                f"{t(lang, 'experience')}: {driver.get('experience') or '—'}\n"
                f"{t(lang, 'regions')}: {', '.join(driver.get('regions') or []) or '—'}\n"
                f"{t(lang, 'subscription')}: {'✅ ' + t(lang, 'active') if premium else '❌ ' + t(lang, 'inactive')}"
            )

            kb = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text=t(lang, "menu_driver_resume"))],
                    [KeyboardButton(text=t(lang, "bonuses"))],
                    [KeyboardButton(text=t(lang, "menu_driver_buy"))],
                    [KeyboardButton(text="📊 " + t(lang, "stats"))],
                    [KeyboardButton(text="🌐 " + t(lang, "change_language"))]
                ],
                resize_keyboard=True
            )
            await message.answer(text, reply_markup=kb, parse_mode="HTML")
            return

        # 👉 Менеджер
        manager = await conn.fetchrow("SELECT * FROM managers WHERE user_id = $1", user_id)
        if manager:
            lang = manager.get("language", "ru")
            premium = await conn.fetchval("""
                SELECT TRUE FROM payments 
                WHERE user_id = $1 AND role = 'manager' AND payment_type = 'premium'
                ORDER BY created_at DESC LIMIT 1
            """, user_id)

            text = (
                f"👤 <b>{t(lang, 'profile_manager')}</b>\n"
                f"{t(lang, 'company')}: {manager.get('company_name') or '—'}\n"
                f"{t(lang, 'position')}: {manager.get('position') or '—'}\n"
                f"{t(lang, 'regions')}: {', '.join(manager.get('regions') or []) or '—'}\n"
                f"{t(lang, 'subscription')}: {'✅ ' + t(lang, 'active') if premium else '❌ ' + t(lang, 'inactive')}"
            )

            kb = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text=t(lang, "menu_manager_publish"))],
                    [KeyboardButton(text=t(lang, "menu_manager_vacancies"))],
                    [KeyboardButton(text=t(lang, "bonuses"))],
                    [KeyboardButton(text=t(lang, "menu_driver_buy"))],
                    [KeyboardButton(text="🌐 " + t(lang, "change_language"))]
                ],
                resize_keyboard=True
            )
            await message.answer(text, reply_markup=kb, parse_mode="HTML")
            return

        # 👉 Владелец компании
        company = await conn.fetchrow("SELECT * FROM companies WHERE owner_id = $1", user_id)
        if company:
            lang = "ru"  # 👈 можно сохранять язык при регистрации, пока — по умолчанию
            text = (
                f"🏢 <b>{t(lang, 'profile_company')}</b>\n"
                f"{t(lang, 'name')}: {company.get('name') or '—'}\n"
                f"{t(lang, 'country')}: {company.get('country') or '—'}, {t(lang, 'city')}: {company.get('city') or '—'}\n"
                f"{t(lang, 'regions')}: {', '.join(company.get('regions') or []) or '—'}\n"
                f"{t(lang, 'description')}: {company.get('description') or '—'}"
            )

            kb = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text=t(lang, "menu_company_managers"))],
                    [KeyboardButton(text="📊 " + t(lang, "stats"))],
                    [KeyboardButton(text="🌐 " + t(lang, "change_language"))]
                ],
                resize_keyboard=True
            )
            await message.answer(text, reply_markup=kb, parse_mode="HTML")
            return

    await message.answer("❌ Профиль не найден.")
