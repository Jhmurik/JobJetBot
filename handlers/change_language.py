from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.start_kb import get_language_keyboard
from utils.i18n import t
from asyncpg import Pool

router = Router()

# 🌐 Кнопка "Сменить язык"
@router.message(F.text == "🌐 Сменить язык")
async def change_language(message: Message, state: FSMContext):
    await message.answer("🌍 Пожалуйста, выберите язык:", reply_markup=get_language_keyboard())

# 🔘 Выбор нового языка
@router.callback_query(F.data.startswith("lang_"))
async def set_new_language(callback: CallbackQuery, state: FSMContext):
    new_lang = callback.data.split("_")[1]
    user_id = callback.from_user.id
    app = callback.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        # Попытка обновить язык у водителя
        updated_driver = await conn.execute("UPDATE drivers SET languages = ARRAY[$1] WHERE id = $2", new_lang, user_id)

        # Если не водитель, попробуем менеджера
        if updated_driver == "UPDATE 0":
            await conn.execute("UPDATE managers SET languages = ARRAY[$1] WHERE user_id = $2", new_lang, user_id)

    await callback.message.edit_text(t(new_lang, "language_changed_successfully"))
    await state.clear()
