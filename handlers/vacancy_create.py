from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from states.vacancy_state import VacancyForm
from asyncpg import Pool
import uuid

router = Router()

# 📢 Кнопка "Создать вакансию"
@router.message(F.text == "📢 Создать вакансию")
async def create_vacancy_start(message: Message, state: FSMContext):
    await state.set_state(VacancyForm.title)
    await message.answer("📝 Введите название вакансии:")

@router.message(VacancyForm.title)
async def set_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(VacancyForm.truck_type)
    await message.answer("🚛 Тип транспорта (тягач, бус, автовоз и т.д.):")

@router.message(VacancyForm.truck_type)
async def set_truck_type(message: Message, state: FSMContext):
    await state.update_data(truck_type=message.text)
    await state.set_state(VacancyForm.salary)
    await message.answer("💰 Укажите зарплату (например: от 2000€/мес):")

@router.message(VacancyForm.salary)
async def set_salary(message: Message, state: FSMContext):
    await state.update_data(salary=message.text)
    await state.set_state(VacancyForm.region)
    await message.answer("🌍 Укажите регион (например: Европа, СНГ):")

@router.message(VacancyForm.region)
async def set_region(message: Message, state: FSMContext):
    await state.update_data(region=message.text)
    await state.set_state(VacancyForm.requirements)
    await message.answer("📋 Укажите требования к водителю:")

@router.message(VacancyForm.requirements)
async def set_requirements(message: Message, state: FSMContext):
    await state.update_data(requirements=message.text)
    await state.set_state(VacancyForm.contacts)
    await message.answer("📞 Контакты для связи (телефон, Telegram и т.д.):")

@router.message(VacancyForm.contacts)
async def set_contacts(message: Message, state: FSMContext):
    await state.update_data(contacts=message.text)
    await state.set_state(VacancyForm.confirm)

    data = await state.get_data()
    preview = (
        f"📢 *Вакансия: {data['title']}*\n"
        f"🚛 Транспорт: {data['truck_type']}\n"
        f"💰 Зарплата: {data['salary']}\n"
        f"🌍 Регион: {data['region']}\n"
        f"📋 Требования: {data['requirements']}\n"
        f"📞 Контакты: {data['contacts']}"
    )

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Опубликовать вакансию")],
            [KeyboardButton(text="❌ Отменить")]
        ],
        resize_keyboard=True
    )

    await message.answer(preview, parse_mode="Markdown")
    await message.answer("🔎 Проверьте данные и подтвердите публикацию:", reply_markup=kb)

@router.message(F.text == "✅ Опубликовать вакансию")
async def confirm_vacancy(message: Message, state: FSMContext):
    data = await state.get_data()
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    vacancy_id = uuid.uuid4()
    user_id = message.from_user.id

    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO vacancies (
                id, manager_id, title, truck_type, salary, region, requirements, contacts, created_at
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, CURRENT_TIMESTAMP
            )
        """, vacancy_id, user_id, data['title'], data['truck_type'], data['salary'],
             data['region'], data['requirements'], data['contacts'])

    await state.clear()
    await message.answer("✅ Вакансия успешно опубликована!")

@router.message(F.text == "❌ Отменить")
async def cancel_vacancy(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Создание вакансии отменено.")
