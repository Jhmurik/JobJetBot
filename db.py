from uuid import uuid4

# 💾 Сохранение анкеты водителя
async def save_driver(pool, data: dict):
    # 🔄 Приведение к списку, если regions — строка
    regions = data.get("regions", [])
    if isinstance(regions, str):
        regions = [r.strip() for r in regions.split(",")]

    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO drivers (
                id,
                telegram_id,
                full_name,
                birth_date,
                citizenship,
                residence,
                license_type,
                experience,
                languages,
                documents,
                truck_type,
                employment_type,
                ready_to_depart,
                salary_expectation,
                regions,
                contacts,
                is_active,
                is_premium,
                created_at
            ) VALUES (
                $1, $2, $3, $4, $5,
                $6, $7, $8, $9, $10,
                $11, $12, $13, $14, $15,
                $16, TRUE, FALSE, CURRENT_TIMESTAMP
            )
            ON CONFLICT (telegram_id) DO UPDATE SET
                full_name = EXCLUDED.full_name,
                birth_date = EXCLUDED.birth_date,
                citizenship = EXCLUDED.citizenship,
                residence = EXCLUDED.residence,
                license_type = EXCLUDED.license_type,
                experience = EXCLUDED.experience,
                languages = EXCLUDED.languages,
                documents = EXCLUDED.documents,
                truck_type = EXCLUDED.truck_type,
                employment_type = EXCLUDED.employment_type,
                ready_to_depart = EXCLUDED.ready_to_depart,
                salary_expectation = EXCLUDED.salary_expectation,
                regions = EXCLUDED.regions,
                contacts = EXCLUDED.contacts,
                is_active = TRUE,
                updated_at = CURRENT_TIMESTAMP
        """,
        str(uuid4()),
        data["telegram_id"],
        data["full_name"],
        data["birth_date"],
        data["citizenship"],
        data["residence"],
        data["license_type"],
        data["experience"],
        data["languages"],
        data["documents"],
        data["truck_type"],
        data["employment_type"],
        data["ready_to_depart"],
        data["salary_expectation"],
        regions,
        data["contacts"]
                          )
