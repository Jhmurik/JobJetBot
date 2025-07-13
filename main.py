import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, BotCommand, BotCommandScopeDefault, MenuButtonCommands, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, Text
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from handlers.driver_form import router as driver_form_router
from db import connect_to_db

# 🔐 Токен и Webhook
TOKEN = "7883161984:AAF_T1IMahf_EYS42limVzfW-5NGuyNu0Qk"
BASE_WEBHOOK_URL = "https://jobjetbot.onrender.com"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"

# 🤖 Бот и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ✅ Роутеры
dp.include_router(driver_form_router)

# 🌐 Переводы
translations = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "uz": "🇺🇿 Oʻzbek",
    "uk": "🇺🇦 Українська",
    "hi": "🇮🇳 हिन्दी",
    "pl": "🇵🇱 Polski"
}
language_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=lang)] for lang in translations.values()],
    resize_keyboard=True,
    one_time_keyboard=True
)

# 🌍 Хранилище выбранного языка (в реальном проекте — лучше FSM или БД)
user_languages = {}

# 🔹 Старт /start
@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer(
        "🌐 Пожалуйста, выберите язык:\n\n" + "\n".join(translations.values()),
        reply_markup=language_keyboard
    )

# 🔹 Выбор языка
@dp.message(Text(text=list(translations.values())))
async def select_language(message: Message):
    lang_code = [code for code, label in translations.items() if label == message.text]
    if lang_code:
        user_languages[message.from_user.id] = lang_code[0]
        await message.answer("✅ Язык сохранён. Напишите 'заполнить анкету' или нажмите кнопку в меню.")
    else:
        await message.answer("❌ Неподдерживаемый язык.")

# 🔹 Команда /company
@dp.message(Command("company"))
async def handle_company(message: Message):
    await message.answer("📦 Раздел для компаний в разработке. Ожидайте обновлений!")

# 🔹 Прочие сообщения
@dp.message()
async def fallback(message: Message):
    await message.answer("✏️ Напишите 'заполнить анкету' или нажмите кнопку в меню.")

# 🚀 Старт
async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)
    pool = await connect_to_db()
    app["db"] = pool
    commands = [
        BotCommand(command="start", description="Главное меню"),
        BotCommand(command="driver", description="Анкета водителя"),
        BotCommand(command="company", description="Анкета для компаний")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())

# 🛑 Завершение
async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    if "db" in app:
        await app["db"].close()

# 👷 Создание приложения
def create_app():
    app = web.Application()
    app["bot"] = bot
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    app.router.add_get("/", lambda _: web.Response(text="JobJet AI Bot работает!"))
    return app

# 🔁 Запуск
if __name__ == "__main__":
    web.run_app(create_app(), port=int(os.getenv("PORT", 8000)))
