import asyncio
import os
import sys
from pathlib import Path
from sqlalchemy import select

# Add current directory to path
sys.path.insert(0, os.getcwd())

from app.database import engine
from app.models.user import User

async def run():
    async with engine.begin() as conn:
        result = await conn.execute(select(User).limit(1))
        user = result.fetchone()
        if user:
            print(f"API_KEY:{user.api_key}")
        else:
            print("No user found")

if __name__ == "__main__":
    asyncio.run(run())
