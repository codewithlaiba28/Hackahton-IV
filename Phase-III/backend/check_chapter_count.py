import asyncio
from sqlalchemy import text
from app.database import engine

async def check_chapters():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT count(*) FROM chapters"))
        count = result.scalar()
        print(f"Chapters count: {count}")

if __name__ == "__main__":
    asyncio.run(check_chapters())
