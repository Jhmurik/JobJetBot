from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from states.manager_state import ManagerForm
from keyboards.start_kb import get_region_keyboard
import uuid

router = Router()

@router.message(F.text == "📋 Стать менеджером")
async def start_manager_form(message: Message, state: FSMContext):
    await state.set_state(ManagerForm.full_name)
    await message.answer("👤 Введите ваше полное имя:")

@router.message(ManagerForm.full_name)
async def form_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(ManagerForm.position)
    await message.answer("💼 Введите вашу должность (например: HR, рекрутер):")

@router.message(ManagerForm.position)
async def form_position(message: Message, state: FSMContext):
    await state.update_data(position=message.text)
    await state.set_state(ManagerForm.phone)
    await message.answer("📱 Введите номер телефона:")

@router.message(ManagerForm.phone)
async def form_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(ManagerForm.email)
    await message.answer("✉️ Введите email (если есть):")

@router.message(ManagerForm.email)
async def form_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(ManagerForm.company_name)
    await message.answer("🏢 Введите название компании, которую вы представляете:")

@router.message(ManagerForm.company_name)
async def form_company_name(message: Message, state: FSMContext):
    await state.update_data(company_name=message.text)
    await state.set_state(ManagerForm.country)
    await message.answer("🌍 Страна компании:")

@router.message(ManagerForm.country)
async def form_country(message: Message, state: FSMContext):
    await state.update_data(country=message.text)
    await state.set_state(ManagerForm.city)
    await message.answer("🏙️ Город компании:")

@router.message(ManagerForm.city)
async def form_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(ManagerForm.regions)
    await state.update_data(regions=[])
    await message.answer("🌐 Выберите регионы работы:", reply_markup=get_region_keyboard())

@router.callback_query(F.data.startswith("region_"))
async def form_regions(callback: CallbackQuery, state: FSMContext):
    region = callback.data.split("_")[1]
    data = await state.get_data()
    regions = data.get("regions", [])

    if region == "done":
        await state.update_data(regions=regions)

        app = callback.bot._ctx.get("application")
        pool = app["db"]
        manager_data = await state.get_data()

        # Запись в БД
        import asyncpg
        async with pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO managers (
                    id, user_id, full_name, position, phone, email,
                    company_name, company_country, company_city, is_owner, is_active, regions
                ) VALUES (
                    $1, $2, $3, $4, $5, $6,
                    $7, $8, $9, FALSE, FALSE, $10
                )
            """, str(uuid.uuid4()), callback.from_user.id,
                 manager_data["full_name"], manager_data["position"], manager_data["phone"], manager_data["email"],
                 manager_data["company_name"], manager_data["country"], manager_data["city"], manager_data["regions"]
            )

        await state.clear()
        await callback.message.edit_text("✅ Вы зарегистрированы как менеджер. Ожидается активация подписки.")
    else:
        if region in regions:
            regions.remove(region)
        else:
            regions.append(region)
        await state.update_data(regions=regions)
        await callback.message.edit_reply_markup(reply_markup=get_region_keyboard(regions))
