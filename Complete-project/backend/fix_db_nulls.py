import asyncio
from sqlalchemy import text
from app.database import engine

async def fix_nullability():
    async with engine.connect() as conn:
        print("Fixing nullability...")
        await conn.execute(text("ALTER TABLE users ALTER COLUMN password_salt DROP NOT NULL"))
        await conn.execute(text("ALTER TABLE users ALTER COLUMN hashed_password DROP NOT NULL"))
        await conn.execute(text("ALTER TABLE users ALTER COLUMN name DROP NOT NULL"))
        await conn.commit()
        print("Done.")

if __name__ == "__main__":
    asyncio.run(fix_nullability())
