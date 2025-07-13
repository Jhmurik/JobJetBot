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
async def process_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Введите дату рождения (дд.мм.гггг):")
    await state.set_state(DriverForm.birth_date)

@router.message(DriverForm.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Укажите ваше гражданство:")
    await state.set_state(DriverForm.citizenship)

@router.message(DriverForm.citizenship)
async def process_citizenship(message: Message, state: FSMContext):
    await state.update_data(citizenship=message.text)
    await message.answer("Укажите страну проживания:")
    await state.set_state(DriverForm.residence)

@router.message(DriverForm.residence)
async def process_residence(message: Message, state: FSMContext):
    await state.update_data(residence=message.text)
    await message.answer("Укажите категории водительских прав (например, C, CE):")
    await state.set_state(DriverForm.license_type)

@router.message(DriverForm.license_type)
async def process_license_type(message: Message, state: FSMContext):
    await state.update_data(license_type=message.text)
    await message.answer("Укажите опыт вождения в годах:")
    await state.set_state(DriverForm.experience)

@router.message(DriverForm.experience)
async def process_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await message.answer("Напишите номер телефона (с кодом страны):")
    await state.set_state(DriverForm.phone)

@router.message(DriverForm.phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)

    data = await state.get_data()
    summary = (
        f"✅ Ваша анкета:\n"
        f"👤 Имя: {data['full_name']}\n"
        f"🎂 Дата рождения: {data['birth_date']}\n"
        f"🌍 Гражданство: {data['citizenship']}\n"
        f"🏠 Проживание: {data['residence']}\n"
        f"🚗 Категории: {data['license_type']}\n"
        f"📅 Опыт: {data['experience']} лет\n"
        f"📞 Телефон: {data['phone']}"
    )

    await message.answer(summary)
    await message.answer("Спасибо! Анкета заполнена ✅")
    await state.clear()
