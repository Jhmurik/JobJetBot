from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("company"))
async def company_menu(message: Message):
    await message.answer("Добро пожаловать, работодатель!\nВы можете разместить вакансию или просмотреть отклики от водителей.")
