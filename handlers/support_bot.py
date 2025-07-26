from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

router = Router()

SUPPORT_TEXT = (
    "📞 <b>Поддержка</b>\n\n"
    "Если у вас возникли вопросы, проблемы или предложения — напишите нам.\n"
    "Менеджер поддержки ответит в ближайшее время.\n\n"
    "🆘 Вы также можете отправить текст или скрин прямо сюда."
)

@router.message(F.text == "🆘 Поддержка")
async def support_menu(message: Message, state: FSMContext):
    await state.clear()
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Назад в меню")]],
        resize_keyboard=True
    )
    await message.answer(SUPPORT_TEXT, parse_mode="HTML", reply_markup=kb)
