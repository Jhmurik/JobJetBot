from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from asyncpg import Pool

router = Router()
driver_cache = {}

# 👀 Кнопка: "Водители"
@router.message(F.text == "🚚 Водители")
async def show_first_driver(message: Message, state: FSMContext):
    user_id = message.from_user.id
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        manager = await conn.fetchrow("SELECT id FROM managers WHERE user_id = $1 AND is_active = TRUE", user_id)
        if not manager:
            await message.answer("❌ Доступ к анкетам только с Premium-подпиской.")
            return

        drivers = await conn.fetch("""
            SELECT * FROM drivers
            WHERE is_active = TRUE
            ORDER BY created_at DESC
            LIMIT 20
        """)

    if not drivers:
        await message.answer("❌ Анкет водителей пока нет.")
        return

    driver_cache[user_id] = drivers
    await state.update_data(driver_index=0)
    await send_driver_card(message, drivers[0], 0, len(drivers))


async def send_driver_card(message_or_cb, driver, index, total):
    text = (
        f"👤 <b>{driver['full_name']}</b>\n"
        f"📅 Дата рождения: {driver['birth_date']}\n"
        f"🛂 Гражданство: {driver['citizenship']}\n"
        f"📍 Проживание: {driver['residence']}\n"
        f"🚗 Тип ТС: {driver['truck_type']}\n"
        f"🔑 Категория: {driver['license_type']}\n"
        f"🧰 Опыт: {driver['experience']}\n"
        f"🌍 Регионы: {', '.join(driver['regions'] or [])}\n"
        f"📞 Контакты: {driver['contacts']}\n\n"
        f"Анкета {index+1} из {total}"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ Назад", callback_data="prev_driver"),
            InlineKeyboardButton(text="✉️ Связаться", callback_data="contact_driver"),
            InlineKeyboardButton(text="▶️ Вперёд", callback_data="next_driver")
        ]
    ])

    if isinstance(message_or_cb, CallbackQuery):
        await message_or_cb.message.edit_text(text, parse_mode="HTML", reply_markup=kb)
        await message_or_cb.answer()
    else:
        await message_or_cb.answer(text, parse_mode="HTML", reply_markup=kb)


@router.callback_query(F.data == "next_driver")
async def next_driver(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    data = await state.get_data()
    index = data.get("driver_index", 0)
    drivers = driver_cache.get(user_id)

    if drivers and index + 1 < len(drivers):
        index += 1
        await state.update_data(driver_index=index)
        await send_driver_card(call, drivers[index], index, len(drivers))


@router.callback_query(F.data == "prev_driver")
async def prev_driver(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    data = await state.get_data()
    index = data.get("driver_index", 0)
    drivers = driver_cache.get(user_id)

    if drivers and index > 0:
        index -= 1
        await state.update_data(driver_index=index)
        await send_driver_card(call, drivers[index], index, len(drivers))


@router.callback_query(F.data == "contact_driver")
async def contact_driver(call: CallbackQuery):
    await call.answer("📞 Свяжитесь напрямую по указанным контактам в анкете.", show_alert=True)
