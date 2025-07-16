import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault, MenuButtonCommands
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.exceptions import TelegramAPIError

# Импорт роутеров
from handlers.start import router as start_router
from handlers.driver_form import router as driver_form_router
from handlers.driver_form_fill import router as driver_form_fill_router  # ✅ Добавлен!
from handlers.stats import router as stats_router

# Импорт подключения к БД
from db import connect_to_db

# Токен и Webhook
TOKEN = os.getenv("BOT_TOKEN", "7883161984:AAF_T1IMahf_EYS42limVzfW-5NGuyNu0Qk")
BASE_WEBHOOK_URL = os.getenv("WEBHOOK_BASE_URL", "https://jobjetbot.onrender.com")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"

# Инициализация
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Подключаем роутеры
dp.include_router(start_router)
dp.include_router(driver_form_router)
dp.include_router(driver_form_fill_router)  # ✅ Обязательно для FSM
dp.include_router(stats_router)

# 🚀 Старт при Webhook
async def on_startup(app: web.Application):
    print("🚀 Старт JobJet AI Bot (Webhook)")

    try:
        await bot.set_webhook(
            url=WEBHOOK_URL,
            drop_pending_updates=True,
            allowed_updates=dp.resolve_used_update_types()
        )
        print(f"✅ Webhook установлен: {WEBHOOK_URL}")
    except TelegramAPIError as e:
        print(f"❌ Ошибка при установке Webhook: {e}")

    try:
        app["db"] = await connect_to_db()
        print("✅ База данных подключена")
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")

    # Важно: сохраняем ссылку на app в контексте
    bot._ctx = {"application": app}

    # Команды
    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="stats", description="Показать статистику")
    ], scope=BotCommandScopeDefault())
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())

# 🛑 Остановка
async def on_shutdown(app: web.Application):
    print("🛑 Завершение работы JobJet AI Bot...")
    await bot.delete_webhook()
    await bot.session.close()
    print("✅ Бот завершил работу")

# 🌐 Приложение Webhook
def create_webhook_app():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    return app

# 🔁 Запуск
if __name__ == "__main__":
    mode = os.getenv("MODE", "webhook")

    if mode == "polling":
        from aiogram import executor

        async def polling_startup(dp):
            await connect_to_db()
            await bot.delete_webhook()
            await bot.set_my_commands([
                BotCommand(command="start", description="Запуск бота"),
                BotCommand(command="stats", description="Показать статистику")
            ])
            await bot.set_chat_menu_button(menu_button=MenuButtonCommands())
            print("✅ Команды установлены")

        print("🔁 Локальный запуск в режиме Polling...")
        executor.start_polling(dp, skip_updates=True, on_startup=polling_startup)
    else:
        print("🌐 Запуск через Webhook...")
        web.run_app(create_webhook_app(), host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
