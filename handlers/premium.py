from aiogram import Router, F
from aiogram.types import Message
from utils.payments import create_payment_link

router = Router()

@router.message(F.text == "💳 Купить подписку")
async def handle_buy_premium(message: Message):
    link = await create_payment_link(
        user_id=message.from_user.id,
        role="driver",
        amount=3.0,
        payment_type="premium"
    )
    await message.answer(f"💰 Для активации Premium перейдите по ссылке:\n\n👉 {link}")
