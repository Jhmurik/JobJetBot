from asyncpg import Pool

# 🔢 Подсчёт количества водителей
async def count_drivers(pool: Pool) -> int:
    try:
        async with pool.acquire() as conn:
            result = await conn.fetchval("SELECT COUNT(*) FROM drivers WHERE is_active = TRUE")
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

# 📦 Подсчёт количества вакансий
async def count_vacancies(pool: Pool) -> int:
    try:
        async with pool.acquire() as conn:
            result = await conn.fetchval("SELECT COUNT(*) FROM vacancies WHERE is_active = TRUE")
            return result or 0
    except Exception as e:
        print(f"Ошибка при подсчёте вакансий: {e}")
        return 0

# 💳 Подсчёт премиум-подписок водителей
async def count_premium_subs(pool: Pool) -> int:
    try:
        async with pool.acquire() as conn:
            result = await conn.fetchval("""
                SELECT COUNT(DISTINCT user_id) FROM payments
                WHERE payment_type = 'premium' AND role = 'driver'
            """)
            return result or 0
    except Exception as e:
        print(f"Ошибка при подсчёте премиум-подписок: {e}")
        return 0
