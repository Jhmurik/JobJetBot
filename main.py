import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault, MenuButtonCommands
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.exceptions import TelegramAPIError

# Импорт роутеров
from handlers.start import router as start_router
from handlers.driver_form import router as driver_form_router
from handlers.stats import router as stats_router

# Импорт подключения к БД
from db import connect_to_db

# Токен и Webhook
TOKEN = "7883161984:AAF_T1IMahf_EYS42limVzfW-5NGuyNu0Qk"
BASE_WEBHOOK_URL = "https://jobjetbot.onrender.com"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Подключаем роутеры
dp.include_router(start_router)
dp.include_router(driver_form_router)
dp.include_router(stats_router)

async def on_startup(app: web.Application):
    print("🚀 Запуск JobJet AI Bot...")
    
    # Для Render лучше использовать Long Polling
    # Но если нужен Webhook:
    try:
        print(f"🔄 Установка Webhook: {WEBHOOK_URL}")
        await bot.set_webhook(
            url=WEBHOOK_URL,
            drop_pending_updates=True,
            allowed_updates=dp.resolve_used_update_types()
        )
        print("✅ Webhook установлен")
        
    except TelegramAPIError as e:
        print(f"❌ Ошибка Telegram API: {e}")
        # Переключаемся на Long Polling при ошибке
        print("🔄 Переключаемся на Long Polling режим")
        await bot.delete_webhook()
        executor.start_polling(dp, skip_updates=True)
        return

    # База данных
    try:
        app["db"] = await connect_to_db()
        print("✅ База подключена")
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")

    # Команды бота
    try:
        await bot.set_my_commands([
            BotCommand(command="start", description="Запуск бота"),
            BotCommand(command="stats", description="Показать статистику")
        ], scope=BotCommandScopeDefault())
        
        await bot.set_chat_menu_button(menu_button=MenuButtonCommands())
        print("📋 Команды установлены")
    except Exception as e:
        print(f"⚠️ Ошибка установки команд: {e}")

async def on_shutdown(app: web.Application):
    print("🛑 Выключение бота...")
    await bot.delete_webhook()
    await dp.storage.close()
    await bot.session.close()
    print("✅ Ресурсы освобождены")

# Точка входа для Render
def main():
    # Создаем aiohttp приложение
    app = web.Application()
    
    # Настраиваем shutdown колбэк
    app.on_shutdown.append(on_shutdown)
    
    # Регистрируем обработчик webhook
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    
    # Устанавливаем startup обработчик
    app.on_startup.append(on_startup)
    
    # Настраиваем aiohttp приложение
    setup_application(app, dp, bot=bot)
    
    # Запускаем приложение
    return app

# Для локального тестирования
if __name__ == "__main__":
    # Для локального запуска используем Long Polling
    from aiogram import executor
    print("🔁 Локальный запуск в режиме Long Polling")
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
