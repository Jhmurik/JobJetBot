from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()

@router.message(F.text == "🚛 Найти работу")
async def driver_entry(message: Message):
    await message.answer(
        "Отлично! Отправьте вашу анкету или напишите, что вы ищете:",
        reply_markup=ReplyKeyboardRemove()
    )
