from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.driver_state import DriverForm
from asyncpg import Pool

router = Router()

@router.message(DriverForm.full_name)
async def handle_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(DriverForm.birth_date)
    await message.answer("📅 Введите дату рождения (например, 05.08.1989):")

@router.message(DriverForm.birth_date)
async def handle_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await state.set_state(DriverForm.citizenship)
    await message.answer("🌍 Введите гражданство:")

@router.message(DriverForm.citizenship)
async def handle_citizenship(message: Message, state: FSMContext):
    await state.update_data(citizenship=message.text)
    await state.set_state(DriverForm.residence)
    await message.answer("🏠 Введите текущее место проживания:")

@router.message(DriverForm.residence)
async def handle_residence(message: Message, state: FSMContext):
    await state.update_data(residence=message.text)
    await state.set_state(DriverForm.license_type)
    await message.answer("🚘 Введите категории водительского удостоверения (например: B, C, E):")

@router.message(DriverForm.license_type)
async def handle_license_type(message: Message, state: FSMContext):
    await state.update_data(license_type=message.text)
    await state.set_state(DriverForm.experience)
    await message.answer("📈 Введите стаж вождения (например, 5 лет):")

@router.message(DriverForm.experience)
async def handle_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await state.set_state(DriverForm.languages)
    await message.answer("🗣️ Введите языки через запятую (например: Русский, Английский):")

@router.message(DriverForm.languages)
async def handle_languages(message: Message, state: FSMContext):
    await state.update_data(languages=[lang.strip() for lang in message.text.split(",")])
    await state.set_state(DriverForm.documents)
    await message.answer("📄 Укажите наличие документов (например: ВНЖ, биометрия, паспорт ЕС):")

@router.message(DriverForm.documents)
async def handle_documents(message: Message, state: FSMContext):
    await state.update_data(documents=message.text)
    await state.set_state(DriverForm.truck_type)
    await message.answer("🚛 Какой тип грузовика предпочитаете (тягач, бус, автовоз и т.д.):")

@router.message(DriverForm.truck_type)
async def handle_truck_type(message: Message, state: FSMContext):
    await state.update_data(truck_type=message.text)
    await state.set_state(DriverForm.employment_type)
    await message.answer("💼 Тип занятости (вахта, на постоянку, подмена и т.д.):")

@router.message(DriverForm.employment_type)
async def handle_employment_type(message: Message, state: FSMContext):
    await state.update_data(employment_type=message.text)
    await state.set_state(DriverForm.ready_to_depart)
    await message.answer("📆 Когда готовы приступить к работе? (сегодня, через неделю и т.д.):")

@router.message(DriverForm.ready_to_depart)
async def handle_ready_to_depart(message: Message, state: FSMContext):
    await state.update_data(ready_to_depart=message.text)
    await state.set_state(DriverForm.contacts)
    await message.answer("📱 Укажите контактные данные (номер телефона, Telegram и т.д.):")

@router.message(DriverForm.contacts)
async def handle_contacts(message: Message, state: FSMContext):
    await state.update_data(contacts=message.text)

    data = await state.get_data()
    data["driver_id"] = message.from_user.id
    data["is_active"] = True

    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO drivers (
                full_name, birth_date, citizenship, residence,
                license_type, experience, languages, documents,
                truck_type, employment_type, ready_to_depart,
                contacts, is_active, created_at, id
            )
            VALUES (
                $1, $2, $3, $4,
                $5, $6, $7, $8,
                $9, $10, $11,
                $12, $13, CURRENT_TIMESTAMP, $14
            )
            ON CONFLICT (id) DO UPDATE
            SET
                full_name = EXCLUDED.full_name,
                birth_date = EXCLUDED.birth_date,
                citizenship = EXCLUDED.citizenship,
                residence = EXCLUDED.residence,
                license_type = EXCLUDED.license_type,
                experience = EXCLUDED.experience,
                languages = EXCLUDED.languages,
                documents = EXCLUDED.documents,
                truck_type = EXCLUDED.truck_type,
                employment_type = EXCLUDED.employment_type,
                ready_to_depart = EXCLUDED.ready_to_depart,
                contacts = EXCLUDED.contacts,
                is_active = TRUE,
                created_at = CURRENT_TIMESTAMP
        """, data["full_name"], data["birth_date"], data["citizenship"], data["residence"],
             data["license_type"], data["experience"], data["languages"], data["documents"],
             data["truck_type"], data["employment_type"], data["ready_to_depart"],
             data["contacts"], True, data["driver_id"])

    await state.clear()
    await message.answer("✅ Анкета успешно сохранена! Спасибо!")
