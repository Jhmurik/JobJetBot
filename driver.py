from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("driver"))
async def driver_menu(message: Message):
    await message.answer("Добро пожаловать, водитель!\nЗдесь вы сможете заполнить анкету, просмотреть вакансии и многое другое.")
