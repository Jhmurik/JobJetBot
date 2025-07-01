import os
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv

# Загружаем переменные из .env (если используешь)
load_dotenv()

# Получаем токен бота из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Команда /start
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.answer("Добро пожаловать в JobJet AI!\n\nЯ помогу вам найти работу дальнобойщиком в Европе 🚛")

# Команда /help
@dp.message_handler(commands=["help"])
async def send_help(message: types.Message):
    await message.answer("Если вам нужна помощь — напишите сюда.\n\nСкоро появится больше функций!")

# Заглушка на все остальные сообщения
@dp.message_handler()
async def handle_all(message: types.Message):
    await message.answer("Пожалуйста, используйте кнопки или команды. Напишите /start для начала.")

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
