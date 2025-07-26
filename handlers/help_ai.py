from aiogram import Router, F
from aiogram.types import Message
from openai import AsyncOpenAI

router = Router()

# 🔐 Укажи свой OpenAI API-ключ
OPENAI_API_KEY = "sk-..."  # Заменить на свой ключ

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.message(F.text.lower().startswith("🤖"))
async def ai_assistant(message: Message):
    prompt = message.text.replace("🤖", "").strip()

    if not prompt:
        await message.answer("🤖 Пожалуйста, введите вопрос после эмодзи. Пример: 🤖 Как получить работу в Литве?")
        return

    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты умный помощник для водителей и логистов в Европе."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=512
        )

        reply = response.choices[0].message.content
        await message.answer(f"🤖 {reply}")

    except Exception as e:
        await message.answer("⚠️ Произошла ошибка при обращении к AI. Попробуйте позже.")
        print("AI Error:", e)
