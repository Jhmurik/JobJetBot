from asyncpg import Pool

# 🔢 Подсчёт количества водителей
async def count_drivers(pool: Pool) -> int:
    try:
        async with pool.acquire() as conn:
            result = await conn.fetchval("SELECT COUNT(*) FROM drivers")
            return result or 0
    except Exception as e:
        print(f"Ошибка при подсчёте водителей: {e}")
        return 0

# 🔢 Подсчёт количества компаний
async def count_companies(pool: Pool) -> int:
    try:
        async with pool.acquire() as conn:
            result = await conn.fetchval("SELECT COUNT(*) FROM companies")
            return result or 0
    except Exception as e:
        print(f"Ошибка при подсчёте компаний: {e}")
        return 0
