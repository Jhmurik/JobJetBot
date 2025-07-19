from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.start_state import StartState
from keyboards.start_kb import get_language_keyboard, get_role_keyboard, get_region_keyboard

router = Router()

# 💬 /start
@router.message(Command("start"))
async def start_bot(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(StartState.language)
    await message.answer("🌐 Пожалуйста, выберите язык:", reply_markup=get_language_keyboard())

# 🌐 Язык
@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split("_")[1]
    await state.update_data(language=lang)
    await state.set_state(StartState.role)
    await callback.message.edit_text("👤 Кто вы?", reply_markup=get_role_keyboard())

# 🧑 Роль
@router.callback_query(F.data.startswith("role_"))
async def set_role(callback: CallbackQuery, state: FSMContext):
    role = callback.data.split("_")[1]
    await state.update_data(role=role)
    await state.update_data(regions=[])
    await state.set_state(StartState.regions)
    await callback.message.edit_text("🌍 Выберите регион(ы) для работы:", reply_markup=get_region_keyboard())

# 🌍 Регионы
@router.callback_query(F.data.startswith("region_"))
async def set_regions(callback: CallbackQuery, state: FSMContext):
    region = callback.data.split("_")[1]
    data = await state.get_data()
    regions = data.get("regions", [])
    role = data.get("role")

    if region == "done":
        await state.update_data(regions=regions)
        await state.clear()

        if role == "driver":
            # Главное меню водителя
            menu_kb = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="📝 Создать анкету водителя")],
                    [KeyboardButton(text="📊 Статистика")],
                    [KeyboardButton(text="🌐 Сменить язык")],
                    [KeyboardButton(text="🚫 Выключить анкету")],
                    [KeyboardButton(text="✅ Включить анкету (платно)")]
                ],
                resize_keyboard=True
            )
            await callback.message.edit_text("✅ Настройка завершена.\n🏁 Главное меню:", reply_markup=None)
            await callback.message.answer("Выберите действие:", reply_markup=menu_kb)

        elif role == "company":
            await callback.message.edit_text("🏢 Создание компании — скоро будет доступно.")

        elif role == "manager":
            await callback.message.edit_text("👨‍💼 Регистрация менеджера — скоро будет доступна.")

    else:
        if region in regions:
            regions.remove(region)
        else:
            regions.append(region)
        await state.update_data(regions=regions)
        await callback.message.edit_reply_markup(reply_markup=get_region_keyboard(regions))
