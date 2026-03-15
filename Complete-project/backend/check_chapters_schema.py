import asyncio
from sqlalchemy import text
from app.database import engine

async def check_schema():
    async with engine.connect() as conn:
        result = await conn.execute(text("""
            SELECT column_name, data_type, character_maximum_length 
            FROM information_schema.columns 
            WHERE table_name = 'chapters'
        """))
        for row in result:
            print(row)

if __name__ == "__main__":
    asyncio.run(check_schema())
