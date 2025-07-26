from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.start_kb import get_language_keyboard

router = Router()

# 🌐 Кнопка: Сменить язык
@router.message(F.text == "🌐 Сменить язык")
async def ask_language(message: Message, state: FSMContext):
    await message.answer("🌐 Пожалуйста, выберите язык:", reply_markup=get_language_keyboard())

# 🈯 Выбор языка
@router.callback_query(F.data.startswith("lang_"))
async def change_language(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split("_")[1]
    await state.update_data(language=lang)
    await callback.answer("✅ Язык изменён.")
    await callback.message.edit_text("Язык успешно изменён.")
