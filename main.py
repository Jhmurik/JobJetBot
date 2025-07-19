import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault, MenuButtonCommands
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.exceptions import TelegramAPIError

# Роутеры
from handlers.start import router as start_router
from handlers.driver_form import router as driver_form_router
from handlers.driver_form_fill import router as driver_form_fill_router
from handlers.stats import router as stats_router
# (Добавить при готовности)
# from handlers.company import router as company_router
# from handlers.manager import router as manager_router

# БД
from db import connect_to_db

# Настройки
TOKEN = os.getenv("BOT_TOKEN", "ТВОЙ_ТОКЕН_ЗДЕСЬ")
BASE_WEBHOOK_URL = os.getenv("WEBHOOK_BASE_URL", "https://jobjetbot.onrender.com")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Роутеры
dp.include_router(start_router)
dp.include_router(driver_form_router)
dp.include_router(driver_form_fill_router)
dp.include_router(stats_router)
# dp.include_router(company_router)
# dp.include_router(manager_router)

# Старт
async def on_startup(app: web.Application):
    print("🚀 Старт JobJet AI Bot")

    try:
        await bot.set_webhook(
            url=WEBHOOK_URL,
            drop_pending_updates=True,
            allowed_updates=dp.resolve_used_update_types()
        )
        print(f"✅ Webhook установлен: {WEBHOOK_URL}")
    except TelegramAPIError as e:
        print(f"❌ Webhook ошибка: {e}")

    try:
        app["db"] = await connect_to_db()
        print("✅ База данных подключена")
    except Exception as e:
        print(f"❌ Ошибка БД: {e}")

    bot._ctx = {"application": app}

    await bot.set_my_commands([
        BotCommand(command="start", description="🔁 Перезапуск бота"),
        BotCommand(command="stats", description="📊 Статистика")
    ], scope=BotCommandScopeDefault())
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())

# Остановка
async def on_shutdown(app: web.Application):
    print("🛑 Завершение работы JobJet AI Bot...")
    await bot.delete_webhook()
    await bot.session.close()

# Webhook App
def create_webhook_app():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    return app

# Запуск
if __name__ == "__main__":
    mode = os.getenv("MODE", "webhook")

    if mode == "polling":
        from aiogram import executor

        async def polling_startup(dp):
            await connect_to_db()
            await bot.delete_webhook()
            await bot.set_my_commands([
                BotCommand(command="start", description="🔁 Перезапуск бота"),
                BotCommand(command="stats", description="📊 Статистика")
            ])
            await bot.set_chat_menu_button(menu_button=MenuButtonCommands())

        print("🔁 Запуск в режиме Polling...")
        executor.start_polling(dp, skip_updates=True, on_startup=polling_startup)
    else:
        print("🌐 Запуск через Webhook...")
        web.run_app(create_webhook_app(), host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
