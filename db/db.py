# db/db.py
from asyncpg import Connection


# ✅ Активировать анкету водителя
async def activate_driver(conn: Connection, driver_id: int):
    await conn.execute(
        "UPDATE drivers SET is_active = TRUE WHERE id = $1",
        driver_id
    )


# ✅ Деактивировать анкету водителя
async def deactivate_driver(conn: Connection, driver_id: int):
    await conn.execute(
        "UPDATE drivers SET is_active = FALSE WHERE id = $1",
        driver_id
    )


# ✅ Проверить активность анкеты
async def is_driver_active(conn: Connection, driver_id: int) -> bool:
    result = await conn.fetchval(
        "SELECT is_active FROM drivers WHERE id = $1",
        driver_id
    )
    return result is True


# ✅ Сохранить компанию
async def save_company(conn: Connection, company_id: int, name: str, country: str, city: str, regions: list[str]):
    await conn.execute("""
        INSERT INTO companies (id, name, country, city, regions, created_at)
        VALUES ($1, $2, $3, $4, $5, CURRENT_TIMESTAMP)
        ON CONFLICT (id) DO UPDATE
        SET name = EXCLUDED.name,
            country = EXCLUDED.country,
            city = EXCLUDED.city,
            regions = EXCLUDED.regions
    """, company_id, name, country, city, regions)


# ✅ Сохранить менеджера
async def save_manager(conn: Connection, manager_id: int, full_name: str, phone: str, email: str, position: str, company_id: int, is_owner: bool):
    await conn.execute("""
        INSERT INTO managers (id, full_name, phone, email, position, company_id, is_owner, is_active, created_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7, TRUE, CURRENT_TIMESTAMP)
        ON CONFLICT (id) DO UPDATE
        SET full_name = EXCLUDED.full_name,
            phone = EXCLUDED.phone,
            email = EXCLUDED.email,
            position = EXCLUDED.position,
            company_id = EXCLUDED.company_id,
            is_owner = EXCLUDED.is_owner,
            is_active = TRUE
    """, manager_id, full_name, phone, email, position, company_id, is_owner)


# ✅ Активировать менеджера
async def activate_manager(conn: Connection, manager_id: int):
    await conn.execute(
        "UPDATE managers SET is_active = TRUE WHERE id = $1",
        manager_id
    )


# ✅ Сохранить платёж
async def save_payment(conn: Connection, user_id: int, role: str, amount: float, currency: str, payment_method: str, payment_type: str, description: str):
    await conn.execute("""
        INSERT INTO payments (user_id, role, amount, currency, payment_method, payment_type, description, created_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7, CURRENT_TIMESTAMP)
    """, user_id, role, amount, currency, payment_method, payment_type, description)


# ✅ Сохранить лог оплаты
async def save_payment_log(conn: Connection, payment_id: str, log: str):
    await conn.execute("""
        INSERT INTO payment_logs (payment_id, log, created_at)
        VALUES ($1, $2, CURRENT_TIMESTAMP)
    """, payment_id, log)


# ✅ Подсчёт количества водителей
async def count_drivers(conn: Connection) -> int:
    return await conn.fetchval("SELECT COUNT(*) FROM drivers")


# ✅ Подсчёт количества компаний
async def count_companies(conn: Connection) -> int:
    return await conn.fetchval("SELECT COUNT(*) FROM companies")
