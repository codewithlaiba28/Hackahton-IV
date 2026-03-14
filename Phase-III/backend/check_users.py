import asyncio
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.user import User

async def check_users():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User))
        users = result.scalars().all()
        print(f"Total users: {len(users)}")
        for u in users:
            print(f"USER_DATA_START|{u.email}|{u.name}|{u.api_key}|{u.tier}|USER_DATA_END")

if __name__ == '__main__':
    asyncio.run(check_users())
