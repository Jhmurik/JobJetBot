import asyncpg
import os

# 🔌 Подключение к базе данных
async def connect_to_db():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL не установлен в переменных окружения")
    return await asyncpg.create_pool(dsn=db_url)

# ✅ Экспортируемые функции (импортируются из db.py)
from .db import (
    activate_driver,
    deactivate_driver,
    is_driver_active,
    activate_manager,
    save_company,
    save_manager,
    save_payment,
    save_payment_log,
    count_drivers,
    count_companies
)
