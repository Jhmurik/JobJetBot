from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from asyncpg import Pool
from states.company_state import CompanyStart
import uuid

router = Router()

# 📦 Старт регистрации компании
@router.message(F.text == "📦 Зарегистрировать компанию")
async def start_company_registration(message: Message, state: FSMContext):
    await state.set_state(CompanyStart.name)
    await message.answer("🏢 Введите название вашей компании:")

@router.message(CompanyStart.name)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CompanyStart.description)
    await message.answer("📝 Введите краткое описание компании:")

@router.message(CompanyStart.description)
async def set_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(CompanyStart.country)
    await message.answer("🌍 Укажите страну, где находится ваша компания:")

@router.message(CompanyStart.country)
async def set_country(message: Message, state: FSMContext):
    await state.update_data(country=message.text)
    await state.set_state(CompanyStart.city)
    await message.answer("🏙️ Укажите город вашей компании:")

@router.message(CompanyStart.city)
async def set_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(CompanyStart.regions)
    await message.answer("🌐 Укажите регионы работы (например: Европа, СНГ, США):")

@router.message(CompanyStart.regions)
async def set_regions(message: Message, state: FSMContext):
    await state.update_data(regions=[r.strip() for r in message.text.split(",")])
    await state.set_state(CompanyStart.confirm)

    data = await state.get_data()
    preview = (
        f"🏢 Название: {data['name']}\n"
        f"📝 Описание: {data['description']}\n"
        f"🌍 Страна: {data['country']}, город: {data['city']}\n"
        f"📍 Регионы: {', '.join(data['regions'])}"
    )

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Подтвердить регистрацию")],
            [KeyboardButton(text="❌ Отменить")]
        ],
        resize_keyboard=True
    )
    await message.answer(f"{preview}\n\nПроверьте данные и подтвердите:", reply_markup=kb)

@router.message(F.text == "✅ Подтвердить регистрацию")
async def confirm_company(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    company_id = uuid.uuid4()

    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO companies (
                id, name, description, country, city, owner_id, regions
            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
        """, company_id, data["name"], data["description"], data["country"],
             data["city"], user_id, data["regions"])

        # Добавим владельца как менеджера с is_owner = TRUE
        manager_id = uuid.uuid4()
        await conn.execute("""
            INSERT INTO managers (
                id, company_id, user_id, full_name, position,
                phone, email, is_owner, is_active, regions
            ) VALUES (
                $1, $2, $3, '-', '-', '-', '-', TRUE, FALSE, $4
            )
        """, manager_id, company_id, user_id, data["regions"])

    await state.clear()
    await message.answer("✅ Компания успешно зарегистрирована! Теперь вы — владелец. Подключите Premium для работы.")

@router.message(F.text == "❌ Отменить")
async def cancel_company_registration(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Регистрация компании отменена.")
