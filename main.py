import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from keyboards import main_menu

# Импорт роутеров
from драйвер import router as driver_router
from company import router as company_router

# ВСТАВЛЕННЫЙ ТОКЕН И URL
TOKEN = "7883161984:AAF_T1IMahf_EYS42limVzfW-5NGuyNu0Qk"
BASE_WEBHOOK_URL = os.getenv("WEBHOOK_BASE_URL")  # Например: https://jobjetbot.onrender.com
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Хендлер /start
@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Добро пожаловать в JobJet AI Bot!", reply_markup=main_menu)

# Подключаем роутеры
dp.include_router(driver_router)
dp.include_router(company_router)

# Установка и удаление webhook
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app):
    await bot.delete_webhook()

# Создание и запуск aiohttp-приложения
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
