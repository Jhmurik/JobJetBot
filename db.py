import pathlib

async def create_tables(pool):
    schema_path = pathlib.Path("schema.sql")
    async with pool.acquire() as conn:
        with schema_path.open("r") as f:
            await conn.execute(f.read())
