import asyncio
import traceback
import sys
import os

# Ensure the backend directory is in the path
sys.path.insert(0, os.getcwd())

async def main():
    import traceback
    try:
        from app.config import settings
        from app.database import engine
        from app.models.user import User, UserTier
        from sqlalchemy.ext.asyncio import AsyncSession
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import select
        
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            print("Checking if user exists...")
            api_key = "test_api_key_12345"
            result = await session.execute(
                select(User).where(User.api_key == api_key)
            )
            existing = result.scalar_one_or_none()
            if existing:
                print(f"Found user: {existing.email}")
            else:
                print("Creating new user...")
                new_user = User(
                    api_key=api_key,
                    email="test@example.com",
                    tier=UserTier.PREMIUM
                )
                session.add(new_user)
                await session.commit()
                print("User created successfully")
        
        print("--- DEBUG SESSION COMPLETED ---")
    except Exception:
        print("Failure Traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
