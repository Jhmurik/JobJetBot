from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from asyncpg import Pool
from keyboards.driver_menu import driver_main_kb

router = Router()

@router.message(F.text == "👤 Личный кабинет")
async def driver_profile(message: Message):
    user_id = message.from_user.id
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        driver = await conn.fetchrow("SELECT * FROM drivers WHERE id = $1", user_id)

    if not driver:
        await message.answer("❗️Вы ещё не заполнили анкету водителя.")
        return

    text = (
        f"👤 *Ваш профиль*\n"
        f"👨‍💼 ФИО: {driver['full_name']}\n"
        f"🎂 Дата рождения: {driver['birth_date']}\n"
        f"🌍 Гражданство: {driver['citizenship']}\n"
        f"📍 Место проживания: {driver['residence']}\n"
        f"📄 Документы: {driver['documents']}\n"
        f"🚛 Транспорт: {driver['truck_type']}\n"
        f"💼 Занятость: {driver['employment_type']}\n"
        f"📆 Готов к работе: {driver['ready_to_depart']}\n"
        f"📞 Контакты: {driver['contacts']}\n"
        f"📦 Регионы: {', '.join(driver['regions'])}\n"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Изменить анкету", callback_data="edit_profile")],
        [InlineKeyboardButton(text="🎁 Бонусы и скидки", callback_data="referral_links")],
        [InlineKeyboardButton(text="💳 Подписка", callback_data="driver_subscription_info")]
    ])

    await message.answer(text, reply_markup=kb, parse_mode="Markdown")
