# main.py (ОБНОВЛЕННЫЙ БЛОК on_startup)

import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    BotCommand, BotCommandScopeDefault, MenuButtonCommands
)
from aiogram.webhook.aiohttp_server import setup_application
from aiogram.exceptions import TelegramAPIError # Импортируем для обработки ошибок API

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
        print(f"🔄 Попытка установки Webhook: {WEBHOOK_URL}")
        # ВСЕГДА УСТАНАВЛИВАЕМ WEBHOOK ПРИ ЗАПУСКЕ
        await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
        print(f"✅ Webhook успешно установлен: {WEBHOOK_URL}")

        # Добавим дополнительную проверку после установки
        final_webhook_info = await bot.get_webhook_info()
        print(f"✅ Финальная проверка Webhook (получено из Telegram): {final_webhook_info.url}")
        if final_webhook_info.url == WEBHOOK_URL:
            print("🎉 Webhook URL подтвержден и совпадает!")
        else:
            print(f"⚠️ ВНИМАНИЕ: Webhook URL не совпадает после установки! Ожидалось: {WEBHOOK_URL}, Получено: {final_webhook_info.url}")
            print("Это может быть временная проблема с Telegram API или некорректная настройка.")

    except TelegramAPIError as e:
        print(f"❌ ОШИБКА TELEGRAM API ПРИ УСТАНОВКЕ WEBHOOK: {e}")
        print("Бот не сможет получать обновления без рабочего webhook.")
    except Exception as e:
        print(f"❌ НЕПРЕДВИДЕННАЯ ОШИБКА ПРИ УСТАНОВКЕ WEBHOOK: {e}")

    # База данных (ваш код остается без изменений)
    try:
        pool = await connect_to_db()
        app["db"] = pool
        print("✅ База подключена")
    except Exception as e:
        print(f"❌ ОШИБКА ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ: {e}")

    # Команды Telegram (ваш код остается без изменений)
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

# ... Остальной код main.py без изменений ...

