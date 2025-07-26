from asyncpg import Pool

# 💾 Сохранение информации о платеже
async def save_payment(pool: Pool, payment: dict):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO payments (user_id, role, amount, currency, payment_method, payment_type, description)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
        """, 
        payment["user_id"],
        payment["role"],
        payment["amount"],
        payment["currency"],
        payment["payment_method"],
        payment["payment_type"],
        payment["description"]
                          )
