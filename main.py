# main.py

import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    BotCommand, BotCommandScopeDefault, MenuButtonCommands
)
from aiogram.webhook.aiohttp_server import setup_application
from aiogram.exceptions import TelegramAPIError # НОВОЕ: Импортируем для обработки ошибок API

# ✅ Импорт роутеров
from handlers.start import router as start_router
from handlers.driver_form import router as driver_form_router
from handlers.stats import router as stats_router

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
dp.include_router(stats_router)

# 🚀 Обработчик запуска
async def on_startup(app: web.Application):
    print("🚀 Запуск JobJet AI Bot...")

    # Webhook
    try:
        current_webhook_info = await bot.get_webhook_info()
        print(f"ℹ️ Текущий Webhook: {current_webhook_info.url}")

        if current_webhook_info.url != WEBHOOK_URL:
            print(f"🔄 Установка нового Webhook: {WEBHOOK_URL}")
            await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True) # НОВОЕ: drop_pending_updates=True
            print(f"✅ Webhook успешно установлен: {WEBHOOK_URL}")
        else:
            print("✅ Webhook уже активен и корректен.")

        # Добавим дополнительную проверку после установки
        final_webhook_info = await bot.get_webhook_info()
        print(f"✅ Финальная проверка Webhook: {final_webhook_info.url}")
        if final_webhook_info.url != WEBHOOK_URL:
            print("⚠️ ВНИМАНИЕ: Webhook URL не совпадает после установки! Возможно, проблема с Telegram API.")

    except TelegramAPIError as e:
        print(f"❌ ОШИБКА TELEGRAM API ПРИ УСТАНОВКЕ WEBHOOK: {e}")
        # Вы можете решить, что делать в этом случае: либо продолжить работу без webhook,
        # либо завершить приложение, так как оно не сможет получать обновления.
        # Для начала давайте просто выведем ошибку и продолжим.
    except Exception as e:
        print(f"❌ НЕПРЕДВИДЕННАЯ ОШИБКА ПРИ УСТАНОВКЕ WEBHOOK: {e}")

    # База данных
    try:
        pool = await connect_to_db()
        app["db"] = pool
        print("✅ База подключена")
    except Exception as e:
        print(f"❌ ОШИБКА ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ: {e}")
        # Если база данных критична, можно остановить запуск
        # raise # Для отладки

    # Команды Telegram
    try:
        await bot.set_my_commands([
            BotCommand(command="start", description="Запуск бота"),
            BotCommand(command="stats", description="Показать статистику")
        ], scope=BotCommandScopeDefault())
        await bot.set_chat_menu_button(menu_button=MenuButtonCommands())
        print("📋 Команды Telegram установлены")
    except TelegramAPIError as e:
        print(f"❌ ОШИБКА TELEGRAM API ПРИ УСТАНОВКЕ КОМАНД: {e}")
    except Exception as e:
        print(f"❌ НЕПРЕДВИДЕННАЯ ОШИБКА ПРИ УСТАНОВКЕ КОМАНД: {e}")


# 🛑 Обработчик завершения
async def on_shutdown(app: web.Application):
    print("🛑 Завершение работы JobJet AI Bot...")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        print("✅ Webhook успешно удален при завершении.")
    except TelegramAPIError as e:
        print(f"❌ ОШИБКА TELEGRAM API ПРИ УДАЛЕНИИ WEBHOOK: {e}")
    except Exception as e:
        print(f"❌ НЕПРЕДВИДЕННАЯ ОШИБКА ПРИ УДАЛЕНИИ WEBHOOK: {e}")

    await bot.session.close()
    if "db" in app:
        await app["db"].close()

# 🌐 Приложение aiohttp
def create_app():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    setup_application(app, dp, bot=bot)
    app.router.add_get("/", lambda _: web.Response(text="JobJet AI Bot работает!"))
    return app

# 👟 Точка входа
if __name__ == "__main__":
    print("👟 Запуск приложения через web.run_app()")
    web.run_app(create_app(), host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

