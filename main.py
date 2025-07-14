import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault, MenuButtonCommands
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from handlers.start import router as start_router
from handlers.driver_form import router as driver_form_router
from db import connect_to_db

TOKEN = "7883161984:AAF_T1IMahf_EYS42limVzfW-5NGuyNu0Qk"
BASE_WEBHOOK_URL = "https://jobjetbot.onrender.com"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(start_router)
dp.include_router(driver_form_router)

async def on_startup(app: web.Application):
    print("🚀 Запуск JobJet AI Bot...")

    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)
        print(f"🔗 Webhook установлен: {WEBHOOK_URL}")
    else:
        print("✅ Webhook уже активен")

    pool = await connect_to_db()
    app["db"] = pool
    app["bot"] = bot
    print("✅ База подключена")

    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="stats", description="Показать статистику")
    ], scope=BotCommandScopeDefault())
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())
    print("📋 Команды Telegram установлены")

async def on_shutdown(app: web.Application):
    print("🛑 Завершение работы JobJet AI Bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
    if "db" in app:
        await app["db"].close()

def create_app():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    # ❗️Регистрация webhook POST-обработчика
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)

    # GET-запрос на корень — просто для проверки
    app.router.add_get("/", lambda _: web.Response(text="JobJet AI Bot работает!"))

    return app

if __name__ == "__main__":
    from aiohttp import web
    print("👟 Запуск приложения через web.run_app()")
    web.run_app(create_app(), host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
