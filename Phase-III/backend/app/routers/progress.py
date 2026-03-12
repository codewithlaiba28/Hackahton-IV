# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.progress import ProgressSummary, UpdateProgressRequest
from app.services.progress_service import get_progress_service

router = APIRouter()


@router.get("/{user_id}", response_model=APIResponse[ProgressSummary])
async def get_progress(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's complete progress summary."""
    # Security: Users can only access their own progress
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access another user's progress"
        )
    
    progress_service = get_progress_service()
    summary = await progress_service.get_progress_summary(current_user.id, db)
    
    return APIResponse(data=ProgressSummary(**summary))


@router.put("/{user_id}/chapter/{chapter_id}", response_model=APIResponse)
async def update_chapter_progress(
    user_id: str,
    chapter_id: str,
    request: UpdateProgressRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update chapter progress status."""
    # Security: Users can only update their own progress
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update another user's progress"
        )
    
    progress_service = get_progress_service()
    await progress_service.update_chapter_progress(
        current_user.id, chapter_id, request.status, db
    )
    
    return APIResponse(data={"message": "Progress updated"})


@router.get("/{user_id}/quiz-scores", response_model=APIResponse)
async def get_quiz_scores(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all quiz scores for a user."""
    # Security check
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access another user's quiz scores"
        )

    progress_service = get_progress_service()
    quiz_scores = await progress_service.get_all_quiz_scores(current_user.id, db)

    return APIResponse(data={"quiz_scores": quiz_scores})
