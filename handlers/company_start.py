from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from states.company_state import CompanyStart
from keyboards.company_kb import get_company_start_keyboard

router = Router()

# 📦 Обработка кнопки "Для компаний"
@router.message(F.text == "📦 Для компаний")
async def company_menu(message: Message, state: FSMContext):
    await state.set_state(CompanyStart.menu)
    await message.answer("Выберите действие:", reply_markup=get_company_start_keyboard())

# 💼 Обработка нажатий на варианты
@router.callback_query(CompanyStart.menu, F.data.startswith("company_"))
async def company_menu_choice(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]

    if action == "register":
        await callback.message.edit_text("📝 Регистрация компании. Введите *название компании*:", parse_mode="Markdown")
        await state.set_state(CompanyStart.name)

    elif action == "join":
        await callback.message.edit_text("🔑 Введите код подключения от компании:")
        await state.set_state(CompanyStart.join_code)
