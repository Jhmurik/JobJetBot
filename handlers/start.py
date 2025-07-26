from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from states.start_state import StartState
from keyboards.start_kb import get_language_keyboard, get_role_keyboard, get_region_keyboard
from asyncpg import Pool
from uuid import UUID
from utils.i18n import t  # 👈 мультиязычность

router = Router()

# 💬 /start (в том числе с deep-link)
@router.message(Command("start"))
async def start_bot(message: Message, state: FSMContext, command: CommandObject):
    await state.clear()

    # 📊 Статистика
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]
    async with pool.acquire() as conn:
        drivers_count = await conn.fetchval("SELECT COUNT(*) FROM drivers")
        companies_count = await conn.fetchval("SELECT COUNT(*) FROM companies")

    stats_text = (
        f"📊 JobJet AI:\n"
        f"🚚 {drivers_count} {t('ru', 'drivers')}\n"
        f"🏢 {companies_count} {t('ru', 'companies')}\n\n"
    )

    # Deep link
    payload = command.args
    if payload and payload.startswith("join_"):
        try:
            company_id = UUID(payload.replace("join_", ""))
            await state.update_data(join_company_id=company_id, role="manager")
        except Exception:
            await message.answer("❌ Неверный код подключения.")
            return

    await state.set_state(StartState.language)
    await message.answer(stats_text + t("ru", "start_choose_language"), reply_markup=get_language_keyboard())


# 🌐 Выбор языка
@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split("_")[1]
    await state.update_data(language=lang)

    data = await state.get_data()
    if data.get("role") == "manager" and data.get("join_company_id"):
        await state.update_data(regions=[])
        await state.set_state(StartState.regions)
        await callback.message.edit_text(t(lang, "start_choose_region"), reply_markup=get_region_keyboard())
    else:
        await state.set_state(StartState.role)
        await callback.message.edit_text(t(lang, "start_choose_role"), reply_markup=get_role_keyboard())


# 👤 Выбор роли
@router.callback_query(F.data.startswith("role_"))
async def set_role(callback: CallbackQuery, state: FSMContext):
    role = callback.data.split("_")[1]
    await state.update_data(role=role, regions=[])
    await state.set_state(StartState.regions)

    lang = (await state.get_data()).get("language", "ru")
    await callback.message.edit_text(t(lang, "start_choose_region"), reply_markup=get_region_keyboard())


# 🌍 Выбор региона (мультивыбор)
@router.callback_query(F.data.startswith("region_"))
async def set_regions(callback: CallbackQuery, state: FSMContext):
    region = callback.data.split("_")[1]
    data = await state.get_data()
    regions = data.get("regions", [])
    role = data.get("role")
    lang = data.get("language", "ru")

    if region == "done":
        await state.update_data(regions=regions)
        await state.set_state(StartState.consent)
        await callback.message.edit_text(t(lang, "consent_text"))
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="✅ Согласен")]],
            resize_keyboard=True
        )
        await callback.message.answer(t(lang, "consent_confirm"), reply_markup=kb)
    else:
        if region in regions:
            regions.remove(region)
        else:
            regions.append(region)
        await state.update_data(regions=regions)
        await callback.message.edit_reply_markup(reply_markup=get_region_keyboard(regions))


# ✅ Подтверждение согласия
@router.message(F.text == "✅ Согласен")
async def confirm_consent(message: Message, state: FSMContext):
    data = await state.get_data()
    role = data.get("role")
    lang = data.get("language", "ru")
    await state.update_data(consent=True)
    await state.clear()

    if role == "driver":
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📝 Создать анкету водителя")],
                [KeyboardButton(text="📄 Вакансии"), KeyboardButton(text="💳 Купить подписку")],
                [KeyboardButton(text="📊 Статистика")],
                [KeyboardButton(text="🌐 Сменить язык")],
                [KeyboardButton(text="🚫 Выключить анкету"), KeyboardButton(text="✅ Включить анкету (платно)")]
            ],
            resize_keyboard=True
        )
        await message.answer(f"{t(lang, 'setup_complete')}\n{t(lang, 'menu_driver')}", reply_markup=kb)

    elif role == "company":
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📦 Зарегистрировать компанию")],
                [KeyboardButton(text="📊 Статистика")],
                [KeyboardButton(text="🌐 Сменить язык")]
            ],
            resize_keyboard=True
        )
        await message.answer(f"{t(lang, 'setup_complete')}\n{t(lang, 'menu_company')}", reply_markup=kb)

    elif role == "manager":
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="👨‍💼 Зарегистрироваться как менеджер")],
                [KeyboardButton(text="💳 Купить подписку")],
                [KeyboardButton(text="📊 Статистика")],
                [KeyboardButton(text="🌐 Сменить язык")]
            ],
            resize_keyboard=True
        )
        await message.answer(f"{t(lang, 'setup_complete')}\n{t(lang, 'menu_manager')}", reply_markup=kb)
