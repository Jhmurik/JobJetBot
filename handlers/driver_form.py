from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from states.driver_state import DriverForm
from keyboards.main_kb import get_driver_main_kb
from utils.i18n import t

router = Router()

# 🧾 Запуск анкеты водителя
@router.message(F.text.in_(["📝 Создать анкету водителя", "📝 Моя анкета"]))
async def start_driver_form(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(DriverForm.full_name)

    lang = "ru"
    try:
        user_data = await state.get_data()
        lang = user_data.get("language", "ru")
    except:
        pass

    await message.answer(
        t(lang, "form_intro_driver"),
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown"
    )
