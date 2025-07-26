from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

# 🛠 Обновления проекта
LATEST_UPDATES = [
    "🚀 Добавлен просмотр вакансий в формате карточек",
    "🌍 Реализована поддержка 6 языков",
    "💳 Оплата подписки через USDT (Cryptomus)",
    "📄 Поддержка анкеты водителя и менеджера",
    "📢 Внутренние объявления и рассылки",
    "📬 Возможность откликнуться на вакансию (только Premium)",
    "🔎 Поиск и фильтры вакансий (в разработке)"
]

@router.message(Command("updates"))
@router.message(F.text.lower().in_({"🛠 обновления", "обновления"}))
async def show_updates(message: Message):
    updates_text = "🛠 <b>Последние обновления JobJet AI</b>:\n\n"
    for update in LATEST_UPDATES:
        updates_text += f"• {update}\n"

    await message.answer(updates_text, parse_mode="HTML")
