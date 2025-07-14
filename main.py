import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    Message, BotCommand, BotCommandScopeDefault,
    MenuButtonCommands, ReplyKeyboardMarkup, KeyboardButton
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.webhook.aiohttp_server import setup_application

from handlers.driver_form import router as driver_form_router
from db import connect_to_db
from states.driver_state import DriverForm
from utils.stats import count_drivers

# 🔐 Токен и Webhook
TOKEN = "7883161984:AAF_T1IMahf_EYS42limVzfW-5NGuyNu0Qk"
BASE_WEBHOOK_URL = "https://jobjetbot.onrender.com"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"

# 🤖 Инициализация
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(driver_form_router)

# 🌍 Поддержка языков
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

@dp.message(Command("start"))
async def handle_start(message: Message):
    print(f"👉 /start от {message.from_user.id}")
    await message.answer("🌐 Пожалуйста, выберите язык:", reply_markup=language_keyboard)

@dp.message(lambda message: message.text in translations.values())
async def select_language(message: Message):
    lang_code = next((code for code, label in translations.items() if label == message.text), None)
    if lang_code:
        user_languages[message.from_user.id] = lang_code
        await message.answer("✅ Язык сохранён. Выберите действие:", reply_markup=main_menu_keyboard)
    else:
        await message.answer("❌ Неподдерживаемый язык.")

@dp.message(lambda message: message.text == "📝 Заполнить анкету")
async def handle_driver_button(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Хорошо, давайте начнем. Введите ваше полное имя:")
    await state.set_state(DriverForm.full_name)

@dp.message(lambda message: message.text == "📦 Для компаний")
async def handle_company_button(message: Message):
    await message.answer("📦 Раздел для компаний в разработке. Ожидайте обновлений!")

@dp.message(lambda message: message.text == "🌐 Сменить язык")
async def handle_change_language(message: Message):
    await message.answer("🌐 Пожалуйста, выберите язык:", reply_markup=language_keyboard)

@dp.message(lambda message: message.text == "📊 Статистика")
async def handle_stats_button(message: Message):
    print(f"📊 Запрошена статистика от {message.from_user.id}")
    app = message.bot._ctx.get("application")
    if not app or "db" not in app:
        await message.answer("❌ Нет подключения к базе данных.")
        return
    pool = app["db"]
    total_drivers = await count_drivers(pool)
    await message.answer(f"📊 Статистика:\n\n🚚 Водителей зарегистрировано: {total_drivers}")

# 🚀 Запуск
async def on_startup(app: web.Application):
    print("🚀 Запуск JobJet AI Bot...")

    # Webhook
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)
        print(f"🔗 Webhook установлен: {WEBHOOK_URL}")
    else:
        print("✅ Webhook уже активен")

    # База данных
    pool = await connect_to_db()
    app["db"] = pool
    app["bot"] = bot
    print("✅ База подключена")

    # Команды
    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="stats", description="Показать статистику")
    ], scope=BotCommandScopeDefault())
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())
    print("📋 Команды Telegram установлены")

async def on_shutdown(app: web.Application):
    print("🛑 Завершение работы JobJet AI Bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
    if "db" in app:
        await app["db"].close()

def create_app():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    setup_application(app, dp, bot=bot)
    app.router.add_get("/", lambda _: web.Response(text="JobJet AI Bot работает!"))
    return app

if __name__ == "__main__":
    print("👟 Запуск приложения через web.run_app()")
    web.run_app(create_app(), host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
