from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from states.start_state import StartState
from keyboards.start_kb import get_language_keyboard, get_role_keyboard, get_region_keyboard
from uuid import UUID

router = Router()

# 💬 /start (с поддержкой deep-link для менеджеров)
@router.message(Command("start"))
async def start_bot(message: Message, state: FSMContext, command: CommandObject):
    await state.clear()

    payload = command.args
    if payload and payload.startswith("join_"):
        try:
            company_id = UUID(payload.replace("join_", ""))
            await state.update_data(join_company_id=company_id, role="manager")
        except Exception:
            await message.answer("❌ Неверный код приглашения.")
            return

    await state.set_state(StartState.language)
    await message.answer("🌐 Пожалуйста, выберите язык:", reply_markup=get_language_keyboard())

# 🌐 Выбор языка
@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split("_")[1]
    await state.update_data(language=lang)

    data = await state.get_data()
    if data.get("role") == "manager" and data.get("join_company_id"):
        await state.update_data(regions=[])
        await state.set_state(StartState.regions)
        await callback.message.edit_text("🌍 Выберите регион(ы) для работы:", reply_markup=get_region_keyboard())
    else:
        await state.set_state(StartState.role)
        await callback.message.edit_text("👤 Кто вы?", reply_markup=get_role_keyboard())

# 👤 Выбор роли
@router.callback_query(F.data.startswith("role_"))
async def set_role(callback: CallbackQuery, state: FSMContext):
    role = callback.data.split("_")[1]
    await state.update_data(role=role, regions=[])
    await state.set_state(StartState.regions)
    await callback.message.edit_text("🌍 Выберите регион(ы) для работы:", reply_markup=get_region_keyboard())

# 🌍 Выбор регионов (мультивыбор)
@router.callback_query(F.data.startswith("region_"))
async def set_regions(callback: CallbackQuery, state: FSMContext):
    region = callback.data.split("_")[1]
    data = await state.get_data()
    regions = data.get("regions", [])
    role = data.get("role")

    if region == "done":
        await state.update_data(regions=regions)
        await state.clear()

        # Главное меню по роли
        if role == "driver":
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
            menu_kb = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="📦 Зарегистрировать компанию")],
                    [KeyboardButton(text="📊 Статистика")],
                    [KeyboardButton(text="🌐 Сменить язык")]
                ],
                resize_keyboard=True
            )
            await callback.message.edit_text("✅ Настройка завершена.\n🏢 Главное меню компании:", reply_markup=None)
            await callback.message.answer("Выберите действие:", reply_markup=menu_kb)

        elif role == "manager":
            menu_kb = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="👨‍💼 Зарегистрироваться как менеджер")],
                    [KeyboardButton(text="📊 Статистика")],
                    [KeyboardButton(text="🌐 Сменить язык")]
                ],
                resize_keyboard=True
            )
            await callback.message.edit_text("✅ Настройка завершена.\n👨‍💼 Главное меню менеджера:", reply_markup=None)
            await callback.message.answer("Выберите действие:", reply_markup=menu_kb)

    else:
        if region in regions:
            regions.remove(region)
        else:
            regions.append(region)
        await state.update_data(regions=regions)
        await callback.message.edit_reply_markup(reply_markup=get_region_keyboard(regions))
