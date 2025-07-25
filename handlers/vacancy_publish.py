from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from states.vacancy_state import VacancyForm
from asyncpg import Pool
from uuid import uuid4

router = Router()

# 📢 Запуск публикации вакансии
@router.message(F.text.lower() == "📢 опубликовать вакансию")
async def start_vacancy_publish(message: Message, state: FSMContext):
    await state.set_state(VacancyForm.title)
    await message.answer("📌 Введите заголовок вакансии (например: Водитель C+E по Европе):")

@router.message(VacancyForm.title)
async def set_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(VacancyForm.truck_type)
    await message.answer("🚛 Укажите тип транспорта (тягач, бус, автовоз и т.д.):")

@router.message(VacancyForm.truck_type)
async def set_truck_type(message: Message, state: FSMContext):
    await state.update_data(truck_type=message.text)
    await state.set_state(VacancyForm.salary)
    await message.answer("💰 Укажите зарплату (например: от 2000€, ставка, за км и т.д.):")

@router.message(VacancyForm.salary)
async def set_salary(message: Message, state: FSMContext):
    await state.update_data(salary=message.text)
    await state.set_state(VacancyForm.region)
    await message.answer("🌍 Укажите регион работы (например: Европа, СНГ, США):")

@router.message(VacancyForm.region)
async def set_region(message: Message, state: FSMContext):
    await state.update_data(region=message.text)
    await state.set_state(VacancyForm.requirements)
    await message.answer("📋 Укажите требования к водителю:")

@router.message(VacancyForm.requirements)
async def set_requirements(message: Message, state: FSMContext):
    await state.update_data(requirements=message.text)
    await state.set_state(VacancyForm.contacts)
    await message.answer("📱 Укажите контакты для связи (номер, Telegram, email и т.д.):")

@router.message(VacancyForm.contacts)
async def set_contacts(message: Message, state: FSMContext):
    await state.update_data(contacts=message.text)
    data = await state.get_data()

    preview = (
        f"*📢 Вакансия: {data['title']}*\n"
        f"🚛 Транспорт: {data['truck_type']}\n"
        f"💰 Зарплата: {data['salary']}\n"
        f"🌍 Регион: {data['region']}\n"
        f"📋 Требования: {data['requirements']}\n"
        f"📱 Контакты: {data['contacts']}\n\n"
        "Опубликовать эту вакансию?"
    )

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="✅ Опубликовать"), KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True
    )

    await state.set_state(VacancyForm.confirm)
    await message.answer(preview, reply_markup=kb, parse_mode="Markdown")

@router.message(F.text == "✅ Опубликовать")
async def confirm_publish(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id

    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    try:
        async with pool.acquire() as conn:
            manager = await conn.fetchrow(
                "SELECT id, company_id FROM managers WHERE user_id = $1 AND is_active = TRUE", user_id)
            if not manager:
                await message.answer("❌ Вы не зарегистрированы как активный менеджер.")
                await state.clear()
                return

            vacancy_id = uuid4()
            await conn.execute("""
                INSERT INTO vacancies (
                    id, company_id, manager_id, title, truck_type,
                    salary, region, requirements, contacts,
                    is_published, created_at
                ) VALUES (
                    $1, $2, $3, $4, $5,
                    $6, $7, $8, $9,
                    TRUE, CURRENT_TIMESTAMP
                )
            """, vacancy_id, manager["company_id"], manager["id"],
                 data["title"], data["truck_type"], data["salary"],
                 data["region"], data["requirements"], data["contacts"])

        await message.answer("✅ Вакансия успешно опубликована!", reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📢 Опубликовать вакансию")],
                [KeyboardButton(text="📊 Статистика")],
                [KeyboardButton(text="🌐 Сменить язык")]
            ],
            resize_keyboard=True
        ))
    except Exception as e:
        await message.answer("❌ Ошибка при публикации. Попробуйте позже.")
        print(f"Ошибка публикации вакансии: {e}")
    finally:
        await state.clear()

@router.message(F.text == "❌ Отмена")
async def cancel_publish(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Публикация отменена.")
