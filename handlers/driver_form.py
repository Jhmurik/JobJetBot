@router.message(DriverForm.confirmation)
async def process_confirmation(message: Message, state: FSMContext):
    if message.text.lower() == "подтверждаю":
        data = await state.get_data()
        pool = message.bot.get("pool")

        async with pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO drivers (
                    full_name, birth_date, citizenship, residence, license_type,
                    experience, languages, documents, truck_type, employment_type,
                    ready_to_work, contacts
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, TRUE, $11)
            """, data["full_name"], data["birth_date"], data["citizenship"],
                 data["residence"], data["license_type"], data["experience"],
                 data["languages"], data["documents"], data["truck_type"],
                 data["employment_type"], data["contacts"])

        await message.answer("✅ Спасибо! Анкета успешно сохранена.")
        await state.clear()
    else:
        await message.answer("Анкета не подтверждена. Чтобы начать заново — напишите 'заполнить анкету'.")
        await state.clear()
