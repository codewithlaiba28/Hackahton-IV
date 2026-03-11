import uuid
from datetime import datetime
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import get_settings
from sqlalchemy.ext.asyncio import create_async_engine
import sqlalchemy

settings = get_settings()

API_KEY = "test_api_key_12345"

async def seed_user():
    engine = create_async_engine(settings.DATABASE_URL)
    async with engine.connect() as conn:
        # Check if user exists
        result = await conn.execute(
            sqlalchemy.text("SELECT id FROM users WHERE api_key = :api_key"),
            {"api_key": API_KEY}
        )
        existing = result.first()
        if not existing:
            user_id = str(uuid.uuid4()).replace('-', '')
            await conn.execute(
                sqlalchemy.text(
                    "INSERT INTO users (id, api_key, email, tier, created_at) "
                    "VALUES (:id, :api_key, :email, 'premium', :now)"
                ),
                {"id": user_id, "api_key": API_KEY, "email": "test@example.com", "now": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}
            )
            await conn.commit()
            print(f"Created user with API Key: {API_KEY}")
        else:
            print(f"User with API Key {API_KEY} already exists.")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(seed_user())
