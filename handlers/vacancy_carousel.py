from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from asyncpg import Pool

router = Router()
vacancy_cache = {}  # 🧠 Хранилище вакансий на пользователя

# 🔘 Кнопка: "📄 Вакансии"
@router.message(F.text == "📄 Вакансии")
async def show_first_vacancy(message: Message, state: FSMContext):
    user_id = message.from_user.id
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        vacancies = await conn.fetch("""
            SELECT v.id, v.title, v.truck_type, v.salary, v.region, v.requirements, v.contacts, c.name AS company_name
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE v.is_published = TRUE
            ORDER BY v.created_at DESC
            LIMIT 20
        """)

    if not vacancies:
        await message.answer("❌ Вакансий пока нет.")
        return

    vacancy_cache[user_id] = vacancies
    await state.update_data(vacancy_index=0)
    await send_vacancy_card(message, vacancies[0], 0, len(vacancies))


# 📩 Отправка карточки
async def send_vacancy_card(message_or_cb, vacancy, index, total):
    user_id = message_or_cb.from_user.id
    app = message_or_cb.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        has_premium = await conn.fetchval("""
            SELECT TRUE FROM payments 
            WHERE user_id = $1 AND role = 'driver' 
              AND payment_type = 'premium'
              AND created_at > (CURRENT_DATE - INTERVAL '30 days')
            LIMIT 1
        """, user_id) or False

    # Кнопки
    buttons = []

    if total > 1:
        nav_buttons = [
            InlineKeyboardButton(text="◀️ Назад", callback_data="prev_vacancy"),
            InlineKeyboardButton(text="▶️ Вперёд", callback_data="next_vacancy")
        ]
    else:
        nav_buttons = []

    apply_button = InlineKeyboardButton(
        text="📬 Откликнуться" if has_premium else "🔒 Только с Premium",
        callback_data="apply_allowed" if has_premium else "apply_disabled"
    )

    buttons.append([*nav_buttons] if nav_buttons else [apply_button])
    if nav_buttons:
        buttons.append([apply_button])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    text = (
        f"📌 <b>{vacancy['title']}</b>\n"
        f"🏢 Компания: {vacancy['company_name']}\n"
        f"🚛 Транспорт: {vacancy['truck_type']}\n"
        f"💰 Зарплата: {vacancy['salary']}\n"
        f"🌍 Регион: {vacancy['region']}\n"
        f"📋 Требования: {vacancy['requirements']}\n"
        f"📱 Контакты: {vacancy['contacts'] if has_premium else '🔒 Только для Premium'}\n\n"
        f"Вакансия {index+1} из {total}"
    )

    if isinstance(message_or_cb, CallbackQuery):
        await message_or_cb.message.edit_text(text, parse_mode="HTML", reply_markup=kb)
        await message_or_cb.answer()
    else:
        await message_or_cb.answer(text, parse_mode="HTML", reply_markup=kb)


# ▶️ Вперёд
@router.callback_query(F.data == "next_vacancy")
async def next_vacancy(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    data = await state.get_data()
    index = data.get("vacancy_index", 0)
    vacancies = vacancy_cache.get(user_id)

    if vacancies and index + 1 < len(vacancies):
        index += 1
        await state.update_data(vacancy_index=index)
        await send_vacancy_card(call, vacancies[index], index, len(vacancies))


# ◀️ Назад
@router.callback_query(F.data == "prev_vacancy")
async def prev_vacancy(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    data = await state.get_data()
    index = data.get("vacancy_index", 0)
    vacancies = vacancy_cache.get(user_id)

    if vacancies and index > 0:
        index -= 1
        await state.update_data(vacancy_index=index)
        await send_vacancy_card(call, vacancies[index], index, len(vacancies))


# 🔒 Без подписки
@router.callback_query(F.data == "apply_disabled")
async def apply_vacancy_locked(call: CallbackQuery):
    await call.answer("⚠️ Функция отклика доступна только с активной подпиской Premium.", show_alert=True)


# ✅ Заглушка на отклик (в будущем подключим отклик)
@router.callback_query(F.data == "apply_allowed")
async def apply_vacancy_enabled(call: CallbackQuery):
    await call.answer("✅ Отклик на вакансию отправлен! (заглушка)", show_alert=True)
