"""
Test fixtures for Course Companion FTE backend.
Provides async test fixtures, test DB setup, and auth fixtures.
"""

import asyncio
import pytest
import uuid
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text

from app.database import Base, get_db
from app.config import get_settings
from app.models.user import User, UserTier
from app.models.chapter import Chapter
from app.models.quiz import QuizQuestion
from app.models.progress import ChapterProgress

# Test settings
TEST_DATABASE_URL = "postgresql+asyncpg://test:test@localhost:5432/test_course_companion"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Drop all tables after tests
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session with rollback after each test."""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    
    async with async_session() as session:
        # Begin transaction
        await session.begin()
        yield session
        # Rollback after test
        await session.rollback()


@pytest.fixture
async def free_user(db_session: AsyncSession) -> User:
    """Create a free tier test user."""
    user = User(
        id=uuid.uuid4(),
        api_key="test_free_api_key_12345678901234567890",
        email="free_user@test.com",
        tier=UserTier.FREE
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def premium_user(db_session: AsyncSession) -> User:
    """Create a premium tier test user."""
    user = User(
        id=uuid.uuid4(),
        api_key="test_premium_api_key_123456789012345678",
        email="premium_user@test.com",
        tier=UserTier.PREMIUM
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def sample_chapters(db_session: AsyncSession) -> list:
    """Create sample chapters for testing."""
    chapters = [
        Chapter(
            id="ch-001",
            title="Introduction to AI Agents",
            difficulty="beginner",
            estimated_read_min=15,
            is_free=True,
            sequence_order=1,
            prev_chapter_id=None,
            next_chapter_id="ch-002",
            r2_content_key="chapters/ch-001/content.md"
        ),
        Chapter(
            id="ch-002",
            title="Claude Agent SDK",
            difficulty="intermediate",
            estimated_read_min=20,
            is_free=True,
            sequence_order=2,
            prev_chapter_id="ch-001",
            next_chapter_id="ch-003",
            r2_content_key="chapters/ch-002/content.md"
        ),
        Chapter(
            id="ch-003",
            title="MCP Basics",
            difficulty="intermediate",
            estimated_read_min=18,
            is_free=True,
            sequence_order=3,
            prev_chapter_id="ch-002",
            next_chapter_id="ch-004",
            r2_content_key="chapters/ch-003/content.md"
        ),
        Chapter(
            id="ch-004",
            title="Agent Skills",
            difficulty="advanced",
            estimated_read_min=25,
            is_free=False,
            sequence_order=4,
            prev_chapter_id="ch-003",
            next_chapter_id="ch-005",
            r2_content_key="chapters/ch-004/content.md"
        ),
        Chapter(
            id="ch-005",
            title="Agent Factory Architecture",
            difficulty="advanced",
            estimated_read_min=22,
            is_free=False,
            sequence_order=5,
            prev_chapter_id="ch-004",
            next_chapter_id=None,
            r2_content_key="chapters/ch-005/content.md"
        ),
    ]
    
    for chapter in chapters:
        db_session.add(chapter)
    
    await db_session.commit()
    return chapters


@pytest.fixture
async def sample_quiz_questions(db_session: AsyncSession) -> list:
    """Create sample quiz questions for testing."""
    questions = [
        QuizQuestion(
            id=uuid.uuid4(),
            chapter_id="ch-001",
            question_text="What are the three key components of an AI agent?",
            question_type="mcq",
            options=[
                "Input, Process, Output",
                "Perception, Decision Making, Action",
                "Sensors, CPU, Actuators"
            ],
            correct_answer="Perception, Decision Making, Action",
            explanation="AI agents perceive their environment, make decisions, and take actions.",
            sequence_order=1
        ),
        QuizQuestion(
            id=uuid.uuid4(),
            chapter_id="ch-001",
            question_text="A simple reflex agent responds directly to current percepts.",
            question_type="true_false",
            options=["True", "False"],
            correct_answer="True",
            explanation="Simple reflex agents use condition-action rules based only on current percepts.",
            sequence_order=2
        ),
    ]
    
    for question in questions:
        db_session.add(question)
    
    await db_session.commit()
    return questions


@pytest.fixture
def headers_free_user(free_user: User) -> dict:
    """Get headers for free user authentication."""
    return {"X-API-Key": free_user.api_key}


@pytest.fixture
def headers_premium_user(premium_user: User) -> dict:
    """Get headers for premium user authentication."""
    return {"X-API-Key": premium_user.api_key}


@pytest.fixture
def invalid_headers() -> dict:
    """Get headers with invalid API key."""
    return {"X-API-Key": "invalid_api_key"}


@pytest.fixture
def no_auth_headers() -> dict:
    """Get headers without authentication."""
    return {}
