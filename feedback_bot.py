from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

ADMIN_IDS = [787919568, 5814167740]  # 👮 Администраторы для получения фидбэка

# 🔄 Состояние
class FeedbackState(StatesGroup):
    waiting_feedback = State()

# 🧾 Меню кнопка
@router.message(F.text == "💬 Оставить отзыв")
async def request_feedback(message: Message, state: FSMContext):
    await state.set_state(FeedbackState.waiting_feedback)
    await message.answer("✍️ Пожалуйста, напишите ваш отзыв, жалобу или предложение:")

# 📩 Приём текста и пересылка админу
@router.message(FeedbackState.waiting_feedback)
async def receive_feedback(message: Message, state: FSMContext):
    await state.clear()
    text = message.text
    user = message.from_user

    msg = (
        f"📬 <b>Новое сообщение от пользователя</b>\n\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"👤 Имя: {user.full_name}\n"
        f"📝 Сообщение:\n{text}"
    )

    for admin_id in ADMIN_IDS:
        try:
            await message.bot.send_message(admin_id, msg, parse_mode="HTML")
        except Exception:
            continue

    await message.answer("✅ Спасибо за ваше сообщение! Мы обязательно его рассмотрим.")
