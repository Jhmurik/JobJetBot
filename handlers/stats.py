from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils.stats import count_drivers, count_companies, count_vacancies, count_premium_subs
from utils.i18n import t

router = Router()

# ✅ Основной обработчик статистики
async def send_stats(message: Message, lang: str, pool):
    total_drivers = await count_drivers(pool)
    total_companies = await count_companies(pool)
    total_vacancies = await count_vacancies(pool)
    total_subs = await count_premium_subs(pool)

    await message.answer(
        f"📊 <b>{t(lang, 'stats_header')}</b>\n\n"
        f"🚚 {t(lang, 'drivers')}: <b>{total_drivers}</b>\n"
        f"🏢 {t(lang, 'companies')}: <b>{total_companies}</b>\n"
        f"📄 {t(lang, 'vacancies')}: <b>{total_vacancies}</b>\n"
        f"💳 {t(lang, 'subscriptions')}: <b>{total_subs}</b>",
        parse_mode="HTML"
    )

# ✅ Команда /stats
@router.message(Command("stats"))
async def show_stats_command(message: Message, state: FSMContext):
    app = message.bot._ctx.get("application")
    if not app or "db" not in app:
        await message.answer("❌ Ошибка: база данных недоступна.")
        return

    data = await state.get_data()
    lang = data.get("language", "ru")
    await send_stats(message, lang, app["db"])

# ✅ Кнопка "📊 Статистика"
@router.message(F.text.in_(["📊 Статистика", "Статистика", "статистика", "📊 Statistics"]))
async def show_stats_button(message: Message, state: FSMContext):
    await show_stats_command(message, state)
