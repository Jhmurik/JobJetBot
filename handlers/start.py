from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.driver_state import DriverForm
from utils.stats import count_drivers

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
        [KeyboardButton(text="📊 Статистика")]
    ],
    resize_keyboard=True
)

user_languages = {}

@router.message(Command("start"))
async def handle_start(message: Message):
    print(f"👉 /start от {message.from_user.id}")
    await message.answer("🌐 Пожалуйста, выберите язык:", reply_markup=language_keyboard)

@router.message(F.text.in_(translations.values()))
async def select_language(message: Message):
    lang_code = next((code for code, label in translations.items() if label == message.text), None)
    if lang_code:
        user_languages[message.from_user.id] = lang_code
        await message.answer("✅ Язык сохранён. Выберите действие:", reply_markup=main_menu_keyboard)
    else:
        await message.answer("❌ Неподдерживаемый язык.")

@router.message(F.text == "📝 Заполнить анкету")
async def handle_driver_button(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Хорошо, давайте начнем. Введите ваше полное имя:")
    await state.set_state(DriverForm.full_name)

@router.message(F.text == "📦 Для компаний")
async def handle_company_button(message: Message):
    await message.answer("📦 Раздел для компаний в разработке. Ожидайте обновлений!")

@router.message(F.text == "🌐 Сменить язык")
async def handle_change_language(message: Message):
    await message.answer("🌐 Пожалуйста, выберите язык:", reply_markup=language_keyboard)

@router.message(F.text == "📊 Статистика")
async def handle_stats_button(message: Message):
    print(f"📊 Запрошена статистика от {message.from_user.id}")
    app = message.bot._ctx.get("application")
    if not app or "db" not in app:
        await message.answer("❌ Нет подключения к базе данных.")
        return
    pool = app["db"]
    total_drivers = await count_drivers(pool)
    await message.answer(f"📊 Статистика:\n\n🚚 Водителей зарегистрировано: {total_drivers}")
