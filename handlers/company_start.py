from db import save_company  # ⚠️ добавим позже
from uuid import uuid4

@router.message(CompanyStart.name)
async def company_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CompanyStart.description)
    await message.answer("✏️ Введите *краткое описание* компании:", parse_mode="Markdown")

@router.message(CompanyStart.description)
async def company_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(CompanyStart.country)
    await message.answer("🌍 Введите страну регистрации:")

@router.message(CompanyStart.country)
async def company_country(message: Message, state: FSMContext):
    await state.update_data(country=message.text)
    await state.set_state(CompanyStart.city)
    await message.answer("🏙️ Введите город регистрации:")

@router.message(CompanyStart.city)
async def company_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)

    data = await state.get_data()
    owner_id = message.from_user.id
    company_id = str(uuid4())

    # Пример данных для сохранения
    company_data = {
        "id": company_id,
        "name": data["name"],
        "description": data["description"],
        "country": data["country"],
        "city": data["city"],
        "owner_id": owner_id,
    }

    # Сохраняем компанию в БД
    app = message.bot._ctx.get("application")
    pool = app["db"]
    await save_company(pool, company_data)

    await state.clear()
    await message.answer(f"✅ Компания успешно зарегистрирована!\n\n"
                         f"Ваш код подключения для менеджеров:\n\n"
                         f"<code>join_{company_id}</code>", parse_mode="HTML")
