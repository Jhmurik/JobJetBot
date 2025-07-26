# db/db.py

async def activate_driver(conn, driver_id: int):
    await conn.execute(
        "UPDATE drivers SET is_active = TRUE WHERE id = $1",
        driver_id
    )

# При необходимости добавь сюда и другие нужные функции
