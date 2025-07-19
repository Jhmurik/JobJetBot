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

# 💾 Сохранение компании в БД
async def save_company(pool, company_data: dict):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO companies (id, name, description, country, city, owner_id, created_at)
            VALUES ($1, $2, $3, $4, $5, $6, CURRENT_TIMESTAMP)
            ON CONFLICT (id) DO NOTHING
        """, UUID(company_data["id"]), company_data["name"], company_data["description"],
             company_data["country"], company_data["city"], company_data["owner_id"])
