import asyncio
import sys
import os
from pathlib import Path
from sqlalchemy import select

# Add parent directory to path
sys.path.insert(0, str(Path(os.getcwd())))

from app.database import engine
from app.models.chapter import Chapter

async def run():
    async with engine.begin() as conn:
        result = await conn.execute(select(Chapter))
        chapters = result.fetchall()
        print(f"DEBUG_START")
        print(f"CHAPTER_COUNT:{len(chapters)}")
        for ch in chapters:
            print(f"CHAPTER_ID:{ch.id}|TITLE:{ch.title}")
        print(f"DEBUG_END")

if __name__ == "__main__":
    asyncio.run(run())
