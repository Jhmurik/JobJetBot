import asyncio import os from aiohttp import web from aiogram import Bot, Dispatcher from aiogram.fsm.storage.memory import MemoryStorage from aiogram.types import Message from aiogram.webhook.aiohttp_server import SimpleRequestHandler from aiogram.fsm.context import FSMContext from aiogram.fsm.state import State, StatesGroup from aiogram.filters import CommandStart

=== Переменные окружения ===

TOKEN = 7883161984:AAF_T1IMahf_EYS42limVzfW-5NGuyNu0Qk BASE_WEBHOOK_URL = os.getenv("WEBHOOK_BASE_URL") WEBHOOK_PATH = f"/webhook/{TOKEN}"

=== Инициализация бота и диспетчера ===

bot = Bot(token=TOKEN) dp = Dispatcher(storage=MemoryStorage())

=== Класс состояния анкеты водителя ===

class DriverForm(StatesGroup): full_name = State() phone = State() experience = State() license_category = State() region = State()

=== Обработчики команд и анкеты ===

@dp.message(CommandStart()) async def start(message: Message, state: FSMContext): await message.answer("Привет! Добро пожаловать в JobJet.\nПожалуйста, введите ваше ФИО:") await state.set_state(DriverForm.full_name)

@dp.message(DriverForm.full_name) async def process_name(message: Message, state: FSMContext): await state.update_data(full_name=message.text) await message.answer("Введите ваш номер телефона:") await state.set_state(DriverForm.phone)

@dp.message(DriverForm.phone) async def process_phone(message: Message, state: FSMContext): await state.update_data(phone=message.text) await message.answer("Укажите опыт работы:") await state.set_state(DriverForm.experience)

@dp.message(DriverForm.experience) async def process_experience(message: Message, state: FSMContext): await state.update_data(experience=message.text) await message.answer("Категория прав (например CE):") await state.set_state(DriverForm.license_category)

@dp.message(DriverForm.license_category) async def process_license(message: Message, state: FSMContext): await state.update_data(license_category=message.text) await message.answer("Из какого вы региона?") await state.set_state(DriverForm.region)

@dp.message(DriverForm.region) async def process_region(message: Message, state: FSMContext): await state.update_data(region=message.text) data = await state.get_data() await message.answer( f"\u2705 Анкета получена:\n\n" f"👤 ФИО: {data['full_name']}\n" f"📞 Телефон: {data['phone']}\n" f"🚚 Опыт: {data['experience']}\n" f"🔠 Категория: {data['license_category']}\n" f"🌍 Регион: {data['region']}" ) await state.clear()

=== Webhook события ===

async def on_startup(app: web.Application): await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}")

async def on_shutdown(app: web.Application): await bot.delete_webhook()

=== Создание и запуск приложения ===

def create_app(): app = web.Application() app["bot"] = bot app.on_startup.append(on_startup) app.on_shutdown.append(on_shutdown) SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH) return app

if name == "main": web.run_app(create_app(), port=int(os.getenv("PORT", 8080)))

