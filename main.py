import os
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    Message, BotCommand, BotCommandScopeDefault,
    MenuButtonCommands, ReplyKeyboardMarkup, KeyboardButton
)
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

from handlers.driver_form import router as driver_form_router
from db import connect_to_db
from aiogram.fsm.context import FSMContext
from states.driver_state import DriverForm
from utils.stats import count_drivers

# 🔐 Новый Telegram Token
TOKEN = "5887286839:AAGmZXbLyFQ9BYWVKvCq1OHPa9ECrhN1GJQ"  # ← ВСТАВЛЕН новый рабочий токен

BASE_WEBHOOK_URL = "https://jobjetbot.onrender.com"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"

# 🤖 Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(driver_form_router)

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

# 📋 Главное меню
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Заполнить анкету")],
        [KeyboardButton(text="📦 Для компаний")],
        [KeyboardButton(text="🌐 Сменить язык")],
        [KeyboardButton(text="📊 Статистика")]
    ],
    resize_keyboard=True
)

# 🧠 Память языка
user_languages = {}

@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("🌐 Пожалуйста, выберите язык:", reply_markup=language_keyboard)

@dp.message(F.text.in_(translations.values()))
async def select_language(message: Message):
    lang_code = [code for code, label in translations.items() if label == message.text]
    if lang_code:
        user_languages[message.from_user.id] = lang_code[0]
        await message.answer("✅ Язык сохранён. Выберите действие:", reply_markup=main_menu_keyboard)
    else:
        await message.answer("❌ Неподдерживаемый язык.")

@dp.message(F.text == "📝 Заполнить анкету")
async def handle_driver_button(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Хорошо, давайте начнем. Введите ваше полное имя:")
    await state.set_state(DriverForm.full_name)

@dp.message(F.text == "📦 Для компаний")
async def handle_company_button(message: Message):
    await message.answer("📦 Раздел для компаний в разработке. Ожидайте обновлений!")

@dp.message(F.text == "🌐 Сменить язык")
async def handle_change_language(message: Message):
    await message.answer("🌐 Пожалуйста, выберите язык:", reply_markup=language_keyboard)

@dp.message(F.text == "📊 Статистика")
async def handle_stats_button(message: Message):
    pool = message.bot.get("db")
    if not pool:
        await message.answer("❌ Нет подключения к базе данных.")
        return
    total = await count_drivers(pool)
    await message.answer(f"📊 Всего заполнено анкет: {total}")

async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)
    pool = await connect_to_db()
    app["db"] = pool
    commands = [
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="stats", description="Статистика анкет")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    if "db" in app:
        await app["db"].close()

def create_app():
    app = web.Application()
    app["bot"] = bot
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    app.router.add_get("/", lambda _: web.Response(text="JobJet AI Bot работает!"))
    return app

if __name__ == "__main__":
    web.run_app(create_app(), port=int(os.getenv("PORT", 8000)))
