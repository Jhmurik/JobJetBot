import uuid
from db import connect_to_db  # если ещё не импортировано

@router.message(F.text == "✅ Подтвердить регистрацию")
async def confirm_manager_registration(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    manager_id = str(uuid.uuid4())
    company_id = None

    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    async with pool.acquire() as conn:
        # Если менеджер указал компанию — пробуем её найти или создаём
        if data['company_name'].lower() != 'нет':
            company_id = str(uuid.uuid4())
            await conn.execute("""
                INSERT INTO companies (id, name, description, country, city, owner_id, regions)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                ON CONFLICT (id) DO NOTHING
            """, company_id, data['company_name'], None, data['company_country'], data['company_city'], user_id, data['regions'])
        else:
            company_id = None

        # Сохраняем менеджера
        await conn.execute("""
            INSERT INTO managers (
                id, company_id, user_id, full_name,
                position, phone, email,
                is_owner, is_active, regions
            )
            VALUES ($1, $2, $3, $4,
                    $5, $6, $7,
                    TRUE, FALSE, $8)
        """, manager_id, company_id, user_id, data['full_name'],
             data['position'], data['phone'], data['email'], data['regions'])

    await state.clear()
    await message.answer("✅ Вы успешно зарегистрированы как менеджер!\nПодключение Premium-доступа доступно через меню.")
