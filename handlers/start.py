from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.driver_state import DriverForm

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
