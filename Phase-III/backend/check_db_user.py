
import asyncio
import uuid
from sqlalchemy import select
from app.database import SessionLocal, engine
from app.models.user import User

async def check_user_tier(email):
    async with SessionLocal() as db:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user:
            print(f"USER_FOUND: {user.email}")
            print(f"TIER: {user.tier}")
            print(f"API_KEY: {user.api_key}")
        else:
            print(f"USER_NOT_FOUND: {email}")

if __name__ == "__main__":
    email = "laibakhan@gmail.com" # From screenshot
    asyncio.run(check_user_tier(email))
