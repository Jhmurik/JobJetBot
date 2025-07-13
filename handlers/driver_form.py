from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.driver_state import DriverForm

router = Router()

@router.message(F.text.lower() == "заполнить анкету")
async def start_form(message: Message, state: FSMContext):
    await message.answer("Введите ваше полное имя:")
    await state.set_state(DriverForm.full_name)

@router.message(DriverForm.full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Введите дату рождения (дд.мм.гггг):")
    await state.set_state(DriverForm.birth_date)

@router.message(DriverForm.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Ваше гражданство:")
    await state.set_state(DriverForm.citizenship)

@router.message(DriverForm.citizenship)
async def process_citizenship(message: Message, state: FSMContext):
    await state.update_data(citizenship=message.text)
    await message.answer("Страна проживания:")
    await state.set_state(DriverForm.residence)

@router.message(DriverForm.residence)
async def process_residence(message: Message, state: FSMContext):
    await state.update_data(residence=message.text)
    await message.answer("Категория водительских прав (например, C, CE):")
    await state.set_state(DriverForm.license_type)

@router.message(DriverForm.license_type)
async def process_license_type(message: Message, state: FSMContext):
    await state.update_data(license_type=message.text)
    await message.answer("Опыт вождения (лет):")
    await state.set_state(DriverForm.experience)

@router.message(DriverForm.experience)
async def process_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await message.answer("Знание языков:")
    await state.set_state(DriverForm.languages)

@router.message(DriverForm.languages)
async def process_languages(message: Message, state: FSMContext):
    await state.update_data(languages=message.text)
    await message.answer("Какие документы есть для работы?")
    await state.set_state(DriverForm.documents)

@router.message(DriverForm.documents)
async def process_documents(message: Message, state: FSMContext):
    await state.update_data(documents=message.text)
    await message.answer("Какой тип грузовика предпочитаете?")
    await state.set_state(DriverForm.truck_type)

@router.message(DriverForm.truck_type)
async def process_truck_type(message: Message, state: FSMContext):
    await state.update_data(truck_type=message.text)
    await message.answer("Желаемый тип занятости (полная/временная):")
    await state.set_state(DriverForm.employment_type)

@router.message(DriverForm.employment_type)
async def process_employment_type(message: Message, state: FSMContext):
    await state.update_data(employment_type=message.text)
    await message.answer("Готовность к выезду (д
