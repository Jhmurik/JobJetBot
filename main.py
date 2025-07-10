import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
import os

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    await message.reply("👋 Привет! Это JobJet AI — бот для поиска работы водителем и найма сотрудников для логистических компаний.")

@dp.message_handler()
async def echo(message: Message):
    await message.reply("Напиши /start, чтобы начать 🚀")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
