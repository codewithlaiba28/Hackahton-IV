"""
LLM-Graded Assessments Router

Feature B: Open-ended written assessments with detailed educational feedback.

Constitutional Compliance:
- Principle VIII: Premium-gated, user-initiated
- Principle IX: Isolated in /api/v2/ (separate from Phase 1)
- Principle X: Cost-tracked via llm_service
- Principle XI: Structured JSON output, grounded in content
- Guard: model_answer_criteria NEVER exposed
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.schemas.assessment import (
    AssessmentQuestionResponse,
    SubmitAnswerRequest,
    AssessmentGradeResponse,
    AssessmentResultSummary
)
from app.schemas.common import APIResponse
from app.services.assessment_service import assessment_service

router = APIRouter(prefix="/api/v2/assessments", tags=["assessments"])


@router.get(
    "/{chapter_id}/questions",
    response_model=APIResponse[List[AssessmentQuestionResponse]],
    summary="Get Assessment Questions (Premium Only)",
    response_description="List of open-ended questions"
)
async def get_assessment_questions(
    chapter_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    **Pro Tier Feature**
    
    Get open-ended assessment questions for a chapter.
    
    **CRITICAL:** Does NOT include model_answer_criteria
    
    **Triggers:**
    - Student asks "Test my understanding"
    - Student requests "I want a written test"
    - Student asks "Give me assessment questions"
    
    **Constitutional Compliance:**
    - Premium-gated (Principle VIII)
    - No criteria leak (security guard)
    """
    try:
        questions = await assessment_service.get_questions(
            chapter_id=chapter_id,
            user=current_user,
            db=db
        )
        
        return APIResponse(
            data=questions,
            error=None,
            meta={
                "message": f"Retrieved {len(questions)} assessment questions",
                "chapter_id": chapter_id,
                "criteria_exposed": False  # Security confirmation
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        # Unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "INTERNAL_ERROR",
                "message": f"Failed to retrieve questions: {str(e)}"
            }
        )


@router.post(
    "/{chapter_id}/submit",
    response_model=APIResponse[AssessmentGradeResponse],
    summary="Submit Answer for LLM Grading (Premium Only)",
    response_description="Graded assessment with feedback"
)
async def submit_assessment(
    chapter_id: str,
    request: SubmitAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    **Pro Tier Feature**
    
    Submit a written answer for LLM grading.
    
    **Requirements:**
    - Answer must be 20-500 words
    - Premium/Pro tier only
    
    **Returns:**
    - Score (0-100)
    - Grade (A/B/C/D/F)
    - Detailed feedback
    - Improvement suggestions
    
    **Cost:** Included in Premium/Pro tier ($2-$5 monthly LLM budget)
    
    **Constitutional Compliance:**
    - Premium-gated (Principle VIII)
    - User-initiated (explicit submission)
    - Cost-tracked (Principle X)
    - Word count validated (no wasted tokens)
    """
    try:
        result = await assessment_service.grade_answer(
            chapter_id=chapter_id,
            question_id=UUID(request.question_id),
            answer_text=request.answer_text,
            user=current_user,
            db=db
        )
        
        return APIResponse(
            data=result,
            error=None,
            meta={
                "message": "Assessment graded successfully",
                "llm_call": True,
                "word_count": result.word_count
            }
        )
        
    except HTTPException as e:
        # Re-raise HTTP exceptions (403, 422)
        raise
        
    except Exception as e:
        # Unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "INTERNAL_ERROR",
                "message": f"Failed to grade assessment: {str(e)}"
            }
        )


@router.get(
    "/{chapter_id}/results",
    response_model=APIResponse[List[AssessmentResultSummary]],
    summary="Get Past Assessment Results (Premium Only)",
    response_description="List of past assessment summaries"
)
async def get_assessment_results(
    chapter_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    **Pro Tier Feature**
    
    Get all past assessment results for a chapter.
    
    **NO LLM CALL** - Returns cached results from database.
    
    **Use Cases:**
    - Student wants to review past performance
    - Student asks "How did I do on assessments?"
    
    **Constitutional Compliance:**
    - Premium-gated (Principle VIII)
    - Zero LLM cost (cached data)
    """
    try:
        results = await assessment_service.get_results(
            chapter_id=chapter_id,
            user=current_user,
            db=db
        )
        
        return APIResponse(
            data=results,
            error=None,
            meta={
                "message": f"Retrieved {len(results)} assessment results",
                "chapter_id": chapter_id,
                "llm_call": False,
                "cached": True
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        # Unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "INTERNAL_ERROR",
                "message": f"Failed to retrieve results: {str(e)}"
            }
        )
