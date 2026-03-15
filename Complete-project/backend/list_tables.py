import asyncio
from sqlalchemy import text
from app.database import engine

async def list_tables():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'"))
        for row in result:
            print(row)

if __name__ == "__main__":
    asyncio.run(list_tables())
