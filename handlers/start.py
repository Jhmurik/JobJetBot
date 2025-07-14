from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.driver_state import DriverForm # Убедитесь, что этот импорт верный

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

# ВНИМАНИЕ: user_languages на MemoryStorage не сохраняется после перезапусков.
# Для продакшена используйте базу данных для хранения настроек пользователя.
user_languages = {}

@router.message(Command("start"))
async def handle_start(message: Message, state: FSMContext):
    print(f"👉 /start от {message.from_user.id}")
    await state.clear() # Очищаем состояние при старте, чтобы начать с чистого листа
    await message.answer("🌐 Пожалуйста, выберите язык:", reply_markup=language_keyboard)

@router.message(F.text.in_(translations.values()))
async def select_language(message: Message):
    lang_code = next((code for code, label in translations.items() if label == message.text), None)
    if lang_code:
        user_languages[message.from_user.id] = lang_code # Временно сохраняем язык
        await message.answer("✅ Язык сохранён. Выберите действие:", reply_markup=main_menu_keyboard)
    else:
        await message.answer("❌ Неподдерживаемый язык.")

# НОВОЕ: Обработчик для кнопки "📝 Заполнить анкету"
@router.message(F.text == "📝 Заполнить анкету")
async def start_fill_form_button(message: Message, state: FSMContext):
    await state.set_state(DriverForm.full_name) # Устанавливаем первое состояние формы
    await message.answer("📝 Отлично! Начнём заполнение анкеты. Пожалуйста, введите ваше *полное имя* (ФИО):", parse_mode="Markdown")

# НОВОЕ: Обработчик для кнопки "🌐 Сменить язык"
@router.message(F.text == "🌐 Сменить язык")
async def change_language_button(message: Message):
    await message.answer("🌐 Пожалуйста, выберите язык:", reply_markup=language_keyboard)

# НОВОЕ: Обработчик для кнопки "📊 Статистика" (для удобства, можно было бы и в stats.py)
@router.message(F.text == "📊 Статистика")
async def stats_button(message: Message):
    # Просто вызываем обработчик команды /stats, так как он делает то же самое
    # Важно: это требует, чтобы handle_stats был в этом же роутере или импортирован.
    # Если вы хотите, чтобы вся логика статистики была в handlers/stats.py,
    # то удалите этот обработчик и полагайтесь на router.message(Command("stats"))
    # или router.message(F.text.lower() == "статистика") из handlers/stats.py
    # В данном случае, это просто вызов команды /stats, которую обработает stats_router
    # Это может быть немного избыточно, если handlers/stats.py уже обрабатывает F.text == "статистика"
    await message.answer("Обрабатываю запрос на статистику...")
    # Можно отправить команду программно, чтобы ее обработал stats_router
    # или просто вызвать соответствующий хендлер, если он доступен
    # В данном случае, так как `stats_router` будет подключен,
    # лучше полагаться на его обработчик текста "Статистика"
    # Для этого, убедитесь, что в handlers/stats.py есть
    # @router.message(F.text.lower() == "статистика")
    # А здесь можно просто вернуть основное меню, если статистика показывается в другом месте
    # await message.answer("Запросите статистику командой /stats или из меню.", reply_markup=main_menu_keyboard)
    pass # Пустое действие, так как handlers/stats.py будет ловить "Статистика"

# НОВОЕ: Обработчик для кнопки "📦 Для компаний" (заглушка)
@router.message(F.text == "📦 Для компаний")
async def for_companies_button(message: Message):
    await message.answer("💼 Раздел для компаний в разработке. Скоро будет доступно!")
    
