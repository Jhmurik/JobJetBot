import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, BotCommand, BotCommandScopeDefault, MenuButtonCommands
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

# 📥 Импорт маршрутов и подключения к БД
from handlers.driver_form import router as driver_form_router
from db import connect_to_db

# 🔐 Токен и Webhook настройки (токен вставлен вручную)
TOKEN = "7883161984:AAF_T1IMahf_EYS42limVzfW-5NGuyNu0Qk"
BASE_WEBHOOK_URL = "https://jobjetbot.onrender.com"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"

# 🤖 Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ✅ Подключение маршрутов (FSM логика анкеты водителя)
dp.include_router(driver_form_router)

# 🔹 Команда /start
@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("Привет! Это JobJet AI Бот. Напишите 'заполнить анкету' или нажмите кнопку в меню.")

# 🔹 Команда /company
@dp.message(Command("company"))
async def handle_company(message: Message):
    await message.answer("Раздел для компаний в разработке. Ожидайте обновлений!")

# ❗ Обработка всех прочих сообщений
@dp.message()
async def fallback(message: Message):
    await message.answer("Привет! Это JobJet AI Бот. Напишите 'заполнить анкету' или нажмите кнопку в меню.")

# 🚀 Действия при запуске
async def on_startup(app: web.Application):
    # Установка webhook
    await bot.set_webhook(WEBHOOK_URL)

    # Подключение к базе данных
    pool = await connect_to_db()
    app["db"] = pool

    # Настройка команд в меню
    commands = [
        BotCommand(command="start", description="Главное меню"),
        BotCommand(command="driver", description="Анкета водителя"),
        BotCommand(command="company", description="Анкета для компаний")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())

# 🛑 Завершение работы
async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    if "db" in app:
        await app["db"].close()

# 👷 Создание aiohttp-приложения
def create_app():
    app = web.Application()
    app["bot"] = bot

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    # Обработчик webhook-запросов
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)

    # Страница для проверки статуса
    app.router.add_get("/", lambda _: web.Response(text="JobJet AI Bot работает!"))

    return app

# 🔁 Запуск приложения
if __name__ == "__main__":
    web.run_app(create_app(), port=int(os.getenv("PORT", 8000)))
