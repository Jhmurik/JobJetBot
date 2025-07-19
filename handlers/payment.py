from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.cryptomus import create_payment_link
from asyncpg import Pool
from datetime import datetime
import uuid

router = Router()

# 💳 Команда "Купить подписку"
@router.message(F.text == "💳 Купить подписку")
async def start_payment(message: Message, state: FSMContext):
    user_id = message.from_user.id
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    # Определяем роль (driver / manager)
    async with pool.acquire() as conn:
        role = await get_user_role(conn, user_id)

    if not role:
        await message.answer("❌ Вы не зарегистрированы как водитель или менеджер.")
        return

    amount = 3.0 if role == "driver" else 25.0
    payment_type = "premium"

    link = await create_payment_link(user_id, role, amount, payment_type)
    await message.answer(
        f"💳 Для оплаты подписки на Premium ({amount}$ в USDT TRC20) нажмите на кнопку ниже:",
        reply_markup=None
    )
    await message.answer(link)

# 📌 Определить роль пользователя
async def get_user_role(conn: Pool, user_id: int) -> str | None:
    driver = await conn.fetchrow("SELECT id FROM drivers WHERE id = $1", user_id)
    if driver:
        return "driver"

    manager = await conn.fetchrow("SELECT user_id FROM managers WHERE user_id = $1", user_id)
    if manager:
        return "manager"

    return None
