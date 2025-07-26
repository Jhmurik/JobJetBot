import asyncpg
import os

# 🔌 Подключение к базе данных
async def connect_to_db():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL не установлен в переменных окружения")
    return await asyncpg.create_pool(dsn=db_url)
