"""Seed chapters using ORM with proper engine from app.database."""
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.database import engine
from app.models.chapter import Chapter
from app.models.quiz import QuizQuestion
import uuid

CHAPTERS = [
    {"id": "ch-001", "title": "Introduction to AI Agents", "difficulty": "beginner", "estimated_read_min": 15, "is_free": True, "sequence_order": 1, "prev_chapter_id": None, "next_chapter_id": "ch-002", "r2_content_key": "chapters/ch-001.md"},
    {"id": "ch-002", "title": "Agent Architecture Patterns", "difficulty": "beginner", "estimated_read_min": 20, "is_free": True, "sequence_order": 2, "prev_chapter_id": "ch-001", "next_chapter_id": "ch-003", "r2_content_key": "chapters/ch-002.md"},
    {"id": "ch-003", "title": "Tool Use and Function Calling", "difficulty": "intermediate", "estimated_read_min": 25, "is_free": True, "sequence_order": 3, "prev_chapter_id": "ch-002", "next_chapter_id": "ch-004", "r2_content_key": "chapters/ch-003.md"},
    {"id": "ch-004", "title": "Memory and State Management", "difficulty": "intermediate", "estimated_read_min": 20, "is_free": False, "sequence_order": 4, "prev_chapter_id": "ch-003", "next_chapter_id": "ch-005", "r2_content_key": "chapters/ch-004.md"},
    {"id": "ch-005", "title": "Multi-Agent Systems", "difficulty": "advanced", "estimated_read_min": 30, "is_free": False, "sequence_order": 5, "prev_chapter_id": "ch-004", "next_chapter_id": None, "r2_content_key": "chapters/ch-005.md"},
]

QUIZZES = [
    {
        "chapter_id": "ch-001",
        "questions": [
            {
                "question_text": "What are the three key components of an AI agent?",
                "question_type": "mcq",
                "options": ["Input, Process, Output", "Perception, Decision Making, Action", "Sensors, CPU, Actuators", "Data, Algorithm, Result"],
                "correct_answer": "Perception, Decision Making, Action",
                "explanation": "AI agents perceive their environment, make decisions based on that perception, and take actions to achieve goals."
            }
        ]
    }
]

async def main():
    # Use original pooler URL but with statement_cache_size=0
    from app.config import get_settings
    settings = get_settings()
    db_url = settings.DATABASE_URL
    from sqlalchemy.ext.asyncio import create_async_engine
    engine = create_async_engine(db_url, connect_args={"ssl": True, "statement_cache_size": 0})
    
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        # Seed Chapters
        for ch_data in CHAPTERS:
            result = await session.execute(select(Chapter).where(Chapter.id == ch_data["id"]))
            existing = result.scalar_one_or_none()
            if existing:
                print(f"Chapter {ch_data['id']} already exists")
                continue
            chapter = Chapter(**ch_data)
            session.add(chapter)
            print(f"Added chapter: {ch_data['title']}")
        
        # Seed Quizzes
        for quiz_data in QUIZZES:
            chapter_id = quiz_data["chapter_id"]
            for i, q in enumerate(quiz_data["questions"]):
                result = await session.execute(select(QuizQuestion).where(QuizQuestion.chapter_id == chapter_id, QuizQuestion.question_text == q["question_text"]))
                if result.scalar_one_or_none():
                    print(f"Quiz already exists for {chapter_id}")
                    continue
                question = QuizQuestion(
                    id=uuid.uuid4(),
                    chapter_id=chapter_id,
                    question_text=q["question_text"],
                    question_type=q["question_type"],
                    options=q["options"],
                    correct_answer=q["correct_answer"],
                    explanation=q["explanation"],
                    sequence_order=i + 1
                )
                session.add(question)
                print(f"Added quiz for {chapter_id}")
        
        await session.commit()
    print("Seeding complete!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
