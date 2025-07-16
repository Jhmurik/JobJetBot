from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.driver_state import DriverForm
from db import deactivate_driver, activate_driver
from asyncpg import Pool

router = Router()

# 🌍 Языки
translations = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "uz": "🇺🇿 Oʻzbek",
    "uk": "🇺🇦 Українська",
    "hi": "🇮🇳 हिन्दी",
    "pl": "🇵🇱 Polski"
}

language_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=lang)] for lang in translations.values()],
    resize_keyboard=True,
    one_time_keyboard=True
)

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Заполнить анкету")],
        [KeyboardButton(text="📦 Для компаний")],
        [KeyboardButton(text="🌐 Сменить язык")],
        [KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="🚫 Выключить анкету")],
        [KeyboardButton(text="✅ Включить анкету (платно)")]
    ],
    resize_keyboard=True
)

user_languages = {}

# 🔘 /start
@router.message(Command("start"))
async def handle_start(message: Message, state: FSMContext):
    print(f"👉 /start от {message.from_user.id}")
    await state.clear()
    await message.answer("🌐 Пожалуйста, выберите язык:", reply_markup=language_keyboard)

# 🌐 Выбор языка
@router.message(F.text.in_(translations.values()))
async def select_language(message: Message):
    lang_code = next((code for code, label in translations.items() if label == message.text), None)
    if lang_code:
        user_languages[message.from_user.id] = lang_code
        await message.answer("✅ Язык сохранён. Выберите действие:", reply_markup=main_menu_keyboard)
    else:
        await message.answer("❌ Неподдерживаемый язык.")

# 📝 Заполнить анкету
@router.message(F.text == "📝 Заполнить анкету")
async def start_fill_form_button(message: Message, state: FSMContext):
    await state.set_state(DriverForm.full_name)
    await message.answer("📝 Отлично! Начнём заполнение анкеты. Введите ваше *полное имя* (ФИО):", parse_mode="Markdown")

# 🌐 Сменить язык
@router.message(F.text == "🌐 Сменить язык")
async def change_language_button(message: Message):
    await message.answer("🌐 Пожалуйста, выберите язык:", reply_markup=language_keyboard)

# 📊 Статистика (заглушка)
@router.message(F.text == "📊 Статистика")
async def stats_button(message: Message):
    await message.answer("📊 Раздел статистики скоро будет активен.")

# 📦 Для компаний
@router.message(F.text == "📦 Для компаний")
async def for_companies_button(message: Message):
    await message.answer("💼 Раздел для компаний в разработке. Скоро будет доступен!")

# 🚫 Выключить анкету
@router.message(F.text == "🚫 Выключить анкету")
async def deactivate_profile(message: Message):
    app = message.bot._ctx.get("application")
    if not app or "db" not in app:
        await message.answer("❌ База данных недоступна.")
        return

    pool: Pool = app["db"]
    driver_id = message.from_user.id

    async with pool.acquire() as conn:
        await deactivate_driver(conn, driver_id)

    await message.answer("🛑 Ваша анкета временно отключена.")

# ✅ Включить анкету (платно)
@router.message(F.text == "✅ Включить анкету (платно)")
async def activate_profile(message: Message):
    app = message.bot._ctx.get("application")
    if not app or "db" not in app:
        await message.answer("❌ База данных недоступна.")
        return

    pool: Pool = app["db"]
    driver_id = message.from_user.id

    # ❗ Позже сюда добавим проверку оплаты
    async with pool.acquire() as conn:
        await activate_driver(conn, driver_id)

    await message.answer("✅ Ваша анкета снова активна и доступна для компаний.")
