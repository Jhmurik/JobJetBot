from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from asyncpg import Pool

router = Router()

# 🧠 Временное хранилище вакансий в памяти
vacancy_cache = {}

# 🔘 Кнопка: "Вакансии"
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


# 📩 Карточка вакансии
async def send_vacancy_card(message_or_cb, vacancy, index, total):
    text = (
        f"📌 <b>{vacancy['title']}</b>\n"
        f"🏢 Компания: {vacancy['company_name']}\n"
        f"🚛 Транспорт: {vacancy['truck_type']}\n"
        f"💰 Зарплата: {vacancy['salary']}\n"
        f"🌍 Регион: {vacancy['region']}\n"
        f"📋 Требования: {vacancy['requirements']}\n"
        f"📱 Контакты: {vacancy['contacts']}\n\n"
        f"Вакансия {index+1} из {total}"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ Назад", callback_data="prev_vacancy"),
            InlineKeyboardButton(text="📬 Откликнуться", callback_data="apply_disabled"),
            InlineKeyboardButton(text="▶️ Вперёд", callback_data="next_vacancy")
        ]
    ])

    if isinstance(message_or_cb, CallbackQuery):
        await message_or_cb.message.edit_text(text, parse_mode="HTML", reply_markup=kb)
        await message_or_cb.answer()
    else:
        await message_or_cb.answer(text, parse_mode="HTML", reply_markup=kb)


# 🔁 Следующая вакансия
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


# ⬅️ Предыдущая вакансия
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


# 📬 Отклик (заглушка)
@router.callback_query(F.data == "apply_disabled")
async def apply_vacancy(call: CallbackQuery):
    await call.answer("❌ Эта функция доступна только с Premium-подпиской.", show_alert=True)
