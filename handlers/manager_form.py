from aiogram import Router, F from aiogram.types import Message from aiogram.fsm.context import FSMContext from states.manager_state import ManagerForm from aiogram.types import ReplyKeyboardMarkup, KeyboardButton import uuid from asyncpg import Pool

router = Router()

🧑 Запуск регистрации менеджера

@router.message(F.text == "👨‍💼 Зарегистрироваться как менеджер") async def start_manager_registration(message: Message, state: FSMContext): await state.set_state(ManagerForm.full_name) await message.answer("👤 Введите ваше полное имя:")

@router.message(ManagerForm.full_name) async def set_full_name(message: Message, state: FSMContext): await state.update_data(full_name=message.text) await state.set_state(ManagerForm.position) await message.answer("💼 Укажите вашу должность:")

@router.message(ManagerForm.position) async def set_position(message: Message, state: FSMContext): await state.update_data(position=message.text) await state.set_state(ManagerForm.phone) await message.answer("📱 Укажите номер телефона:")

@router.message(ManagerForm.phone) async def set_phone(message: Message, state: FSMContext): await state.update_data(phone=message.text) await state.set_state(ManagerForm.email) await message.answer("📧 Укажите email (если есть):")

@router.message(ManagerForm.email) async def set_email(message: Message, state: FSMContext): await state.update_data(email=message.text) await state.set_state(ManagerForm.company_name) await message.answer("🏢 Укажите название вашей компании (или напишите 'нет'):")

@router.message(ManagerForm.company_name) async def set_company_name(message: Message, state: FSMContext): await state.update_data(company_name=message.text) await state.set_state(ManagerForm.company_country) await message.answer("🌍 Укажите страну вашей компании (или '-' если не применимо):")

@router.message(ManagerForm.company_country) async def set_company_country(message: Message, state: FSMContext): await state.update_data(company_country=message.text) await state.set_state(ManagerForm.company_city) await message.answer("🏙️ Укажите город вашей компании (или '-' если не применимо):")

@router.message(ManagerForm.company_city) async def set_company_city(message: Message, state: FSMContext): await state.update_data(company_city=message.text) await state.set_state(ManagerForm.regions) await message.answer("🌐 Укажите регионы, где вы работаете (например: Европа, СНГ, США):")

@router.message(ManagerForm.regions) async def set_regions(message: Message, state: FSMContext): await state.update_data(regions=[r.strip() for r in message.text.split(",")]) await state.set_state(ManagerForm.confirm)

data = await state.get_data()
preview = (
    f"👤 Имя: {data['full_name']}\n"
    f"💼 Должность: {data['position']}\n"
    f"📱 Телефон: {data['phone']}\n"
    f"📧 Email: {data['email']}\n"
    f"🏢 Компания: {data['company_name']} ({data['company_country']}, {data['company_city']})\n"
    f"🌍 Регионы: {', '.join(data['regions'])}"
)

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Подтвердить регистрацию")],
        [KeyboardButton(text="❌ Отменить")]
    ],
    resize_keyboard=True
)
await message.answer(f"{preview}\n\nПроверьте данные и подтвердите:", reply_markup=kb)

@router.message(F.text == "✅ Подтвердить регистрацию") async def confirm_registration(message: Message, state: FSMContext): data = await state.get_data() app = message.bot._ctx.get("application") pool: Pool = app["db"]

manager_id = str(uuid.uuid4())
user_id = message.from_user.id
is_owner = False
is_active = False

async with pool.acquire() as conn:
    company_id = None
    if data["company_name"].lower() != "нет":
        company_id = str(uuid.uuid4())
        await conn.execute("""
            INSERT INTO companies (id, name, description, country, city, owner_id, regions)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
        """, company_id, data["company_name"], "-", data["company_country"],
             data["company_city"], user_id, data["regions"])
    else:
        company_id = str(uuid.uuid4())

    await conn.execute("""
        INSERT INTO managers (
            id, company_id, user_id, full_name, position,
            phone, email, is_owner, is_active, regions
        ) VALUES (
            $1, $2, $3, $4, $5,
            $6, $7, $8, $9, $10
        )
    """, manager_id, company_id, user_id, data["full_name"], data["position"],
         data["phone"], data["email"], is_owner, is_active, data["regions"])

await state.clear()
await message.answer("✅ Вы успешно зарегистрированы как менеджер.\n💳 Для активации доступа потребуется оплата. Функция подключения скоро будет доступна.")

@router.message(F.text == "❌ Отменить") async def cancel_registration(message: Message, state: FSMContext): await state.clear() await message.answer("❌ Регистрация отменена. Возврат в главное меню.")

