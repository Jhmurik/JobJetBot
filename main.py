import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    BotCommand, BotCommandScopeDefault, MenuButtonCommands
)
from aiogram.webhook.aiohttp_server import setup_application

# ✅ Импорт роутеров
from handlers.start import router as start_router
from handlers.driver_form import router as driver_form_router
from handlers.stats import router as stats_router # НОВОЕ: Импортируем роутер для статистики

# ✅ Импорт подключения к БД
from db import connect_to_db

# 🔐 Токен и Webhook
TOKEN = "7883161984:AAF_T1IMahf_EYS42limVzfW-5NGuyNu0Qk"
BASE_WEBHOOK_URL = "https://jobjetbot.onrender.com"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"

# 🤖 Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ✅ Подключаем роутеры
dp.include_router(start_router)
dp.include_router(driver_form_router)
dp.include_router(stats_router) # НОВОЕ: Подключаем роутер для статистики

# 🚀 Обработчик запуска
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
    app["db"] = pool # Сохраняем пул в контексте приложения aiohttp
    print("✅ База подключена")

    # Команды Telegram
    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="stats", description="Показать статистику")
    ], scope=BotCommandScopeDefault())
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())
    print("📋 Команды Telegram установлены")

# 🛑 Обработчик завершения
async def on_shutdown(app: web.Application):
    print("🛑 Завершение работы JobJet AI Bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
    if "db" in app:
        await app["db"].close()

# 🌐 Приложение aiohttp
def create_app():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    # Передаем bot и dispatcher в setup_application
    setup_application(app, dp, bot=bot)
    app.router.add_get("/", lambda _: web.Response(text="JobJet AI Bot работает!"))
    return app

# 👟 Точка входа
if __name__ == "__main__":
    print("👟 Запуск приложения через web.run_app()")
    web.run_app(create_app(), host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
    
