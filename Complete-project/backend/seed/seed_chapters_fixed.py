#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.config import get_settings
from app.models.chapter import Chapter
from app.database import Base

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
        "content": "# Introduction to AI Agents\n\nWhat is an AI Agent?\n\nAn AI Agent is an autonomous software system that can perceive its environment, make decisions, and take actions to achieve specific goals."
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
        "content": "# Claude Agent SDK\n\n## Overview\n\nThe Claude Agent SDK provides a powerful framework for building AI agents powered by Anthropic's Claude models."
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
        "content": "# MCP Basics\n\n## What is Model Context Protocol (MCP)?\n\nModel Context Protocol (MCP) is an open standard that enables AI agents to interact with external tools, data sources, and services through a unified interface."
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
        "content": "# Agent Skills\n\n## What are Agent Skills?\n\nAgent Skills are predefined capabilities that teach AI agents how to perform specific tasks consistently."
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
        "content": "# Agent Factory Architecture\n\n## Overview\n\nThe Agent Factory Architecture is a systematic approach to building AI agents at scale."
    }
]

async def seed_chapters():
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    content_dir = Path(__file__).parent.parent / "content" / "chapters"
    content_dir.mkdir(parents=True, exist_ok=True)

    async with async_session() as session:
        for chapter_data in CHAPTERS:
            result = await session.execute(select(Chapter).where(Chapter.id == chapter_data["id"]))
            existing = result.scalar_one_or_none()
            if existing: continue

            # Save content to local filesystem
            chapter_content_dir = content_dir / chapter_data["id"]
            chapter_content_dir.mkdir(parents=True, exist_ok=True)
            content_file = chapter_content_dir / "content.md"
            content_file.write_text(chapter_data["content"], encoding='utf-8')

            db_data = {k: v for k, v in chapter_data.items() if k != 'content'}
            chapter = Chapter(**db_data, r2_content_key=f"chapters/{chapter_data['id']}/content.md")
            session.add(chapter)
        
        await session.commit()
        print(f"Successfully seeded {len(CHAPTERS)} chapters!")

if __name__ == "__main__":
    asyncio.run(seed_chapters())
