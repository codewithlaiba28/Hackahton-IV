import asyncio
import os
from sqlalchemy import text, create_engine
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://neondb_owner:npg_B4phOVN7TwMZ@ep-twilight-bread-adhpvbz1-pooler.c-2.us-east-1.aws.neon.tech/neondb"

async def check_schema():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.connect() as conn:
        print("\n--- Users Table Columns ---")
        result = await conn.execute(text("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'users'"))
        columns = result.fetchall()
        for col in columns:
            print(f"Column: {col[0]}, Type: {col[1]}, Nullable: {col[2]}")

if __name__ == "__main__":
    asyncio.run(check_schema())
