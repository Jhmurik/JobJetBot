from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from utils.stats import count_drivers, count_companies, count_vacancies, count_premium_subs

router = Router()

# ✅ Обработчик команды /stats
@router.message(Command("stats"))
async def show_stats_command(message: Message):
    app = message.bot._ctx.get("application")
    if not app or "db" not in app:
        await message.answer("❌ Ошибка: подключение к базе данных недоступно.")
        return

    pool = app["db"]
    total_drivers = await count_drivers(pool)
    total_companies = await count_companies(pool)
    total_vacancies = await count_vacancies(pool)
    total_subs = await count_premium_subs(pool)

    await message.answer(
        f"📊 <b>Статистика проекта JobJet AI</b>\n\n"
        f"🚚 Водителей: <b>{total_drivers}</b>\n"
        f"🏢 Компаний: <b>{total_companies}</b>\n"
        f"📄 Вакансий: <b>{total_vacancies}</b>\n"
        f"💳 Premium-подписок: <b>{total_subs}</b>",
        parse_mode="HTML"
    )

# ✅ Обработчик текста "📊 Статистика" (при нажатии кнопки)
@router.message(F.text.in_(["📊 Статистика", "Статистика", "статистика"]))
async def show_stats_text(message: Message):
    await show_stats_command(message)
