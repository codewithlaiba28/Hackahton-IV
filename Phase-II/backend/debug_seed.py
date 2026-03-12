"""Test seeding with fresh engine and statement_cache_size=0."""
import asyncio
import sys, os
sys.path.insert(0, os.getcwd())

async def main():
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import text, select
    
    db_url = "postgresql+asyncpg://neondb_owner:npg_B4phOVN7TwMZ@ep-twilight-bread-adhpvbz1-pooler.c-2.us-east-1.aws.neon.tech/neondb"
    engine = create_async_engine(db_url, echo=False, connect_args={"ssl": True, "statement_cache_size": 0})
    
    output = []
    try:
        async with engine.connect() as conn:
            # Check enum
            result = await conn.execute(text("SELECT unnest(enum_range(NULL::usertier))"))
            rows = result.fetchall()
            output.append("Enum values: " + str([r[0] for r in rows]))
            
            # Check users
            result = await conn.execute(text("SELECT count(*) FROM users"))
            output.append(f"Users: {result.scalar()}")
            
            # Try direct insert with cast
            import uuid
            from datetime import datetime
            uid = uuid.uuid4()
            await conn.execute(
                text("INSERT INTO users (id, api_key, email, tier, created_at) VALUES (:id, :key, :email, :tier::usertier, :now)"),
                {"id": uid, "key": "test_api_key_12345", "email": "test@example.com", "tier": "premium", "now": datetime.utcnow()}
            )
            await conn.commit()
            output.append("INSERT successful!")
            
            # Verify
            result = await conn.execute(text("SELECT email, tier FROM users"))
            rows = result.fetchall()
            for r in rows:
                output.append(f"  {r[0]} / {r[1]}")
    except Exception as e:
        import traceback
        output.append(f"ERROR: {type(e).__name__}: {e}")
        output.append(traceback.format_exc())
    
    await engine.dispose()
    
    with open("debug_output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    print("Done - check debug_output.txt")

asyncio.run(main())
