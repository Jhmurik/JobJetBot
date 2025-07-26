from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

# 👥 Состояние для обратной связи
class FeedbackState(StatesGroup):
    waiting_for_feedback = State()

# 📥 Команда /feedback или по кнопке
@router.message(Command("feedback"))
@router.message(F.text.lower() == "💬 предложить идею / жалобу")
async def ask_feedback(message: Message, state: FSMContext):
    await message.answer("📝 Напишите сюда ваше предложение, идею или жалобу. Мы обязательно рассмотрим!")
    await state.set_state(FeedbackState.waiting_for_feedback)

# ✅ Получение сообщения
@router.message(FeedbackState.waiting_for_feedback)
async def receive_feedback(message: Message, state: FSMContext):
    text = message.text
    user = message.from_user

    # 🔔 Отправка админу (можно расширить)
    ADMIN_ID = 787919568  # 👈 Укажите ID администратора
    feedback = (
        f"📩 Новое сообщение от пользователя:\n\n"
        f"👤 <b>{user.full_name}</b> (@{user.username or '—'})\n"
        f"🆔 ID: <code>{user.id}</code>\n\n"
        f"{text}"
    )
    await message.bot.send_message(ADMIN_ID, feedback, parse_mode="HTML")

    await message.answer("✅ Спасибо! Ваше сообщение отправлено администрации.", reply_markup=ReplyKeyboardRemove())
    await state.clear()
