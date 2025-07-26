from aiogram import Router, F
from aiogram.types import Message
from asyncpg import Pool

from utils.translate import translate_text  # ✨ Подключим свою функцию перевода

router = Router()

@router.message(F.text.startswith("📨 Сообщение для "))
async def relay_message(message: Message):
    parts = message.text.split(maxsplit=3)
    if len(parts) < 4:
        await message.answer("❌ Неверный формат. Используйте:\n📨 Сообщение для ID_ПОЛУЧАТЕЛЯ ваш_текст")
        return

    _, _, target_id_raw, *msg_parts = parts
    target_id = int(target_id_raw)
    user_msg = ' '.join(msg_parts)

    user = message.from_user
    original_text = f"📩 Новое сообщение от <b>{user.full_name}</b> (ID: <code>{user.id}</code>):\n\n{user_msg}"
    
    # Перевод текста (пример: с русского на английский)
    translated_text = await translate_text(user_msg, source_lang="auto", target_lang="en")
    translated = f"\n\n🌐 Перевод:\n{translated_text}"

    try:
        await message.bot.send_message(target_id, original_text + translated, parse_mode="HTML")
        await message.answer("✅ Сообщение отправлено.")
    except Exception as e:
        await message.answer("❌ Не удалось отправить сообщение. Проверьте ID.")
