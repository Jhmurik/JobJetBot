from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()

@router.message(F.text == "🏢 Я — компания")
async def company_entry(message: Message):
    await message.answer(
        "Пожалуйста, отправьте описание вашей вакансии или кратко напишите, кого вы ищете.",
        reply_markup=ReplyKeyboardRemove()
    )
