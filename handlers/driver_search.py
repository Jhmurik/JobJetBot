from aiogram import Router, F from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton from asyncpg import Pool from aiogram.fsm.context import FSMContext

router = Router()

🧠 Кэш анкет водителей

search_cache = {}

🔍 Поиск водителей

@router.message(F.text == "🔍 Найти водителей") async def find_drivers(message: Message, state: FSMContext): user_id = message.from_user.id app = message.bot._ctx.get("application") pool: Pool = app["db"]

async with pool.acquire() as conn:
    # Проверка подписки менеджера
    is_premium = await conn.fetchval("""
        SELECT TRUE FROM payments
        WHERE user_id = $1 AND role = 'manager'
          AND payment_type = 'premium'
          AND created_at > (CURRENT_DATE - INTERVAL '30 days')
        LIMIT 1
    """, user_id)

    if not is_premium:
        await message.answer("❌ Эта функция доступна только с активной Premium-подпиской.")
        return

    # Загрузка анкет водителей
    drivers = await conn.fetch("""
        SELECT * FROM drivers
        WHERE is_active = TRUE
        ORDER BY created_at DESC
        LIMIT 20
    """)

if not drivers:
    await message.answer("❌ Анкет водителей пока нет.")
    return

search_cache[user_id] = drivers
await state.update_data(driver_index=0)
await send_driver_card(message, drivers[0], 0, len(drivers))

📇 Карточка водителя

async def send_driver_card(message_or_cb, driver, index, total): text = ( f"👨‍🔧 <b>{driver['full_name']}</b>\n" f"📅 Возраст: {driver['birth_date']}\n" f"🌍 Регионы: {', '.join(driver['regions'] or [])}\n" f"🚛 Транспорт: {driver['truck_type']}\n" f"🪪 Права: {driver['license_type']}\n" f"⏳ Опыт: {driver['experience']}\n" f"🗣️ Языки: {', '.join(driver['languages'] or [])}\n" f"📦 Занятость: {driver['employment_type']}\n" f"📱 Контакты: {driver['contacts']}\n\n" f"Анкета {index+1} из {total}" )

kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="◀️", callback_data="prev_driver"),
        InlineKeyboardButton(text="💬 Написать", callback_data="contact_driver"),
        InlineKeyboardButton(text="▶️", callback_data="next_driver")
    ],
    [InlineKeyboardButton(text="💛 В избранное", callback_data="save_driver")]
])

if isinstance(message_or_cb, CallbackQuery):
    await message_or_cb.message.edit_text(text, parse_mode="HTML", reply_markup=kb)
    await message_or_cb.answer()
else:
    await message_or_cb.answer(text, parse_mode="HTML", reply_markup=kb)

▶️ Следующий водитель

@router.callback_query(F.data == "next_driver") async def next_driver(call: CallbackQuery, state: FSMContext): user_id = call.from_user.id data = await state.get_data() index = data.get("driver_index", 0) drivers = search_cache.get(user_id)

if drivers and index + 1 < len(drivers):
    index += 1
    await state.update_data(driver_index=index)
    await send_driver_card(call, drivers[index], index, len(drivers))

◀️ Предыдущий водитель

@router.callback_query(F.data == "prev_driver") async def prev_driver(call: CallbackQuery, state: FSMContext): user_id = call.from_user.id data = await state.get_data() index = data.get("driver_index", 0) drivers = search_cache.get(user_id)

if drivers and index > 0:
    index -= 1
    await state.update_data(driver_index=index)
    await send_driver_card(call, drivers[index], index, len(drivers))

💬 Связаться (заглушка)

@router.callback_query(F.data == "contact_driver") async def contact_driver(call: CallbackQuery): await call.answer("🔒 Чат с водителем будет доступен после запуска функции общения.", show_alert=True)

💛 Сохранить водителя (заглушка)

@router.callback_query(F.data == "save_driver") async def save_driver(call: CallbackQuery): await call.answer("💾 Добавлено в избранное (в разработке)", show_alert=True)

                                                                      
