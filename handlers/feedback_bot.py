from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

# 📌 Список ID админов
ADMIN_IDS = [5814167740, 787919568]

# 👥 Состояние для обратной связи
class FeedbackState(StatesGroup):
    waiting_for_feedback = State()

# 💬 Команда /feedback или кнопка
@router.message(Command("feedback"))
@router.message(F.text.lower() == "💬 предложить идею / жалобу")
async def ask_feedback(message: Message, state: FSMContext):
    await state.set_state(FeedbackState.waiting_for_feedback)
    await message.answer(
        "📝 Напишите своё предложение, идею или жалобу одним сообщением.\n\n"
        "Мы внимательно читаем все обращения!",
        reply_markup=ReplyKeyboardRemove()
    )

# 📥 Приём сообщения
@router.message(FeedbackState.waiting_for_feedback)
async def receive_feedback(message: Message, state: FSMContext):
    text = message.text.strip()
    user = message.from_user

    if not text:
        await message.answer("⚠️ Пожалуйста, отправьте не пустое сообщение.")
        return

    # ✉️ Формирование текста
    feedback = (
        f"📬 <b>Новое сообщение от пользователя</b>\n\n"
        f"👤 <b>{user.full_name}</b> (@{user.username or '—'})\n"
        f"🆔 ID: <code>{user.id}</code>\n\n"
        f"<i>{text}</i>"
    )

    # 📤 Отправка администраторам
    for admin_id in ADMIN_IDS:
        try:
            await message.bot.send_message(admin_id, feedback, parse_mode="HTML")
        except Exception:
            continue

    await message.answer("✅ Спасибо! Ваше сообщение отправлено администрации.")
    await state.clear()
