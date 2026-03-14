import asyncio
import sys
from pathlib import Path
from sqlalchemy import select

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.database import engine
from app.models.chapter import Chapter

async def run():
    async with engine.begin() as conn:
        result = await conn.execute(select(Chapter))
        chapters = result.fetchall()
        print(f"Total chapters: {len(chapters)}")
        for ch in chapters:
            print(f"ID: {ch.id}, Title: {ch.title}")

if __name__ == "__main__":
    asyncio.run(run())
