from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.driver_state import DriverForm
from aiogram.filters import Command

router = Router()


@router.message(Command("driver"))
async def start_driver_form(message: Message, state: FSMContext):
    await message.answer("Введите ваше полное имя:")
    await state.set_state(DriverForm.full_name)


@router.message(DriverForm.full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Введите дату рождения (например, 05.08.1989):")
    await state.set_state(DriverForm.birth_date)


@router.message(DriverForm.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Укажите ваше гражданство:")
    await state.set_state(DriverForm.citizenship)


@router.message(DriverForm.citizenship)
async def process_citizenship(message: Message, state: FSMContext):
    await state.update_data(citizenship=message.text)
    await message.answer("Где вы сейчас проживаете?")
    await state.set_state(DriverForm.residence)


@router.message(DriverForm.residence)
async def process_residence(message: Message, state: FSMContext):
    await state.update_data(residence=message.text)
    await message.answer("Укажите категорию ваших водительских прав (например, CE):")
    await state.set_state(DriverForm.license_type)


@router.message(DriverForm.license_type)
async def process_license_type(message: Message, state: FSMContext):
    await state.update_data(license_type=message.text)
    await message.answer("Стаж работы водителем (в годах):")
    await state.set_state(DriverForm.experience)


@router.message(DriverForm.experience)
async def process_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await message.answer("Какими языками вы владеете?")
    await state.set_state(DriverForm.languages)


@router.message(DriverForm.languages)
async def process_languages(message: Message, state: FSMContext):
    await state.update_data(languages=message.text)
    await message.answer("Какие у вас есть документы? (ВНЖ, 95 код, паспорт и т.д.):")
    await state.set_state(DriverForm.documents)


@router.message(DriverForm.documents)
async def process_documents(message: Message, state: FSMContext):
    await state.update_data(documents=message.text)
    await message.answer("Какой тип грузовика предпочитаете? (тягач, бус, автовоз и т.д.):")
    await state.set_state(DriverForm.truck_type)


@router.message(DriverForm.truck_type)
async def process_truck_type(message: Message, state: FSMContext):
    await state.update_data(truck_type=message.text)
    await message.answer("Какой тип занятости вас интересует? (полная, вахта и т.д.):")
    await state.set_state(DriverForm.employment_type)


@router.message(DriverForm.employment_type)
async def process_employment_type(message: Message, state: FSMContext):
    await state.update_data(employment_type=message.text)
    await message.answer("Когда вы готовы выехать на работу?")
    await state.set_state(DriverForm.ready_to_depart)


@router.message(DriverForm.ready_to_depart)
async def process_ready_to_depart(message: Message, state: FSMContext):
    await state.update_data(ready_to_depart=message.text)
    await message.answer("Оставьте контактные данные (телефон или Telegram):")
    await state.set_state(DriverForm.contacts)


@router.message(DriverForm.contacts)
async def process_contacts(message: Message, state: FSMContext):
    await state.update_data(contacts=message.text)

    data = await state.get_data()
    summary = "\n".join([f"{key.replace('_', ' ').capitalize()}: {value}" for key, value in data.items()])

    await message.answer(f"Проверьте введённые данные:\n\n{summary}\n\nНапишите 'да', если всё верно или 'нет', чтобы начать заново.")
    await state.set_state(DriverForm.confirmation)


@router.message(DriverForm.confirmation)
async def confirm_form(message: Message, state: FSMContext):
    if message.text.lower() == "да":
        await message.answer("Спасибо! Ваша анкета принята. Ожидайте отклика.")
        await state.clear()
    else:
        await message.answer("Окей, давайте начнём заново. Введите ваше полное имя:")
        await state.set_state(DriverForm.full_name)
