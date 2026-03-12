"""
Phase 2 Hybrid Features Tests

Tests for Adaptive Learning Path and LLM-Graded Assessments.

Constitutional Compliance Testing:
- Principle VIII: Premium-gating
- Principle IX: Architectural separation
- Principle X: Cost tracking
- Principle XII: Tier enforcement

Test Scenarios:
1. Free user cannot access Phase 2 features (403)
2. Premium user can access Phase 2 features (200)
3. Cost tracking works correctly
4. model_answer_criteria never exposed
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from app.models.user import User, UserTier
from app.models.chapter import Chapter
from app.models.assessment import AssessmentQuestion


# ===========================================
# TEST FIXTURES
# ===========================================

@pytest.fixture
async def free_user(db: AsyncSession) -> User:
    """Create a free tier user."""
    user = User(
        email=f"free_test_{uuid4()}@example.com",
        tier=UserTier.FREE,
        api_key=f"free_test_key_{uuid4()}"
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.fixture
async def premium_user(db: AsyncSession) -> User:
    """Create a premium tier user."""
    user = User(
        email=f"premium_test_{uuid4()}@example.com",
        tier=UserTier.PREMIUM,
        api_key=f"premium_test_key_{uuid4()}"
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.fixture
async def pro_user(db: AsyncSession) -> User:
    """Create a pro tier user."""
    user = User(
        email=f"pro_test_{uuid4()}@example.com",
        tier=UserTier.PRO,
        api_key=f"pro_test_key_{uuid4()}"
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.fixture
async def chapter_with_assessments(db: AsyncSession) -> Chapter:
    """Create a chapter with assessment questions."""
    chapter = Chapter(
        id="ch-001",
        title="Test Chapter",
        sequence_order=1,
        is_free=True,
        content="# Test Content"
    )
    db.add(chapter)
    
    # Add assessment questions
    question = AssessmentQuestion(
        chapter_id=chapter.id,
        question_text="Explain AI Agents",
        model_answer_criteria="Must include autonomy, perception, action",
        difficulty="conceptual",
        sequence_order=1
    )
    db.add(question)
    
    await db.commit()
    await db.refresh(chapter)
    return chapter


# ===========================================
# TEST 1: ADAPTIVE LEARNING PATH - FREE USER
# ===========================================

@pytest.mark.asyncio
async def test_free_user_cannot_access_adaptive_path(
    client: AsyncClient,
    free_user: User
):
    """
    FREE USER TEST:
    Free users should get 403 when trying to access adaptive learning path.
    
    Constitutional Compliance:
    - Principle VIII: Premium-gated
    - Principle XII: Tier enforcement
    """
    headers = {"X-API-Key": free_user.api_key}
    
    response = await client.post(
        "/api/v2/adaptive/learning-path",
        headers=headers,
        json={"include_review": True}
    )
    
    # MUST return 403 Forbidden
    assert response.status_code == 403
    data = response.json()
    assert "PREMIUM_REQUIRED" in data["detail"]["error"]
    assert "upgrade" in data["detail"]["message"].lower()


# ===========================================
# TEST 2: ADAPTIVE LEARNING PATH - PREMIUM USER
# ===========================================

@pytest.mark.asyncio
async def test_premium_user_can_access_adaptive_path(
    client: AsyncClient,
    premium_user: User,
    chapter_with_assessments: Chapter
):
    """
    PREMIUM USER TEST:
    Premium users should get 200 with personalized recommendations.
    
    Constitutional Compliance:
    - Principle VIII: User-initiated
    - Principle X: Cost-tracked
    - Principle XI: Structured output
    """
    headers = {"X-API-Key": premium_user.api_key}
    
    response = await client.post(
        "/api/v2/adaptive/learning-path",
        headers=headers,
        json={"include_review": True}
    )
    
    # MUST return 200 with structured recommendation
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "recommended_chapters" in data["data"]
    assert "meta" in data
    assert data["meta"]["llm_call"] is True
    assert data["meta"]["cached"] is False


# ===========================================
# TEST 3: ADAPTIVE LEARNING PATH - PRO USER
# ===========================================

@pytest.mark.asyncio
async def test_pro_user_can_access_adaptive_path(
    client: AsyncClient,
    pro_user: User
):
    """
    PRO USER TEST:
    Pro users should get 200 with personalized recommendations.
    """
    headers = {"X-API-Key": pro_user.api_key}
    
    response = await client.post(
        "/api/v2/adaptive/learning-path",
        headers=headers,
        json={"include_review": True}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "recommended_chapters" in data["data"]


# ===========================================
# TEST 4: ASSESSMENT QUESTIONS - FREE USER
# ===========================================

@pytest.mark.asyncio
async def test_free_user_cannot_access_assessments(
    client: AsyncClient,
    free_user: User,
    chapter_with_assessments: Chapter
):
    """
    FREE USER TEST:
    Free users should get 403 when trying to access assessment questions.
    
    Constitutional Compliance:
    - Principle VIII: Premium-gated
    - Guard: model_answer_criteria never exposed
    """
    headers = {"X-API-Key": free_user.api_key}
    chapter_id = chapter_with_assessments.id
    
    response = await client.get(
        f"/api/v2/assessments/{chapter_id}/questions",
        headers=headers
    )
    
    # MUST return 403 Forbidden
    assert response.status_code == 403
    data = response.json()
    assert "PREMIUM_REQUIRED" in data["detail"]["error"]


# ===========================================
# TEST 5: ASSESSMENT QUESTIONS - PREMIUM USER
# ===========================================

@pytest.mark.asyncio
async def test_premium_user_can_access_assessments(
    client: AsyncClient,
    premium_user: User,
    chapter_with_assessments: Chapter
):
    """
    PREMIUM USER TEST:
    Premium users should get questions WITHOUT model_answer_criteria.
    
    Constitutional Compliance:
    - Principle VIII: Premium-gated
    - Guard: model_answer_criteria NEVER exposed
    """
    headers = {"X-API-Key": premium_user.api_key}
    chapter_id = chapter_with_assessments.id
    
    response = await client.get(
        f"/api/v2/assessments/{chapter_id}/questions",
        headers=headers
    )
    
    # MUST return 200 with questions
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0
    
    # CRITICAL: model_answer_criteria MUST NOT be in response
    for question in data["data"]:
        assert "model_answer_criteria" not in question
        assert "question_text" in question
        assert "difficulty" in question
    
    # Security confirmation in meta
    assert data["meta"]["criteria_exposed"] is False


# ===========================================
# TEST 6: ASSESSMENT SUBMISSION - FREE USER
# ===========================================

@pytest.mark.asyncio
async def test_free_user_cannot_submit_assessment(
    client: AsyncClient,
    free_user: User,
    chapter_with_assessments: Chapter
):
    """
    FREE USER TEST:
    Free users should get 403 when trying to submit answers for grading.
    """
    headers = {"X-API-Key": free_user.api_key}
    chapter_id = chapter_with_assessments.id
    
    # Get question first (should fail, but let's try anyway)
    response = await client.post(
        f"/api/v2/assessments/{chapter_id}/submit",
        headers=headers,
        json={
            "question_id": str(chapter_with_assessments.assessment_questions[0].id),
            "answer_text": "AI agents are autonomous systems..."
        }
    )
    
    # MUST return 403 Forbidden
    assert response.status_code == 403


# ===========================================
# TEST 7: ASSESSMENT SUBMISSION - PREMIUM USER
# ===========================================

@pytest.mark.asyncio
async def test_premium_user_can_submit_assessment(
    client: AsyncClient,
    premium_user: User,
    chapter_with_assessments: Chapter
):
    """
    PREMIUM USER TEST:
    Premium users can submit answers and get graded feedback.
    
    Constitutional Compliance:
    - Principle X: Cost-tracked
    - Principle XI: Structured output, grounding
    """
    headers = {"X-API-Key": premium_user.api_key}
    chapter_id = chapter_with_assessments.id
    question_id = str(chapter_with_assessments.assessment_questions[0].id)
    
    response = await client.post(
        f"/api/v2/assessments/{chapter_id}/submit",
        headers=headers,
        json={
            "question_id": question_id,
            "answer_text": "AI agents are autonomous systems that perceive their environment and take actions to achieve goals. They differ from traditional programs by learning and adapting. For example, a self-driving car is an AI agent that uses sensors to perceive the road and actuators to control the vehicle."
        }
    )
    
    # MUST return 200 with graded result
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "score" in data["data"]
    assert "grade" in data["data"]
    assert "feedback" in data["data"]
    assert "meta" in data
    assert data["meta"]["llm_call"] is True
    assert data["meta"]["word_count"] > 0


# ===========================================
# TEST 8: ASSESSMENT - WORD COUNT VALIDATION
# ===========================================

@pytest.mark.asyncio
async def test_assessment_rejects_too_short_answer(
    client: AsyncClient,
    premium_user: User,
    chapter_with_assessments: Chapter
):
    """
    VALIDATION TEST:
    Answers under 20 words should be rejected (no wasted LLM tokens).
    """
    headers = {"X-API-Key": premium_user.api_key}
    chapter_id = chapter_with_assessments.id
    question_id = str(chapter_with_assessments.assessment_questions[0].id)
    
    response = await client.post(
        f"/api/v2/assessments/{chapter_id}/submit",
        headers=headers,
        json={
            "question_id": question_id,
            "answer_text": "AI agents are cool."  # Too short (< 20 words)
        }
    )
    
    # MUST return 422 Unprocessable Entity
    assert response.status_code == 422
    data = response.json()
    assert "WORD_COUNT" in data["detail"]["error"]


@pytest.mark.asyncio
async def test_assessment_rejects_too_long_answer(
    client: AsyncClient,
    premium_user: User,
    chapter_with_assessments: Chapter
):
    """
    VALIDATION TEST:
    Answers over 500 words should be rejected.
    """
    headers = {"X-API-Key": premium_user.api_key}
    chapter_id = chapter_with_assessments.id
    question_id = str(chapter_with_assessments.assessment_questions[0].id)
    
    # Generate 501 words
    long_answer = " ".join(["word"] * 501)
    
    response = await client.post(
        f"/api/v2/assessments/{chapter_id}/submit",
        headers=headers,
        json={
            "question_id": question_id,
            "answer_text": long_answer
        }
    )
    
    # MUST return 422 Unprocessable Entity
    assert response.status_code == 422
    data = response.json()
    assert "WORD_COUNT" in data["detail"]["error"]


# ===========================================
# TEST 9: COST TRACKING - FREE USER
# ===========================================

@pytest.mark.asyncio
async def test_free_user_cost_summary_is_zero(
    client: AsyncClient,
    free_user: User
):
    """
    COST TRANSPARENCY TEST:
    Free users should see $0.00 cost (they can't access hybrid features).
    """
    headers = {"X-API-Key": free_user.api_key}
    
    response = await client.get(
        "/api/v2/users/me/cost-summary",
        headers=headers
    )
    
    # MUST return 200 with $0 cost
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"]["total_cost_usd"] == 0.0
    assert data["data"]["remaining_budget"] == 0.0


# ===========================================
# TEST 10: COST TRACKING - PREMIUM USER
# ===========================================

@pytest.mark.asyncio
async def test_premium_user_cost_summary(
    client: AsyncClient,
    premium_user: User
):
    """
    COST TRANSPARENCY TEST:
    Premium users should see accurate cost breakdown.
    
    Constitutional Compliance:
    - Principle X: Cost tracking, transparency
    """
    headers = {"X-API-Key": premium_user.api_key}
    
    response = await client.get(
        "/api/v2/users/me/cost-summary",
        headers=headers
    )
    
    # MUST return 200 with cost breakdown
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total_cost_usd" in data["data"]
    assert "breakdown" in data["data"]
    assert "monthly_cap" in data["data"]
    assert "remaining_budget" in data["data"]
    
    # Premium cap should be $2.00
    assert data["data"]["monthly_cap"] == 2.00


# ===========================================
# TEST 11: COST TRACKING - PRO USER
# ===========================================

@pytest.mark.asyncio
async def test_pro_user_cost_summary(
    client: AsyncClient,
    pro_user: User
):
    """
    COST TRANSPARENCY TEST:
    Pro users should see $5.00 monthly cap.
    """
    headers = {"X-API-Key": pro_user.api_key}
    
    response = await client.get(
        "/api/v2/users/me/cost-summary",
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Pro cap should be $5.00
    assert data["data"]["monthly_cap"] == 5.00


# ===========================================
# TEST 12: CACHED RECOMMENDATION - NO LLM CALL
# ===========================================

@pytest.mark.asyncio
async def test_cached_recommendation_no_llm_call(
    client: AsyncClient,
    premium_user: User
):
    """
    CACHING TEST:
    GET /learning-path/latest should return cached result (no LLM call).
    
    Constitutional Compliance:
    - Principle X: Cost optimization
    """
    headers = {"X-API-Key": premium_user.api_key}
    
    # First, generate a recommendation
    await client.post(
        "/api/v2/adaptive/learning-path",
        headers=headers,
        json={"include_review": True}
    )
    
    # Then, get cached version
    response = await client.get(
        "/api/v2/adaptive/learning-path/latest",
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    
    # If data exists, it should be from cache
    if data["data"] is not None:
        assert "meta" in data
        assert data["meta"]["cached"] is True
        assert data["meta"]["llm_call"] is False


# ===========================================
# TEST 13: ASSESSMENT RESULTS - CACHED
# ===========================================

@pytest.mark.asyncio
async def test_assessment_results_cached(
    client: AsyncClient,
    premium_user: User,
    chapter_with_assessments: Chapter
):
    """
    CACHING TEST:
    GET /assessments/{id}/results returns cached results (no LLM call).
    """
    headers = {"X-API-Key": premium_user.api_key}
    chapter_id = chapter_with_assessments.id
    question_id = str(chapter_with_assessments.assessment_questions[0].id)
    
    # First, submit an answer
    await client.post(
        f"/api/v2/assessments/{chapter_id}/submit",
        headers=headers,
        json={
            "question_id": question_id,
            "answer_text": "AI agents are autonomous systems that perceive their environment and take actions to achieve goals. They differ from traditional programs by learning and adapting."
        }
    )
    
    # Then, get results (should be cached)
    response = await client.get(
        f"/api/v2/assessments/{chapter_id}/results",
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0


# ===========================================
# TEST 14: ARCHITECTURAL SEPARATION
# ===========================================

@pytest.mark.asyncio
async def test_phase_1_endpoints_still_work(
    client: AsyncClient,
    free_user: User,
    chapter_with_assessments: Chapter
):
    """
    ARCHITECTURE TEST:
    Phase 1 endpoints must work unchanged for all users.
    
    Constitutional Compliance:
    - Principle IX: Architectural separation
    """
    headers = {"X-API-Key": free_user.api_key}
    
    # Test Phase 1: Get chapters
    response = await client.get("/chapters", headers=headers)
    assert response.status_code == 200
    
    # Test Phase 1: Get chapter content (free chapter)
    response = await client.get(f"/chapters/{chapter_with_assessments.id}", headers=headers)
    assert response.status_code == 200
    
    # Test Phase 1: Search
    response = await client.get("/search?q=AI", headers=headers)
    assert response.status_code == 200
    
    # Test Phase 1: Get progress
    response = await client.get(f"/progress/{free_user.id}", headers=headers)
    assert response.status_code == 200


# ===========================================
# TEST 15: PREMIUM GATE - DETAILED MESSAGE
# ===========================================

@pytest.mark.asyncio
async def test_premium_gate_error_message_quality(
    client: AsyncClient,
    free_user: User
):
    """
    UX TEST:
    Premium gate error messages should be clear and helpful.
    
    Constitutional Compliance:
    - Principle XII: Clear upgrade message
    """
    headers = {"X-API-Key": free_user.api_key}
    
    response = await client.post(
        "/api/v2/adaptive/learning-path",
        headers=headers,
        json={}
    )
    
    assert response.status_code == 403
    data = response.json()
    detail = data["detail"]
    
    # Must have structured error
    assert "error" in detail
    assert "message" in detail
    assert detail["error"] == "PREMIUM_REQUIRED"
    
    # Message should mention upgrade
    assert "upgrade" in detail["message"].lower() or "premium" in detail["message"].lower()
