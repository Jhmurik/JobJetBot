import os
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    Message, BotCommand, BotCommandScopeDefault,
    MenuButtonCommands, ReplyKeyboardMarkup, KeyboardButton
)
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import setup_application

from handlers.driver_form import router as driver_form_router
from db import connect_to_db
from aiogram.fsm.context import FSMContext
from states.driver_state import DriverForm
from utils.stats import count_drivers

# 🔐 Токен и Webhook
TOKEN = os.getenv("BOT_TOKEN", "7883161984:AAF_T1IMahf_EYS42limVzfW-5NGuyNu0Qk")
BASE_WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://jobjetbot.onrender.com")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"

# 🤖 Инициализация
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
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

user_languages = {}

# 🔹 Команды
@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("🌐 Пожалуйста, выберите язык:", reply_markup=language_keyboard)

@dp.message(F.text.in_(translations.values()))
async def select_language(message: Message):
    lang_code = next((code for code, label in translations.items() if label == message.text), None)
    if lang_code:
        user_languages[message.from_user.id] = lang_code
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
    pool = bot.get("db")
    if not pool:
        await message.answer("❌ Нет подключения к базе данных.")
        return
    total_drivers = await count_drivers(pool)
    await message.answer(f"📊 Статистика:\n\n🚚 Водителей зарегистрировано: {total_drivers}")

# 🚀 Запуск
async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)  # ✅ Telegram будет знать куда отправлять запросы
    pool = await connect_to_db()
    app["db"] = pool
    bot["db"] = pool

    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="stats", description="Статистика")
    ], scope=BotCommandScopeDefault())

    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())

async def on_shutdown(app: web.Application):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
    if "db" in app:
        await app["db"].close()

# 👷 Приложение
def create_app():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    setup_application(app, dp, bot=bot, path=WEBHOOK_PATH)  # ✅ Обрабатывает только путь с токеном
    app.router.add_get("/", lambda _: web.Response(text="JobJet AI Bot работает!"))
    return app

# 🔁 Запуск
if __name__ == "__main__":
    web.run_app(create_app(), port=int(os.getenv("PORT", 8000)))
