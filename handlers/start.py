from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from states.start_state import StartState
from keyboards.start_kb import get_language_keyboard, get_role_keyboard, get_region_keyboard
from asyncpg import Pool
from uuid import UUID
from utils.i18n import t
from utils.stats import count_drivers, count_companies
from handlers.ads import send_active_ads  # 👈 показать рекламу

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

    lang = "ru"
    await state.update_data(language=lang)

    stats_text = (
        f"📊 JobJet AI:\n"
        f"🚚 {drivers_count} {t(lang, 'drivers')}\n"
        f"🏢 {companies_count} {t(lang, 'companies')}\n\n"
    )

    # Deep-link
    payload = command.args
    if payload and payload.startswith("join_"):
        try:
            company_id = UUID(payload.replace("join_", ""))
            await state.update_data(join_company_id=company_id, role="manager")
        except Exception:
            await message.answer(t(lang, "invalid_invite"))
            return

    await state.set_state(StartState.language)
    await message.answer(stats_text + t(lang, "start_choose_language"), reply_markup=get_language_keyboard())

    # 📣 Реклама
    await send_active_ads(message)


# 🌐 Выбор языка
@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split("_")[1]
    await state.update_data(language=lang)

    data = await state.get_data()
    if data.get("role") == "manager" and data.get("join_company_id"):
        await state.update_data(regions=[])
        await state.set_state(StartState.regions)
        await callback.message.edit_text(t(lang, "start_choose_region"), reply_markup=get_region_keyboard(lang))
    else:
        await state.set_state(StartState.role)
        await callback.message.edit_text(t(lang, "start_choose_role"), reply_markup=get_role_keyboard(lang))


# 👤 Выбор роли
@router.callback_query(F.data.startswith("role_"))
async def set_role(callback: CallbackQuery, state: FSMContext):
    role = callback.data.split("_")[1]
    await state.update_data(role=role, regions=[])

    lang = (await state.get_data()).get("language", "ru")
    await state.set_state(StartState.regions)
    await callback.message.edit_text(t(lang, "start_choose_region"), reply_markup=get_region_keyboard(lang))


# 🌍 Выбор региона (мультивыбор)
@router.callback_query(F.data.startswith("region_"))
async def set_regions(callback: CallbackQuery, state: FSMContext):
    region = callback.data.split("_")[1]
    data = await state.get_data()
    regions = data.get("regions", [])
    lang = data.get("language", "ru")

    if region == "done":
        await state.update_data(regions=regions)
        await state.set_state(StartState.consent)
        await callback.message.edit_text(t(lang, "consent_text"))
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="✅ " + t(lang, "consent_button"))]],
            resize_keyboard=True
        )
        await callback.message.answer(t(lang, "consent_confirm"), reply_markup=kb)
    else:
        if region in regions:
            regions.remove(region)
        else:
            regions.append(region)
        await state.update_data(regions=regions)
        await callback.message.edit_reply_markup(reply_markup=get_region_keyboard(lang, regions))


# ✅ Подтверждение согласия
@router.message(F.text.startswith("✅"))
async def confirm_consent(message: Message, state: FSMContext):
    data = await state.get_data()
    role = data.get("role")
    lang = data.get("language", "ru")
    await state.update_data(consent=True)
    await state.clear()

    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    if role == "driver":
        kb.keyboard = [
            [KeyboardButton(text=t(lang, "menu_driver_create"))],
            [KeyboardButton(text=t(lang, "menu_driver_vacancies")), KeyboardButton(text=t(lang, "menu_driver_buy"))],
            [KeyboardButton(text="📊 " + t(lang, "stats"))],
            [KeyboardButton(text="🌐 " + t(lang, "change_language"))],
            [KeyboardButton(text=t(lang, "deactivate_form")), KeyboardButton(text=t(lang, "activate_form_paid"))]
        ]
        await message.answer(f"{t(lang, 'setup_complete')}\n{t(lang, 'menu_driver')}", reply_markup=kb)

    elif role == "company":
        kb.keyboard = [
            [KeyboardButton(text=t(lang, "menu_company_register"))],
            [KeyboardButton(text="📊 " + t(lang, "stats"))],
            [KeyboardButton(text="🌐 " + t(lang, "change_language"))]
        ]
        await message.answer(f"{t(lang, 'setup_complete')}\n{t(lang, 'menu_company')}", reply_markup=kb)

    elif role == "manager":
        kb.keyboard = [
            [KeyboardButton(text=t(lang, "menu_manager_register"))],
            [KeyboardButton(text=t(lang, "menu_driver_buy"))],
            [KeyboardButton(text="📊 " + t(lang, "stats"))],
            [KeyboardButton(text="🌐 " + t(lang, "change_language"))]
        ]
        await message.answer(f"{t(lang, 'setup_complete')}\n{t(lang, 'menu_manager')}", reply_markup=kb)
