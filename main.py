import asyncio
import os
import asyncpg
from contextlib import asynccontextmanager
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

# Чтение токена и базового URL из переменных окружения
TOKEN = "7883161984:AAF_T1IMahf_EYS42limVzfW-5NGuyNu0Qk"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
BASE_WEBHOOK_URL = os.getenv("WEBHOOK_BASE_URL")
WEBHOOK_URL = f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"

# Создание бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@asynccontextmanager
async def lifespan(app):
    db_url = os.getenv("DATABASE_URL")
    pool = await asyncpg.create_pool(dsn=db_url)
    await create_tables(pool)
    app['db'] = pool
    yield
    await pool.close()
    
# Хэндлер на входящее сообщение
@dp.message()
async def echo_handler(message: Message):
    await message.answer("Привет! Это JobJet бот.")

# Установка webhook при запуске
async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)

# Удаление webhook при завершении
async def on_shutdown(app: web.Application):
    await bot.delete_webhook()

def create_app():
    app = web.Application(lifespan=lifespan)  # 🔧 lifespan добавлен сюда
    app["bot"] = bot

    # Устанавливаем хуки запуска и завершения
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    app.router.add_get("/", lambda _: web.Response(text="JobJet AI Bot работает!"))

    return app
    
    # 👇 добавляем подключение к базе данных через жизненный цикл
    app.cleanup_ctx.append(lifespan)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    app.router.add_get("/", lambda _: web.Response(text="JobJet AI is working"))
    return app

# Запуск приложения
if __name__ == "__main__":
    web.run_app(create_app(), port=int(os.getenv("PORT", 8000)))
