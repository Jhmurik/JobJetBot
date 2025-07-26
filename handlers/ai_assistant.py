from aiogram import Router, F
from aiogram.types import Message
from openai import AsyncOpenAI
import os

router = Router()

# ✅ Команда: AI-помощник (GPT)
@router.message(F.text.lower().startswith("🤖 помощник") | F.text.lower().startswith("/ask"))
async def ask_ai(message: Message):
    query = message.text.replace("🤖 помощник", "").replace("/ask", "").strip()

    if not query:
        await message.answer("✍️ Пожалуйста, напишите ваш вопрос после команды.")
        return

    # 🔑 Ключ OpenAI из переменной окружения
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        await message.answer("❌ OpenAI API не подключён.")
        return

    client = AsyncOpenAI(api_key=openai_api_key)

    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты AI-помощник для водителей и логистических компаний."},
                {"role": "user", "content": query}
            ],
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        await message.answer(reply)
    except Exception as e:
        await message.answer("⚠️ Ошибка AI: " + str(e))
