import asyncio
import os
import asyncpg
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from contextlib import asynccontextmanager

# Импорт маршрутов анкеты
from handlers.driver_form import router as driver_form_router

# 🔐 Токен и URL Webhook
TOKEN = "7883161984:AAF_T1IMahf_EYS42limVzfW-5NGuyNu0Qk"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
BASE_WEBHOOK_URL = os.getenv("WEBHOOK_BASE_URL")  # Пример: https://jobjetbot.onrender.com
WEBHOOK_URL = f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"

# Создание бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Хэндлер по умолчанию
@dp.message()
async def echo_handler(message: Message):
    await message.answer("Привет! Это JobJet бот. Напиши 'заполнить анкету' для начала.")

# Жизненный цикл: подключение к базе данных
@asynccontextmanager
async def lifespan(app):
    db_url = os.getenv("DATABASE_URL")  # Пример: postgres://user:pass@host:port/dbname
    pool = await asyncpg.create_pool(dsn=db_url)
    app["db"] = pool
    yield
    await pool.close()

# Установка webhook при старте
async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)

# Удаление webhook при остановке
async def on_shutdown(app: web.Application):
    await bot.delete_webhook()

# Основное приложение
def create_app():
    app = web.Application()
    app["bot"] = bot

    # Запуск/остановка вебхука
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    # Подключение маршрутов FSM
    dp.include_router(driver_form_router)

    # Webhook handler
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)

    # Проверка статуса по корневому пути
    app.router.add_get("/", lambda _: web.Response(text="JobJet AI Bot работает!"))

    return app

# Запуск приложения
if __name__ == "__main__":
    web.run_app(create_app(), port=int(os.getenv("PORT", 8000)))
