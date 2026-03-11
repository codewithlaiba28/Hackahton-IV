#!/usr/bin/env python3
"""
Simple seed script - insert chapters without FK constraints first.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import get_settings
from sqlalchemy.ext.asyncio import create_async_engine

settings = get_settings()

CHAPTERS = [
    ("ch-001", "Introduction to AI Agents", "beginner", 15, True, 1, None, None),
    ("ch-002", "Claude Agent SDK", "intermediate", 20, True, 2, None, None),
    ("ch-003", "MCP Basics", "intermediate", 18, True, 3, None, None),
    ("ch-004", "Agent Skills", "advanced", 25, False, 4, None, None),
    ("ch-005", "Agent Factory Architecture", "advanced", 22, False, 5, None, None),
]

# FK updates after all chapters inserted (id, prev, next)
FK_UPDATES = [
    ("ch-001", None, "ch-002"),
    ("ch-002", "ch-001", "ch-003"),
    ("ch-002", "ch-001", "ch-003"),
    ("ch-003", "ch-002", "ch-004"),
    ("ch-004", "ch-003", "ch-005"),
    ("ch-005", "ch-004", None),
]


async def seed_chapters():
    """Seed chapters using raw SQL."""
    engine = create_async_engine(settings.DATABASE_URL)
    
    content_dir = Path(settings.LOCAL_CONTENT_PATH) / "chapters"
    content_dir.mkdir(parents=True, exist_ok=True)

    async with engine.connect() as conn:
        # Insert all chapters first without FK
        for chapter_id, title, difficulty, read_min, is_free, seq, _, _ in CHAPTERS:
            result = await conn.execute(
                sys.modules['sqlalchemy'].text(
                    "SELECT id FROM chapters WHERE id = :id"
                ),
                {"id": chapter_id}
            )
            existing = result.first()

            if existing:
                print(f"Chapter {chapter_id} already exists, skipping...")
                continue

            await conn.execute(
                sys.modules['sqlalchemy'].text(
                    """INSERT INTO chapters 
                    (id, title, difficulty, estimated_read_min, is_free, sequence_order, prev_chapter_id, next_chapter_id, r2_content_key, created_at)
                    VALUES (:id, :title, :difficulty, :read_min, :is_free, :seq, NULL, NULL, :r2_key, CURRENT_TIMESTAMP)"""
                ),
                {
                    "id": chapter_id,
                    "title": title,
                    "difficulty": difficulty,
                    "read_min": read_min,
                    "is_free": is_free,
                    "seq": seq,
                    "r2_key": f"chapters/{chapter_id}/content.md"
                }
            )

            # Create local content file
            chapter_content_dir = content_dir / chapter_id
            chapter_content_dir.mkdir(parents=True, exist_ok=True)
            content_file = chapter_content_dir / "content.md"
            
            if not content_file.exists():
                content_file.write_text(f"# {title}\n\nContent coming soon...", encoding='utf-8')
            
            print(f"Added chapter: {title}")

        # Update FK constraints
        for fk_data in FK_UPDATES:
            chapter_id = fk_data[0]
            prev_id = fk_data[1] if len(fk_data) > 1 else None
            next_id = fk_data[2] if len(fk_data) > 2 else None
            
            await conn.execute(
                sys.modules['sqlalchemy'].text(
                    "UPDATE chapters SET prev_chapter_id = :prev, next_chapter_id = :next WHERE id = :id"
                ),
                {"id": chapter_id, "prev": prev_id, "next": next_id}
            )

        await conn.commit()
        print(f"\nSuccessfully seeded {len(CHAPTERS)} chapters!")
        print(f"Content stored in: {content_dir.absolute()}")

    await engine.dispose()


if __name__ == "__main__":
    import sqlalchemy
    print("Seeding chapters...")
    asyncio.run(seed_chapters())
