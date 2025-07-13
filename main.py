import os
import asyncpg
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, BotCommand, BotCommandScopeDefault, MenuButtonCommands
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from contextlib import asynccontextmanager

# Импорт анкеты водителя
from handlers.driver_form import router as driver_form_router

# 🔐 Токен и Webhook
TOKEN = "7883161984:AAF_T1IMahf_EYS42limVzfW-5NGuyNu0Qk"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
BASE_WEBHOOK_URL = os.getenv("WEBHOOK_BASE_URL")  # Например: https://jobjetbot.onrender.com
WEBHOOK_URL = f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"

# Бот и хранилище
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# 👋 Хэндлер на любое сообщение (по умолчанию)
@dp.message(F.text.lower().in_({"заполнить анкету", "анкета", "start"}))
async def handle_form_request(message: Message):
    await message.answer("Привет! Нажмите /driver для заполнения анкеты водителя.")

@dp.message()
async def fallback(message: Message):
    await message.answer("Привет! Это JobJet AI Бот. Напишите 'заполнить анкету' или нажмите кнопку в меню.")

# 📦 Подключение к БД
@asynccontextmanager
async def lifespan(app):
    db_url = os.getenv("DATABASE_URL")
    pool = await asyncpg.create_pool(dsn=db_url)
    app["db"] = pool
    yield
    await pool.close()

# 🚀 При запуске
async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)

    # Установка команд
    commands = [
        BotCommand(command="start", description="Главное меню"),
        BotCommand(command="driver", description="Анкета водителя"),
        BotCommand(command="company", description="Анкета для компаний")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())

# 🛑 При остановке
async def on_shutdown(app: web.Application):
    await bot.delete_webhook()

# 🔧 Приложение aiohttp
def create_app():
    app = web.Application()
    app["bot"] = bot

    dp.include_router(driver_form_router)

    # Подключение событий и webhook
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    # 👇 Вебхук-обработчик
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
