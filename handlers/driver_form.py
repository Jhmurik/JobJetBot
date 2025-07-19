from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from states.driver_state import DriverForm

router = Router()

@router.message(F.text == "📝 Создать анкету водителя")
async def start_driver_form(message: Message, state: FSMContext):
    await state.set_state(DriverForm.full_name)
    await message.answer("📝 Введите ваше полное имя (ФИО):")
