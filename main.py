import asyncio
import os
import asyncpg
from contextlib import asynccontextmanager
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from keyboards import main_menu  # Импорт клавиатуры

# Чтение токена и базового URL из переменных окружения
TOKEN = os.getenv("BOT_TOKEN")  # <-- Лучше использовать переменные окружения
WEBHOOK_PATH = f"/webhook/{TOKEN}"
BASE_WEBHOOK_URL = os.getenv("WEBHOOK_BASE_URL")
WEBHOOK_URL = f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"

# Создание бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ===== Хэндлеры =====

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer(
        "Добро пожаловать в JobJet AI!\nВыберите раздел:",
        reply_markup=main_menu
    )

# ===== Webhook события =====

@asynccontextmanager
async def lifespan(app):
    db_url = os.getenv("DATABASE_URL")
    pool = await asyncpg.create_pool(dsn=db_url)
    await create_tables(pool)
    app['db'] = pool
    yield
    await pool.close()

async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()

# ===== Создание таблиц =====

async def create_tables(pool):
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE,
                username TEXT,
                full_name TEXT,
                role TEXT DEFAULT 'driver',
                is_premium BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)

# ===== Запуск приложения =====

def create_app():
    app = web.Application()  # Убираем lifespan отсюда (используем cleanup_ctx ниже)
    app["bot"] = bot

    app.cleanup_ctx.append(lifespan)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    app.router.add_get("/", lambda _: web.Response(text="JobJet AI Bot работает!"))

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    return app

if __name__ == "__main__":
    web.run_app(create_app(), port=int(os.getenv("PORT", 8000)))
