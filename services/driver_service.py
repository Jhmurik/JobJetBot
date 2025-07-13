# services/driver_service.py

async def save_driver(data: dict, pool):
    query = """
        INSERT INTO drivers (
            full_name, phone, experience,
            license_type, languages, city,
            ready_to_work
        ) VALUES ($1, $2, $3, $4, $5, $6, $7)
    """

    await pool.execute(
        query,
        data.get("full_name"),
        data.get("contacts"),
        data.get("experience"),
        data.get("license_type"),
        data.get("languages").split(",") if data.get("languages") else [],
        data.get("residence"),
        True
    )
