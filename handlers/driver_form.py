from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.driver_state import DriverForm

router = Router()

# ▶️ Начало анкеты — вызывается по кнопке в main.py
@router.message(DriverForm.full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("📅 Введите дату рождения (дд.мм.гггг):")
    await state.set_state(DriverForm.birth_date)

@router.message(DriverForm.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("🌍 Укажите ваше гражданство:")
    await state.set_state(DriverForm.citizenship)

@router.message(DriverForm.citizenship)
async def process_citizenship(message: Message, state: FSMContext):
    await state.update_data(citizenship=message.text)
    await message.answer("🏠 В какой стране вы сейчас проживаете?")
    await state.set_state(DriverForm.residence)

@router.message(DriverForm.residence)
async def process_residence(message: Message, state: FSMContext):
    await state.update_data(residence=message.text)
    await message.answer("🚘 Категория водительских прав (например, C, CE):")
    await state.set_state(DriverForm.license_type)

@router.message(DriverForm.license_type)
async def process_license_type(message: Message, state: FSMContext):
    await state.update_data(license_type=message.text)
    await message.answer("📈 Сколько лет опыта вождения у вас?")
    await state.set_state(DriverForm.experience)

@router.message(DriverForm.experience)
async def process_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await message.answer("🗣️ Какие языки вы знаете? (через запятую)")
    await state.set_state(DriverForm.languages)

@router.message(DriverForm.languages)
async def process_languages(message: Message, state: FSMContext):
    await state.update_data(languages=message.text)
    await message.answer("📄 Какие у вас есть документы для работы?")
    await state.set_state(DriverForm.documents)

@router.message(DriverForm.documents)
async def process_documents(message: Message, state: FSMContext):
    await state.update_data(documents=message.text)
    await message.answer("🚛 Предпочитаемый тип грузовика:")
    await state.set_state(DriverForm.truck_type)

@router.message(DriverForm.truck_type)
async def process_truck_type(message: Message, state: FSMContext):
    await state.update_data(truck_type=message.text)
    await message.answer("📅 Предпочитаемый тип занятости (полная/временная):")
    await state.set_state(DriverForm.employment_type)

@router.message(DriverForm.employment_type)
async def process_employment_type(message: Message, state: FSMContext):
    await state.update_data(employment_type=message.text)
    await message.answer("🕒 Готовность к выезду (дата или 'сразу'):")
    await state.set_state(DriverForm.ready_to_depart)

@router.message(DriverForm.ready_to_depart)
async def process_ready_to_depart(message: Message, state: FSMContext):
    await state.update_data(ready_to_work=True)
    await message.answer("📱 Ваши контактные данные (телефон, Telegram и т.д.):")
    await state.set_state(DriverForm.contacts)

@router.message(DriverForm.contacts)
async def process_contacts(message: Message, state: FSMContext):
    await state.update_data(contacts=message.text)
    data = await state.get_data()

    summary = "\n".join([
        f"{key.replace('_', ' ').capitalize()}: {', '.join(value) if isinstance(value, list) else value}"
        for key, value in data.items()
    ])

    await message.answer(
        f"🧾 Проверьте введённые данные:\n\n{summary}\n\n"
        "Если всё верно, напишите *подтверждаю* для отправки анкеты.",
        parse_mode="Markdown"
    )
    await state.set_state(DriverForm.confirmation)

@router.message(DriverForm.confirmation)
async def process_confirmation(message: Message, state: FSMContext):
    if message.text.strip().lower() == "подтверждаю":
        data = await state.get_data()
        pool = message.bot.get("db")
        if pool is None:
            await message.answer("❌ Ошибка подключения к базе данных.")
            return

        async with pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO drivers (
                    full_name, birth_date, citizenship, residence, license_type,
                    experience, languages, documents, truck_type, employment_type,
                    ready_to_work, contacts
                ) VALUES (
                    $1, $2, $3, $4, $5,
                    $6, $7, $8, $9, $10,
                    TRUE, $11
                )
            """,
            data.get("full_name", ""),
            data.get("birth_date", ""),
            data.get("citizenship", ""),
            data.get("residence", ""),
            data.get("license_type", ""),
            data.get("experience", ""),
            [lang.strip() for lang in data.get("languages", "").split(",")],
            data.get("documents", ""),
            data.get("truck_type", ""),
            data.get("employment_type", ""),
            data.get("contacts", "")
            )

        await message.answer("✅ Спасибо! Ваша анкета успешно сохранена.")
        await state.clear()
    else:
        await message.answer("❌ Анкета не подтверждена. Чтобы начать заново — нажмите '📝 Заполнить анкету'.")
        await state.clear()
