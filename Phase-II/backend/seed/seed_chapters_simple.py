#!/usr/bin/env python3
"""
Simple seed script for course chapters.
Reads content from local filesystem and creates database entries.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.config import get_settings
from app.models import Chapter  # Import from models package to ensure all registered
from app.database import Base, engine

settings = get_settings()

# Chapter metadata (content read from files)
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
    # Use existing engine
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Content directory
    content_dir = Path(settings.LOCAL_CONTENT_PATH) / "chapters"

    async with async_session() as session:
        for chapter_data in CHAPTERS:
            # Check if chapter already exists
            result = await session.execute(
                select(Chapter).where(Chapter.id == chapter_data["id"])
            )
            existing = result.scalar_one_or_none()

            if existing:
                print(f"Chapter {chapter_data['id']} already exists, skipping...")
                continue

            # Verify content file exists
            content_file = content_dir / chapter_data["id"] / "content.md"
            if not content_file.exists():
                print(f"Warning: Content file not found for {chapter_data['id']}")
                continue

            # Create R2 content key (local filesystem path)
            r2_key = f"chapters/{chapter_data['id']}/content.md"

            # Create chapter in database
            chapter = Chapter(
                id=chapter_data["id"],
                title=chapter_data["title"],
                difficulty=chapter_data["difficulty"],
                estimated_read_min=chapter_data["estimated_read_min"],
                is_free=chapter_data["is_free"],
                sequence_order=chapter_data["sequence_order"],
                prev_chapter_id=chapter_data["prev_chapter_id"],
                next_chapter_id=chapter_data["next_chapter_id"],
                r2_content_key=r2_key,
            )
            session.add(chapter)
            print(f"Added chapter to DB: {chapter_data['title']}")

        # Commit all changes
        await session.commit()
        print(f"\nSuccessfully seeded {len(CHAPTERS)} chapters!")
        print(f"Content directory: {content_dir.absolute()}")


if __name__ == "__main__":
    print("Seeding chapters...")
    asyncio.run(seed_chapters())
