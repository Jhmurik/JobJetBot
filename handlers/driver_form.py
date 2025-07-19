from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from states.driver_state import DriverForm

router = Router()

# Главное меню водителя
driver_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Создать анкету водителя")],
        [KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="🌐 Сменить язык")],
        [KeyboardButton(text="🚫 Выключить анкету")],
        [KeyboardButton(text="✅ Включить анкету (платно)")]
    ],
    resize_keyboard=True
)

# Запуск создания анкеты водителя
@router.message(F.text == "📝 Создать анкету водителя")
async def start_driver_form(message: Message, state: FSMContext):
    await state.set_state(DriverForm.full_name)
    await message.answer("📝 Отлично! Начнём заполнение анкеты.\nВведите ваше *полное имя* (ФИО):", parse_mode="Markdown")
