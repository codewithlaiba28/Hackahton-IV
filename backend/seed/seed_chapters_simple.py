#!/usr/bin/env python3
"""
Simple seed script for course chapters.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.config import get_settings
from app.models.chapter import Chapter

settings = get_settings()

CHAPTERS = [
    {
        "id": "ch-001",
        "title": "Introduction to AI Agents",
        "difficulty": "beginner",
        "estimated_read_min": 15,
        "is_free": True,
        "sequence_order": 1,
        "prev_chapter_id": None,
        "next_chapter_id": "ch-002",
    },
    {
        "id": "ch-002",
        "title": "Claude Agent SDK",
        "difficulty": "intermediate",
        "estimated_read_min": 20,
        "is_free": True,
        "sequence_order": 2,
        "prev_chapter_id": "ch-001",
        "next_chapter_id": "ch-003",
    },
    {
        "id": "ch-003",
        "title": "MCP Basics",
        "difficulty": "intermediate",
        "estimated_read_min": 18,
        "is_free": True,
        "sequence_order": 3,
        "prev_chapter_id": "ch-002",
        "next_chapter_id": "ch-004",
    },
    {
        "id": "ch-004",
        "title": "Agent Skills",
        "difficulty": "advanced",
        "estimated_read_min": 25,
        "is_free": False,
        "sequence_order": 4,
        "prev_chapter_id": "ch-003",
        "next_chapter_id": "ch-005",
    },
    {
        "id": "ch-005",
        "title": "Agent Factory Architecture",
        "difficulty": "advanced",
        "estimated_read_min": 22,
        "is_free": False,
        "sequence_order": 5,
        "prev_chapter_id": "ch-004",
        "next_chapter_id": None,
    },
]


async def seed_chapters():
    """Seed chapters into the database."""
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    content_dir = Path(settings.LOCAL_CONTENT_PATH) / "chapters"
    content_dir.mkdir(parents=True, exist_ok=True)

    async with async_session() as session:
        for chapter_data in CHAPTERS:
            result = await session.execute(
                select(Chapter).where(Chapter.id == chapter_data["id"])
            )
            existing = result.scalar_one_or_none()

            if existing:
                print(f"Chapter {chapter_data['id']} already exists, skipping...")
                continue

            chapter_content_dir = content_dir / chapter_data["id"]
            chapter_content_dir.mkdir(parents=True, exist_ok=True)
            content_file = chapter_content_dir / "content.md"
            
            if not content_file.exists():
                content_file.write_text(f"# {chapter_data['title']}\n\nContent coming soon...", encoding='utf-8')
            print(f"Saved content for chapter: {chapter_data['id']}")

            chapter = Chapter(**chapter_data)
            session.add(chapter)
            print(f"Added chapter to DB: {chapter_data['title']}")

        await session.commit()
        print(f"\nSuccessfully seeded {len(CHAPTERS)} chapters!")
        print(f"Content stored in: {content_dir.absolute()}")


if __name__ == "__main__":
    print("Seeding chapters...")
    asyncio.run(seed_chapters())
