# utils/stats.py

async def count_drivers(pool):
    async with pool.acquire() as conn:
        result = await conn.fetchval("SELECT COUNT(*) FROM drivers")
        return result or 0
