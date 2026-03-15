import asyncio
import os
from sqlalchemy import text
from app.database import engine

async def check_schema():
    async with engine.connect() as conn:
        print("--- Tables ---")
        res_tables = await conn.execute(text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'"))
        tables = res_tables.fetchall()
        for t in tables:
            print(f"Table: {t[0]}")
            
        print("\n--- Users Table Columns ---")
        result = await conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users'"))
        columns = result.fetchall()
        for col in columns:
            print(f"Column: {col[0]}, Type: {col[1]}")
            
        print("\n--- Alembic Version ---")
        try:
            res_ver = await conn.execute(text("SELECT version_num FROM alembic_version"))
            ver = res_ver.scalar()
            print(f"Version: {ver}")
        except Exception as e:
            print("No alembic_version table.")

if __name__ == "__main__":
    asyncio.run(check_schema())
