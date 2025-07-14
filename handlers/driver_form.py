from aiogram import Router from aiogram.types import Message from aiogram.fsm.context import FSMContext from states.driver_state import DriverForm

router = Router()

▶️ Полное имя

@router.message(DriverForm.full_name) async def process_full_name(message: Message, state: FSMContext): await state.update_data(full_name=message.text.strip()) await message.answer("\ud83d\udcc5 \u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0434\u0430\u0442\u0443 \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f (\u0434\u0434.\u043c\u043c.\u0433\u0433\u0433\u0433):") await state.set_state(DriverForm.birth_date)

▶️ Дата рождения

@router.message(DriverForm.birth_date) async def process_birth_date(message: Message, state: FSMContext): await state.update_data(birth_date=message.text.strip()) await message.answer("\ud83c\udf0d \u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u0432\u0430\u0448\u0435 \u0433\u0440\u0430\u0436\u0434\u0430\u043d\u0441\u0442\u0432\u043e:") await state.set_state(DriverForm.citizenship)

▶️ Гражданство

@router.message(DriverForm.citizenship) async def process_citizenship(message: Message, state: FSMContext): await state.update_data(citizenship=message.text.strip()) await message.answer("\ud83c\udfe0 \u0412 \u043a\u0430\u043a\u043e\u0439 \u0441\u0442\u0440\u0430\u043d\u0435 \u0432\u044b \u0441\u0435\u0439\u0447\u0430\u0441 \u043f\u0440\u043e\u0436\u0438\u0432\u0430\u0435\u0442\u0435?") await state.set_state(DriverForm.residence)

▶️ Место проживания

@router.message(DriverForm.residence) async def process_residence(message: Message, state: FSMContext): await state.update_data(residence=message.text.strip()) await message.answer("\ud83d\ude98 \u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f \u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c\u0441\u043a\u0438\u0445 \u043f\u0440\u0430\u0432 (\u043d\u0430\u043f\u0440\u0438\u043c\u0435\u0440, C, CE):") await state.set_state(DriverForm.license_type)

▶️ Водительские права

@router.message(DriverForm.license_type) async def process_license_type(message: Message, state: FSMContext): await state.update_data(license_type=message.text.strip()) await message.answer("\ud83d\udcc8 \u0421\u043a\u043e\u043b\u044c\u043a\u043e \u043b\u0435\u0442 \u043e\u043f\u044b\u0442\u0430 \u0432\u043e\u0436\u0434\u0435\u043d\u0438\u044f \u0443 \u0432\u0430\u0441?") await state.set_state(DriverForm.experience)

▶️ Опыт

@router.message(DriverForm.experience) async def process_experience(message: Message, state: FSMContext): await state.update_data(experience=message.text.strip()) await message.answer("\ud83d\udd0a \u041a\u0430\u043a\u0438\u0435 \u044f\u0437\u044b\u043a\u0438 \u0432\u044b \u0437\u043d\u0430\u0435\u0442\u0435? (\u0447\u0435\u0440\u0435\u0437 \u0437\u0430\u043f\u044f\u0442\u0443\u044e)") await state.set_state(DriverForm.languages)

▶️ Языки

@router.message(DriverForm.languages) async def process_languages(message: Message, state: FSMContext): await state.update_data(languages=message.text.strip()) await message.answer("\ud83d\udcc4 \u041a\u0430\u043a\u0438\u0435 \u0443 \u0432\u0430\u0441 \u0435\u0441\u0442\u044c \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u044b \u0434\u043b\u044f \u0440\u0430\u0431\u043e\u0442\u044b?") await state.set_state(DriverForm.documents)

▶️ Документы

@router.message(DriverForm.documents) async def process_documents(message: Message, state: FSMContext): await state.update_data(documents=message.text.strip()) await message.answer("\ud83d\ude9b \u041f\u0440\u0435\u0434\u043f\u043e\u0447\u0438\u0442\u0430\u0435\u043c\u044b\u0439 \u0442\u0438\u043f \u0433\u0440\u0443\u0437\u043e\u0432\u0438\u043a\u0430:") await state.set_state(DriverForm.truck_type)

▶️ Тип грузовика

@router.message(DriverForm.truck_type) async def process_truck_type(message: Message, state: FSMContext): await state.update_data(truck_type=message.text.strip()) await message.answer("\ud83d\udcc5 \u041f\u0440\u0435\u0434\u043f\u043e\u0447\u0438\u0442\u0430\u0435\u043c\u044b\u0439 \u0442\u0438\u043f \u0437\u0430\u043d\u044f\u0442\u043e\u0441\u0442\u0438 (\u043f\u043e\u043b\u043d\u0430\u044f/\u0432\u0440\u0435\u043c\u0435\u043d\u043d\u0430\u044f):") await state.set_state(DriverForm.employment_type)

▶️ Тип занятости

@router.message(DriverForm.employment_type) async def process_employment_type(message: Message, state: FSMContext): await state.update_data(employment_type=message.text.strip()) await message.answer("\ud83d\udd52 \u0413\u043e\u0442\u043e\u0432\u043d\u043e\u0441\u0442\u044c \u043a \u0432\u044b\u0435\u0437\u0434\u0443 (\u0434\u0430\u0442\u0430 \u0438\u043b\u0438 'сразу'):") await state.set_state(DriverForm.ready_to_depart)

▶️ Готовность к выезду

@router.message(DriverForm.ready_to_depart) async def process_ready_to_depart(message: Message, state: FSMContext): await state.update_data(ready_to_depart=message.text.strip()) await state.update_data(ready_to_work=True) await message.answer("\ud83d\udcf1 \u0412\u0430\u0448\u0438 \u043a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435 (\u0442\u0435\u043b\u0435\u0444\u043e\u043d, Telegram \u0438 \u0442.\u0434.):") await state.set_state(DriverForm.contacts)

▶️ Контакты

@router.message(DriverForm.contacts) async def process_contacts(message: Message, state: FSMContext): await state.update_data(contacts=message.text.strip()) data = await state.get_data()

summary = "\n".join([
    f"{key.replace('_', ' ').capitalize()}: {', '.join(value) if isinstance(value, list) else value}"
    for key, value in data.items()
])

await message.answer(
    f"\ud83d\udcdf \u041f\u0440\u043e\u0432\u0435\u0440\u044c\u0442\u0435 \u0432\u0432\u0435\u0434\u0451\u043d\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435:\n\n{summary}\n\n"
    "\u0415\u0441\u043b\u0438 \u0432\u0441\u0451 \u0432\u0435\u0440\u043d\u043e, \u043d\u0430\u043f\u0438\u0448\u0438\u0442\u0435 *\u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0430\u044e* \u0434\u043b\u044f \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438 \u0430\u043d\u043a\u0435\u0442\u044b.",
    parse_mode="Markdown"
)
await state.set_state(DriverForm.confirmation)

▶️ Подтверждение

@router.message(DriverForm.confirmation) async def process_confirmation(message: Message, state: FSMContext): if message.text.strip().lower() == "подтверждаю": data = await state.get_data() pool = message.bot.get("db") if pool is None: await message.answer("\u274c \u041e\u0448\u0438\u0431\u043a\u0430 \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f \u043a \u0431\u0430\u0437\u0435 \u0434\u0430\u043d\u043d\u044b\u0445.") return

async with pool.acquire() as conn:
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
        data.get("ready_to_depart", ""),
        data.get("contacts", "")
        )

    await message.answer("\u2705 \u0421\u043f\u0430\u0441\u0438\u0431\u043e! \u0412\u0430\u0448\u0430 \u0430\u043d\u043a\u0435\u0442\u0430 \u0443\u0441\u043f\u0435\u0448\u043d\u043e \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0430.")
    await state.clear()
else:
    await message.answer("\u274c \u0410\u043d\u043a\u0435\u0442\u0430 \u043d\u0435 \u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0430. \u0427\u0442\u043e\u0431\u044b \u043d\u0430\u0447\u0430\u0442\u044c \u0437\u0430\u043d\u043e\u0432\u043e \u2014 \u043d\u0430\u0436\u043c\u0438\u0442\u0435 '\ud83d\udcdd \u0417\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0430\u043d\u043a\u0435\u0442\u0443'.")
    await state.clear()

