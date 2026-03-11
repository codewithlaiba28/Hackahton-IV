"""
Tests for progress endpoints.
Tests progress tracking and streak calculation.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from datetime import date, timedelta
from sqlalchemy import select

from app.main import app
from app.models.progress import ChapterProgress, DailyActivity


@pytest.fixture
def client():
    """Create test client."""
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_get_progress_empty(
    client: AsyncClient,
    free_user: User,
    headers_free_user: dict
):
    """Test getting progress for user with no activity."""
    response = await client.get(f"/progress/{free_user.id}", headers=headers_free_user)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"]["chapters_completed"] == []
    assert data["data"]["chapters_in_progress"] == []
    assert data["data"]["overall_percentage"] == 0
    assert data["data"]["current_streak_days"] == 0


@pytest.mark.asyncio
async def test_update_chapter_progress(
    client: AsyncClient,
    free_user: User,
    sample_chapters: list,
    headers_free_user: dict,
    db_session
):
    """Test updating chapter progress."""
    update_data = {"status": "in_progress"}
    
    response = await client.put(
        f"/progress/{free_user.id}/chapter/ch-001",
        json=update_data,
        headers=headers_free_user
    )
    
    assert response.status_code == status.HTTP_200_OK
    
    # Verify in database
    result = await db_session.execute(
        select(ChapterProgress).where(
            ChapterProgress.user_id == free_user.id,
            ChapterProgress.chapter_id == "ch-001"
        )
    )
    progress = result.scalar_one_or_none()
    
    assert progress is not None
    assert progress.status == "in_progress"
    assert progress.started_at is not None


@pytest.mark.asyncio
async def test_complete_chapter(
    client: AsyncClient,
    free_user: User,
    sample_chapters: list,
    headers_free_user: dict,
    db_session
):
    """Test completing a chapter."""
    # First start the chapter
    await client.put(
        f"/progress/{free_user.id}/chapter/ch-001",
        json={"status": "in_progress"},
        headers=headers_free_user
    )
    
    # Then complete it
    response = await client.put(
        f"/progress/{free_user.id}/chapter/ch-001",
        json={"status": "completed"},
        headers=headers_free_user
    )
    
    assert response.status_code == status.HTTP_200_OK
    
    # Verify in database
    result = await db_session.execute(
        select(ChapterProgress).where(
            ChapterProgress.user_id == free_user.id,
            ChapterProgress.chapter_id == "ch-001"
        )
    )
    progress = result.scalar_one_or_none()
    
    assert progress.status == "completed"
    assert progress.completed_at is not None


@pytest.mark.asyncio
async def test_progress_summary_after_completion(
    client: AsyncClient,
    free_user: User,
    sample_chapters: list,
    headers_free_user: dict
):
    """Test progress summary reflects completed chapters."""
    # Complete one chapter
    await client.put(
        f"/progress/{free_user.id}/chapter/ch-001",
        json={"status": "completed"},
        headers=headers_free_user
    )
    
    # Get progress summary
    response = await client.get(f"/progress/{free_user.id}", headers=headers_free_user)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert "ch-001" in data["data"]["chapters_completed"]
    assert data["data"]["overall_percentage"] > 0


@pytest.mark.asyncio
async def test_cannot_access_another_user_progress(
    client: AsyncClient,
    free_user: User,
    premium_user: User,
    headers_free_user: dict
):
    """Test users cannot access another user's progress."""
    other_user_id = str(premium_user.id)
    
    response = await client.get(f"/progress/{other_user_id}", headers=headers_free_user)
    
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_cannot_update_another_user_progress(
    client: AsyncClient,
    free_user: User,
    premium_user: User,
    headers_free_user: dict
):
    """Test users cannot update another user's progress."""
    other_user_id = str(premium_user.id)
    
    response = await client.put(
        f"/progress/{other_user_id}/chapter/ch-001",
        json={"status": "completed"},
        headers=headers_free_user
    )
    
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_get_quiz_scores_empty(
    client: AsyncClient,
    free_user: User,
    headers_free_user: dict
):
    """Test getting quiz scores with no attempts."""
    response = await client.get(f"/progress/{free_user.id}/quiz-scores", headers=headers_free_user)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"]["quiz_scores"] == []


@pytest.mark.asyncio
async def test_streak_tracking(
    client: AsyncClient,
    free_user: User,
    sample_chapters: list,
    headers_free_user: dict,
    db_session
):
    """Test streak is tracked in daily_activity."""
    # Complete a chapter
    await client.put(
        f"/progress/{free_user.id}/chapter/ch-001",
        json={"status": "completed"},
        headers=headers_free_user
    )
    
    # Check daily activity was recorded
    result = await db_session.execute(
        select(DailyActivity).where(DailyActivity.user_id == free_user.id)
    )
    activities = result.scalars().all()
    
    assert len(activities) == 1
    assert activities[0].activity_date == date.today()


@pytest.mark.asyncio
async def test_unauthenticated_progress_access(
    client: AsyncClient,
    free_user: User
):
    """Test unauthenticated user gets 401."""
    response = await client.get(f"/progress/{free_user.id}")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
