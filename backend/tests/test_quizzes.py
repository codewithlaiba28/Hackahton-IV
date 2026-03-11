"""
Tests for quiz endpoints.
Tests quiz retrieval and rule-based grading.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
import uuid

from app.main import app
from app.models.quiz import QuizAttempt


@pytest.fixture
def client():
    """Create test client."""
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_get_quiz_questions(
    client: AsyncClient,
    free_user: User,
    sample_quiz_questions: list,
    headers_free_user: dict
):
    """Test getting quiz questions does NOT return correct answers."""
    response = await client.get("/quizzes/ch-001", headers=headers_free_user)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert len(data["data"]) == 2
    
    # Verify correct_answer is NOT in response
    for question in data["data"]:
        assert "correct_answer" not in question
        assert "question_text" in question
        assert "options" in question
        assert "question_type" in question


@pytest.mark.asyncio
async def test_submit_quiz_all_correct(
    client: AsyncClient,
    free_user: User,
    sample_quiz_questions: list,
    headers_free_user: dict
):
    """Test submitting all correct answers returns 100%."""
    submission = {
        "answers": [
            {"question_id": str(sample_quiz_questions[0].id), "answer": "Perception, Decision Making, Action"},
            {"question_id": str(sample_quiz_questions[1].id), "answer": "True"}
        ]
    }
    
    response = await client.post("/quizzes/ch-001/submit", json=submission, headers=headers_free_user)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"]["score"] == 2
    assert data["data"]["total"] == 2
    assert data["data"]["percentage"] == 100.0
    
    # Verify all questions marked correct
    for result in data["data"]["results"]:
        assert result["correct"] == True


@pytest.mark.asyncio
async def test_submit_quiz_all_wrong(
    client: AsyncClient,
    free_user: User,
    sample_quiz_questions: list,
    headers_free_user: dict
):
    """Test submitting all wrong answers returns 0%."""
    submission = {
        "answers": [
            {"question_id": str(sample_quiz_questions[0].id), "answer": "Wrong Answer 1"},
            {"question_id": str(sample_quiz_questions[1].id), "answer": "False"}
        ]
    }
    
    response = await client.post("/quizzes/ch-001/submit", json=submission, headers=headers_free_user)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"]["score"] == 0
    assert data["data"]["total"] == 2
    assert data["data"]["percentage"] == 0.0
    
    # Verify all questions marked wrong
    for result in data["data"]["results"]:
        assert result["correct"] == False


@pytest.mark.asyncio
async def test_submit_quiz_mixed(
    client: AsyncClient,
    free_user: User,
    sample_quiz_questions: list,
    headers_free_user: dict
):
    """Test submitting mixed answers returns correct percentage."""
    submission = {
        "answers": [
            {"question_id": str(sample_quiz_questions[0].id), "answer": "Perception, Decision Making, Action"},
            {"question_id": str(sample_quiz_questions[1].id), "answer": "False"}
        ]
    }
    
    response = await client.post("/quizzes/ch-001/submit", json=submission, headers=headers_free_user)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"]["score"] == 1
    assert data["data"]["total"] == 2
    assert data["data"]["percentage"] == 50.0


@pytest.mark.asyncio
async def test_quiz_attempt_recorded(
    client: AsyncClient,
    free_user: User,
    sample_quiz_questions: list,
    headers_free_user: dict,
    db_session
):
    """Test quiz attempts are recorded in database."""
    submission = {
        "answers": [
            {"question_id": str(sample_quiz_questions[0].id), "answer": "Perception, Decision Making, Action"}
        ]
    }
    
    await client.post("/quizzes/ch-001/submit", json=submission, headers=headers_free_user)
    
    # Check database for recorded attempt
    result = await db_session.execute(
        select(QuizAttempt).where(QuizAttempt.user_id == free_user.id)
    )
    attempts = result.scalars().all()
    
    assert len(attempts) == 1
    assert attempts[0].chapter_id == "ch-001"
    assert attempts[0].score >= 0


@pytest.mark.asyncio
async def test_get_best_score(
    client: AsyncClient,
    free_user: User,
    sample_quiz_questions: list,
    headers_free_user: dict
):
    """Test getting best score for chapter."""
    # First submission - 50%
    submission1 = {
        "answers": [
            {"question_id": str(sample_quiz_questions[0].id), "answer": "Perception, Decision Making, Action"},
            {"question_id": str(sample_quiz_questions[1].id), "answer": "False"}
        ]
    }
    await client.post("/quizzes/ch-001/submit", json=submission1, headers=headers_free_user)
    
    # Second submission - 100%
    submission2 = {
        "answers": [
            {"question_id": str(sample_quiz_questions[0].id), "answer": "Perception, Decision Making, Action"},
            {"question_id": str(sample_quiz_questions[1].id), "answer": "True"}
        ]
    }
    await client.post("/quizzes/ch-001/submit", json=submission2, headers=headers_free_user)
    
    # Get best score
    response = await client.get("/quizzes/ch-001/best-score", headers=headers_free_user)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"]["best_score"] == 2
    assert data["data"]["percentage"] == 100.0


@pytest.mark.asyncio
async def test_quiz_premium_chapter_free_user(
    client: AsyncClient,
    free_user: User,
    headers_free_user: dict
):
    """Test free user gets 403 for premium chapter quiz."""
    response = await client.get("/quizzes/ch-004", headers=headers_free_user)
    
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_quiz_premium_chapter_premium_user(
    client: AsyncClient,
    premium_user: User,
    sample_quiz_questions: list,
    headers_premium_user: dict
):
    """Test premium user can access premium chapter quiz."""
    response = await client.get("/quizzes/ch-004", headers=headers_premium_user)
    
    # Should return 200 with empty list (no questions for ch-004 in test data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_unauthenticated_quiz_access(
    client: AsyncClient,
    sample_quiz_questions: list
):
    """Test unauthenticated user gets 401."""
    response = await client.get("/quizzes/ch-001")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
