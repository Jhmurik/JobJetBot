import pathlib
import asyncpg
from uuid import UUID

# 📥 Создание таблиц из schema.sql
async def create_tables(pool):
    schema_path = pathlib.Path("schema.sql")
    schema_sql = schema_path.read_text(encoding='utf-8')
    async with pool.acquire() as conn:
        await conn.execute(schema_sql)

# 🔌 Подключение к базе и создание таблиц
async def connect_to_db():
    from os import getenv
    db_url = getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("❌ DATABASE_URL не найден в переменных окружения")

    pool = await asyncpg.create_pool(dsn=db_url)
    await create_tables(pool)
    return pool

# 🔄 Управление статусом анкеты водителя
async def deactivate_driver(conn, driver_id: int):
    await conn.execute("UPDATE drivers SET is_active = FALSE WHERE id = $1", driver_id)

async def activate_driver(conn, driver_id: int):
    await conn.execute("UPDATE drivers SET is_active = TRUE WHERE id = $1", driver_id)

async def is_driver_active(conn, driver_id: int) -> bool:
    result = await conn.fetchrow("SELECT is_active FROM drivers WHERE id = $1", driver_id)
    return result["is_active"] if result else False

# 💾 Сохранение компании
async def save_company(pool, company_data: dict):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO companies (id, name, description, country, city, owner_id, regions, created_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, CURRENT_TIMESTAMP)
            ON CONFLICT (id) DO NOTHING
        """, UUID(company_data["id"]), company_data["name"], company_data["description"],
             company_data["country"], company_data["city"], company_data["owner_id"],
             company_data["regions"])

# 💾 Сохранение менеджера
async def save_manager(pool, manager_data: dict):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO managers (
                id, company_id, user_id, full_name, position,
                phone, email, company_name, company_country,
                company_city, is_owner, is_active, regions, created_at
            ) VALUES (
                $1, $2, $3, $4, $5,
                $6, $7, $8, $9,
                $10, $11, $12, $13, CURRENT_TIMESTAMP
            )
        """, UUID(manager_data["id"]), manager_data.get("company_id"),
             manager_data["user_id"], manager_data["full_name"], manager_data["position"],
             manager_data["phone"], manager_data["email"], manager_data.get("company_name"),
             manager_data.get("company_country"), manager_data.get("company_city"),
             manager_data["is_owner"], manager_data["is_active"], manager_data["regions"])

# 💳 Добавление платежа
async def save_payment(pool, payment_data: dict):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO payments (
                user_id, role, amount, currency,
                payment_method, payment_type, description, created_at
            ) VALUES (
                $1, $2, $3, $4,
                $5, $6, $7, CURRENT_TIMESTAMP
            )
        """, payment_data["user_id"], payment_data["role"], payment_data["amount"],
             payment_data["currency"], payment_data["payment_method"],
             payment_data["payment_type"], payment_data.get("description", ""))

# 📊 Статистика
async def count_drivers(pool):
    async with pool.acquire() as conn:
        result = await conn.fetchval("SELECT COUNT(*) FROM drivers")
        return result or 0

async def count_companies(pool):
    async with pool.acquire() as conn:
        result = await conn.fetchval("SELECT COUNT(*) FROM companies")
        return result or 0
