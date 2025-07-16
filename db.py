import pathlib
import asyncpg

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
