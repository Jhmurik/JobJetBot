import asyncio
import os
import asyncpg
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from contextlib import asynccontextmanager

# Импорт FSM-маршрутов
from handlers.driver_form import router as driver_form_router

# 🔐 Токен и Webhook
TOKEN = "7883161984:AAF_T1IMahf_EYS42limVzfW-5NGuyNu0Qk"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
BASE_WEBHOOK_URL = os.getenv("WEBHOOK_BASE_URL")  # Пример: https://jobjetbot.onrender.com
WEBHOOK_URL = f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"

# 🎛️ Инициализация
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# 📲 Клавиатура выбора
start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Водитель")],
        [KeyboardButton(text="Компания")]
    ],
    resize_keyboard=True
)

# ✅ Хендлер /start с кнопками
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Добро пожаловать, водитель!\n"
        "Здесь вы сможете заполнить анкету, просмотреть вакансии и многое другое.",
        reply_markup=start_kb
    )

# 📩 Резервный хендлер
@dp.message()
async def echo_handler(message: Message):
    await message.answer("Привет! Это JobJet бот. Напиши 'заполнить анкету' для начала.")

# 🔄 Жизненный цикл
@asynccontextmanager
async def lifespan(app):
    db_url = os.getenv("DATABASE_URL")
    pool = await asyncpg.create_pool(dsn=db_url)
    app["db"] = pool
    yield
    await pool.close()

# 🚀 Webhook lifecycle
async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()

# 🧩 Создание приложения
def create_app():
    app = web.Application()
    app["bot"] = bot

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    dp.include_router(driver_form_router)

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    app.router.add_get("/", lambda _: web.Response(text="JobJet AI Bot работает!"))

    return app

# 🔧 Запуск
if __name__ == "__main__":
    web.run_app(create_app(), port=int(os.getenv("PORT", 8000)))
