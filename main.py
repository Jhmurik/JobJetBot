import os
from aiohttp import web
import asyncpg
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, BotCommand, BotCommandScopeDefault, MenuButtonCommands
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

# Импорт анкеты водителя и подключения к БД
from handlers.driver_form import router as driver_form_router
from db import connect_to_db

# 🔐 Токен и Webhook
TOKEN = "7883161984:AAF_T1IMahf_EYS42limVzfW-5NGuyNu0Qk"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
BASE_WEBHOOK_URL = os.getenv("WEBHOOK_BASE_URL")  # https://jobjetbot.onrender.com
WEBHOOK_URL = f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# 🤖 Обработка сообщений
@dp.message(F.text.lower().in_({"заполнить анкету", "анкета", "start"}))
async def handle_form_request(message: Message):
    await message.answer("Привет! Нажмите /driver для заполнения анкеты водителя.")

@dp.message()
async def fallback(message: Message):
    await message.answer("Привет! Это JobJet AI Бот. Напишите 'заполнить анкету' или нажмите кнопку в меню.")

# 🚀 При запуске
async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)

    # ✅ Подключение к БД
    pool = await connect_to_db()
    app["db"] = pool

    # Команды и меню
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
    if "db" in app:
        await app["db"].close()

# 👷 Создание приложения
def create_app():
    app = web.Application()
    app["bot"] = bot

    dp.include_router(driver_form_router)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    app.router.add_get("/", lambda _: web.Response(text="JobJet AI Bot работает!"))

    return app

# 🔁 Запуск
if __name__ == "__main__":
    web.run_app(create_app(), port=int(os.getenv("PORT", 8000)))
