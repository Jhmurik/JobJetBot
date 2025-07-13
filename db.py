import pathlib
import asyncpg

# Функция: создать таблицы из schema.sql
async def create_tables(pool):
    schema_path = pathlib.Path("schema.sql")
    schema_sql = schema_path.read_text(encoding='utf-8')
    async with pool.acquire() as conn:
        await conn.execute(schema_sql)

# Функция: подключиться к базе (и создать таблицы)
async def connect_to_db():
    from os import getenv
    db_url = getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("❌ DATABASE_URL не найден в переменных окружения")

    pool = await asyncpg.create_pool(dsn=db_url)
    await create_tables(pool)
    return pool
