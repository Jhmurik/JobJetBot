from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command # НОВОЕ: Добавляем импорт Command
from states.driver_state import DriverForm

router = Router()

# НОВОЕ: Точка входа для начала заполнения анкеты (командой)
@router.message(Command("fill_form"))
async def start_driver_form_command(message: Message, state: FSMContext):
    await state.clear() # Начинаем заполнение с чистого листа
    await state.set_state(DriverForm.full_name)
    await message.answer("📝 Отлично! Начнём заполнение анкеты. Пожалуйста, введите ваше *полное имя* (ФИО):", parse_mode="Markdown")

# 🔹 Полное имя
@router.message(DriverForm.full_name)
async def process_full_name(message: Message, state: FSMContext):
    if not message.text: # Простая валидация
        await message.answer("Пожалуйста, введите ваше имя текстом.")
        return
    await state.update_data(full_name=message.text.strip())
    await message.answer("📅 Введите дату рождения (дд.мм.гггг):")
    await state.set_state(DriverForm.birth_date)

# 🔹 Дата рождения
@router.message(DriverForm.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, введите дату рождения текстом.")
        return
    await state.update_data(birth_date=message.text.strip())
    await message.answer("🌍 Укажите ваше гражданство:")
    await state.set_state(DriverForm.citizenship)

# 🔹 Гражданство
@router.message(DriverForm.citizenship)
async def process_citizenship(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, введите гражданство текстом.")
        return
    await state.update_data(citizenship=message.text.strip())
    await message.answer("🏠 В какой стране вы сейчас проживаете?")
    await state.set_state(DriverForm.residence)

# 🔹 Место проживания
@router.message(DriverForm.residence)
async def process_residence(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, введите страну проживания текстом.")
        return
    await state.update_data(residence=message.text.strip())
    await message.answer("🚘 Категория водительских прав (например, C, CE):")
    await state.set_state(DriverForm.license_type)

# 🔹 Права
@router.message(DriverForm.license_type)
async def process_license_type(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, введите категорию прав текстом.")
        return
    await state.update_data(license_type=message.text.strip())
    await message.answer("📈 Сколько лет опыта вождения у вас?")
    await state.set_state(DriverForm.experience)

# 🔹 Опыт
@router.message(DriverForm.experience)
async def process_experience(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, введите опыт вождения текстом.")
        return
    await state.update_data(experience=message.text.strip())
    await message.answer("🗣️ Какие языки вы знаете? (через запятую)")
    await state.set_state(DriverForm.languages)

# 🔹 Языки
@router.message(DriverForm.languages)
async def process_languages(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, введите языки текстом.")
        return
    raw = message.text.strip()
    languages = [lang.strip() for lang in raw.split(",") if lang.strip()]
    await state.update_data(languages=languages)
    await message.answer("📄 Какие у вас есть документы для работы?")
    await state.set_state(DriverForm.documents)

# 🔹 Документы
@router.message(DriverForm.documents)
async def process_documents(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, введите документы текстом.")
        return
    await state.update_data(documents=message.text.strip())
    await message.answer("🚛 Предпочитаемый тип грузовика:")
    await state.set_state(DriverForm.truck_type)

# 🔹 Тип грузовика
@router.message(DriverForm.truck_type)
async def process_truck_type(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, введите тип грузовика текстом.")
        return
    await state.update_data(truck_type=message.text.strip())
    await message.answer("📅 Предпочитаемый тип занятости (полная/временная):")
    await state.set_state(DriverForm.employment_type)

# 🔹 Тип занятости
@router.message(DriverForm.employment_type)
async def process_employment_type(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, введите тип занятости текстом.")
        return
    await state.update_data(employment_type=message.text.strip())
    await message.answer("🕒 Готовность к выезду (дата или 'сразу'):")
    await state.set_state(DriverForm.ready_to_depart)

# 🔹 Готовность к выезду
@router.message(DriverForm.ready_to_depart)
async def process_ready_to_depart(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, введите готовность к выезду текстом.")
        return
    await state.update_data(ready_to_depart=message.text.strip())
    await message.answer("📱 Ваши контактные данные (телефон, Telegram и т.д.):")
    await state.set_state(DriverForm.contacts)

# 🔹 Контакты
@router.message(DriverForm.contacts)
async def process_contacts(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, введите контакты текстом.")
        return
    await state.update_data(contacts=message.text.strip())
    data = await state.get_data()

    # Убедитесь, что все поля имеют значения по умолчанию, если они могут быть пустыми
    summary_parts = []
    for key, value in data.items():
        if isinstance(value, list):
            summary_value = ', '.join(value) if value else 'Не указано'
        else:
            summary_value = value if value else 'Не указано'
        summary_parts.append(f"*{key.replace('_', ' ').capitalize()}*: {summary_value}")

    summary = "\n".join(summary_parts)

    await message.answer(
        f"🧾 Проверьте введённые данные:\n\n{summary}\n\n"
        "Если всё верно, напишите *подтверждаю* для отправки анкеты.",
        parse_mode="Markdown"
    )
    await state.set_state(DriverForm.confirmation)

# 🔹 Подтверждение
@router.message(DriverForm.confirmation)
async def process_confirmation(message: Message, state: FSMContext):
    # Простая защита от пустых сообщений
    if not message.text:
        await message.answer("Пожалуйста, введите 'подтверждаю' или 'отмена'.")
        return

    if message.text.strip().lower() == "подтверждаю":
        data = await state.get_data()

        # НОВОЕ: Правильный способ получить pool из приложения aiohttp
        pool = message.bot.get('__APP__').get("db")
        if not pool:
            await message.answer("❌ Ошибка подключения к базе данных.")
            return

        async with pool.acquire() as conn:
            # Убедитесь, что поля в INSERT соответствуют колонкам в вашей БД
            # и что порядок и количество $1, $2... правильные.
            # Добавил 'ready_to_work' = TRUE по умолчанию, как было в вашем коде.
            await conn.execute("""
                INSERT INTO drivers (
                    full_name, birth_date, citizenship, residence, license_type,
                    experience, languages, documents, truck_type, employment_type,
                    ready_to_work, ready_to_depart, contacts
                ) VALUES (
                    $1, $2, $3, $4, $5,
                    $6, $7, $8, $9, $10,
                    TRUE, $11, $12
                )
            """,
                data.get("full_name", None), # Используем None, чтобы БД могла обрабатывать NULL
                data.get("birth_date", None),
                data.get("citizenship", None),
                data.get("residence", None),
                data.get("license_type", None),
                data.get("experience", None),
                data.get("languages", []), # Список для PostgeSQL TEXT[]
                data.get("documents", None),
                data.get("truck_type", None),
                data.get("employment_type", None),
                data.get("ready_to_depart", None),
                data.get("contacts", None)
            )

        await message.answer("✅ Спасибо! Ваша анкета успешно сохранена.")
        await state.clear()
    else:
        await message.answer("❌ Анкета не подтверждена. Чтобы начать заново — нажмите '📝 Заполнить анкету' или напишите /fill_form.")
        await state.clear()

