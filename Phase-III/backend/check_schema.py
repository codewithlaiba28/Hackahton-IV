import asyncio
import os
from sqlalchemy import text
from app.database import engine

async def check_schema():
    async with engine.connect() as conn:
        print("Checking users table schema...")
        result = await conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users'"))
        columns = result.fetchall()
        for col in columns:
            print(f"Column: {col[0]}, Type: {col[1]}")

if __name__ == "__main__":
    asyncio.run(check_schema())
