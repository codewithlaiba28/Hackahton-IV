# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.quiz import QuizQuestion, QuizResult, QuizAttemptSummary
from app.services.quiz_service import get_quiz_service

router = APIRouter()


@router.get("/{chapter_id}", response_model=APIResponse[List[QuizQuestion]])
async def get_quiz_questions(
    chapter_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get quiz questions for a chapter (WITHOUT answers)."""
    quiz_service = get_quiz_service()
    questions = await quiz_service.get_quiz_questions(chapter_id, db)
    
    # Convert to schema (excluding correct_answer)
    question_schemas = []
    for q in questions:
        question_schemas.append(QuizQuestion(
            id=str(q.id),
            question_text=q.question_text,
            question_type=q.question_type,
            options=q.options,
            sequence_order=q.sequence_order
        ))
    
    return APIResponse(data=question_schemas)


@router.post("/{chapter_id}/submit", response_model=APIResponse[QuizResult])
async def submit_quiz(
    chapter_id: str,
    submission: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit quiz answers and get graded results."""
    quiz_service = get_quiz_service()
    result = await quiz_service.grade_quiz(chapter_id, submission, current_user, db)
    
    return APIResponse(data=QuizResult(**result))


@router.get("/{chapter_id}/best-score", response_model=APIResponse[QuizAttemptSummary | None])
async def get_best_score(
    chapter_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's best score for a chapter."""
    quiz_service = get_quiz_service()
    result = await quiz_service.get_best_score(chapter_id, current_user.id, db)
    
    return APIResponse(data=result)
