"""NUKE THE DATABASE."""
import asyncio
import sys, os
sys.path.insert(0, os.getcwd())

async def main():
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy import text
    
    db_url = "postgresql+asyncpg://neondb_owner:npg_B4phOVN7TwMZ@ep-twilight-bread-adhpvbz1-pooler.c-2.us-east-1.aws.neon.tech/neondb"
    engine = create_async_engine(db_url, echo=False, connect_args={"ssl": True, "statement_cache_size": 0})
    
    async with engine.begin() as conn:
        print("Dropping all tables...")
        # Get all table names
        result = await conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
        tables = [row[0] for row in result.fetchall()]
        for table in tables:
            print(f"  Dropping table {table}...")
            await conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
            
        print("Dropping all custom types...")
        # Get all custom types
        result = await conn.execute(text("SELECT typname FROM pg_type WHERE typtype = 'e'"))
        types = [row[0] for row in result.fetchall()]
        for t in types:
            print(f"  Dropping type {t}...")
            await conn.execute(text(f"DROP TYPE IF EXISTS {t} CASCADE"))
            
        print("Finalizing...")
        await conn.execute(text("COMMIT"))

    await engine.dispose()
    print("Database Nuked Successfully!")

asyncio.run(main())
