@router.message(DriverForm.confirmation)
async def process_confirmation(message: Message, state: FSMContext):
    if message.text.lower() == "подтверждаю":
        data = await state.get_data()
        pool = message.bot.get("db")

        async with pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO drivers (
                    full_name, birth_date, citizenship, residence, license_type,
                    experience, languages, documents, truck_type, employment_type,
                    ready_to_work, contacts
                ) VALUES (
                    $1, $2, $3, $4, $5,
                    $6, $7, $8, $9, $10,
                    TRUE, $11
                )
            """,
            data.get("full_name"),
            data.get("birth_date"),
            data.get("citizenship"),
            data.get("residence"),
            data.get("license_type"),
            data.get("experience"),
            [lang.strip() for lang in data.get("languages", "").split(",")],
            data.get("documents"),
            data.get("truck_type"),
            data.get("employment_type"),
            data.get("contacts"))

        await message.answer("✅ Спасибо! Анкета успешно сохранена.")
        await state.clear()
    else:
        await message.answer("❌ Анкета не подтверждена. Чтобы начать заново — напишите 'заполнить анкету'.")
        await state.clear()
