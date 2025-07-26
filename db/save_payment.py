from asyncpg import Pool
from datetime import datetime

# 💾 Сохранение информации о платеже
async def save_payment(pool: Pool, payment: dict):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO payments (
                user_id, role, amount, currency,
                payment_method, payment_type, description, created_at
            ) VALUES (
                $1, $2, $3, $4,
                $5, $6, $7, $8
            )
        """,
        payment.get("user_id"),
        payment.get("role"),
        payment.get("amount"),
        payment.get("currency", "USDT"),
        payment.get("payment_method", "cryptomus"),
        payment.get("payment_type", "premium"),
        payment.get("description", ""),
        datetime.utcnow()
                          )
