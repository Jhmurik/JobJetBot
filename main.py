import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault, MenuButtonCommands
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.exceptions import TelegramAPIError
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# 📦 Импорт роутеров
from handlers.start import router as start_router
from handlers.driver_form import router as driver_form_router
from handlers.driver_form_fill import router as driver_form_fill_router
from handlers.stats import router as stats_router
from handlers.manager_register import router as manager_router
from handlers.company_register import router as company_router
from handlers.payment_button import router as payment_router
from handlers.cryptomus_webhook import cryptomus_webhook
from handlers.vacancy_publish import router as vacancy_router
from handlers.vacancy_manage import router as vacancy_manage_router
from handlers.profile import router as profile_router
from handlers.vacancy_carousel import router as vacancy_carousel_router
from handlers.company_profile import router as company_profile_router
from handlers.responses_view import router as responses_router

# 🔌 База данных
from db import connect_to_db

# 🔐 Настройки
TOKEN = os.getenv("BOT_TOKEN", "ТВОЙ_ТОКЕН_ЗДЕСЬ")
BASE_WEBHOOK_URL = os.getenv("WEBHOOK_BASE_URL", "https://jobjetbot.onrender.com")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"

# 🤖 Бот и диспетчер
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

# 🔁 Подключение роутеров
dp.include_router(start_router)
dp.include_router(driver_form_router)
dp.include_router(driver_form_fill_router)
dp.include_router(stats_router)
dp.include_router(manager_router)
dp.include_router(company_router)
dp.include_router(payment_router)
dp.include_router(vacancy_router)
dp.include_router(vacancy_manage_router)
dp.include_router(profile_router)
dp.include_router(vacancy_carousel_router)
dp.include_router(company_profile_router)
dp.include_router(responses_router)

# 🚀 Запуск Webhook
async def on_startup(app: web.Application):
    print("🚀 JobJet AI: запуск...")

    try:
        await bot.set_webhook(
            url=WEBHOOK_URL,
            drop_pending_updates=True,
            allowed_updates=dp.resolve_used_update_types()
        )
        print(f"✅ Webhook установлен: {WEBHOOK_URL}")
    except TelegramAPIError as e:
        print(f"❌ Ошибка установки Webhook: {e}")

    try:
        app["db"] = await connect_to_db()
        print("✅ Подключение к базе данных успешно")
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")

    bot._ctx = {"application": app}

    await bot.set_my_commands([
        BotCommand(command="start", description="🔁 Перезапуск бота"),
        BotCommand(command="stats", description="📊 Статистика")
    ], scope=BotCommandScopeDefault())

    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())

# 🛑 Завершение
async def on_shutdown(app: web.Application):
    print("🛑 JobJet AI: остановка...")
    await bot.delete_webhook()
    await bot.session.close()

# 🌍 Приложение Webhook
def create_webhook_app():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    # ⚠️ Ключевой момент: включаем обработку callback_query
    SimpleRequestHandler(dispatcher=dp, bot=bot, handle_callback_query=True).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    app.add_routes(cryptomus_webhook)
    return app

# ▶️ Точка входа
if __name__ == "__main__":
    mode = os.getenv("MODE", "webhook")

    if mode == "polling":
        from aiogram import executor

        async def polling_startup(dp):
            print("🔁 Polling-режим запускается...")
            await connect_to_db()
            await bot.delete_webhook()
            await bot.set_my_commands([
                BotCommand(command="start", description="🔁 Перезапуск бота"),
                BotCommand(command="stats", description="📊 Статистика")
            ])
            await bot.set_chat_menu_button(menu_button=MenuButtonCommands())

        executor.start_polling(dp, skip_updates=True, on_startup=polling_startup)
    else:
        print("🌐 Запуск через Webhook...")
        web.run_app(create_webhook_app(), host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
