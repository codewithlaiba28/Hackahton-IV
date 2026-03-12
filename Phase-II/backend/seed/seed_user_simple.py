import uuid
from datetime import datetime
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import get_settings
from app.database import engine
import sqlalchemy

settings = get_settings()

API_KEY = "test_api_key_12345"

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.user import User, UserTier

async def seed_user():
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        try:
            # Check if user exists
            result = await session.execute(
                select(User).where(User.api_key == API_KEY)
            )
            existing = result.scalar_one_or_none()
            
            if not existing:
                new_user = User(
                    api_key=API_KEY,
                    email="test@example.com",
                    tier=UserTier.PREMIUM
                )
                session.add(new_user)
                await session.commit()
                print(f"Created user with API Key: {API_KEY}")
            else:
                print(f"User with API Key {API_KEY} already exists.")
        except Exception:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    from sqlalchemy import select
    asyncio.run(seed_user())
