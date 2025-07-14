# handlers/stats.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command # Добавляем импорт Command
from utils.stats import count_drivers

router = Router()

# Изменяем фильтр на Command("stats")
@router.message(Command("stats"))
async def show_stats_command(message: Message):
    # Лучше получать pool через DI или через event.bot.get()
    # Убедитесь, что 'db' был передан в контекст бота или приложения.
    # В main.py вы делали app["db"] = pool.
    # Чтобы aiogram мог его подхватить, можно либо:
    # 1. Передать его через `setup_application(app, dp, bot=bot, aiohttp_config={"db": pool_instance})`
    #    и затем получать через `message.bot.get('db')` (хотя это не стандартный путь для aiohttp app context)
    # 2. Использовать `dp["db"] = pool` в `on_startup` (если вы хотите хранить его в диспетчере)
    #    и затем получать через `message.bot.dispatcher.get("db")`
    # 3. Или использовать `message.bot.get('db_pool')` если вы установили его как `bot.set('db_pool', pool)`
    # 4. Самый надежный способ: использовать DI (Dependency Injection) для передачи pool в хендлер.

    # Давайте предположим, что вы изменили main.py, чтобы pool был доступен через message.bot.get("db_pool")
    # или что он доступен через message.bot.get("db") как вы и написали.
    # Если вы добавили его в app["db"] в main.py, то aiogram автоматически прикрепляет
    # aiohttp application object к боту, и вы можете получить его так:
    pool = message.bot.get('__APP__').get("db") # Получаем app, а из него уже "db"
    # Или, если вы передавали его в DI:
    # from aiogram.client.bot import Bot
    # async def show_stats_command(message: Message, db_pool: some_db_pool_type): # Пример с DI
    #     total_drivers = await count_drivers(db_pool)

    if not pool:
        await message.answer("❌ Ошибка: Подключение к базе данных недоступно.")
        return

    total_drivers = await count_drivers(pool)
    await message.answer(f"📊 Всего заполнено анкет: {total_drivers}")


# Обработчик для текстовых команд "статистика"
@router.message(F.text.lower() == "статистика")
async def show_stats_text(message: Message):
    # Можно просто вызвать основной обработчик
    await show_stats_command(message)
