"""
Adaptive Learning Path Router

Feature A: Personalized learning path recommendations using LLM analysis.

Constitutional Compliance:
- Principle VIII: Premium-gated, user-initiated
- Principle IX: Isolated in /api/v2/ (separate from Phase 1)
- Principle X: Cost-tracked via llm_service
- Principle XI: Structured JSON output, fallback on LLM failure
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.schemas.adaptive import (
    AdaptiveRecommendationResponse,
    AdaptivePathRequest,
    CachedRecommendation
)
from app.schemas.common import APIResponse
from app.services.adaptive_service import adaptive_service

router = APIRouter(prefix="/api/v2/adaptive", tags=["adaptive-learning"])


@router.post(
    "/learning-path",
    response_model=APIResponse[AdaptiveRecommendationResponse],
    summary="Generate Personalized Learning Path (Premium Only)",
    response_description="Personalized learning recommendation"
)
async def generate_learning_path(
    request: AdaptivePathRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    **Pro Tier Feature**
    
    Generate a personalized learning path using AI analysis of:
    - Quiz performance
    - Learning patterns
    - Knowledge gaps
    - Optimal review timing
    
    **Cost:** Included in Premium/Pro tier ($2-$5 monthly LLM budget)
    
    **Triggers:**
    - Student asks "What should I study next?"
    - Student requests "Give me a study plan"
    - Student asks "What's next for me?"
    
    **Constitutional Compliance:**
    - Premium-gated (Principle VIII)
    - User-initiated (Principle VIII)
    - Cost-tracked (Principle X)
    """
    try:
        recommendation = await adaptive_service.generate_learning_path(
            user=current_user,
            db=db
        )
        
        return APIResponse(
            data=recommendation,
            error=None,
            meta={
                "message": "Learning path generated successfully",
                "llm_call": True,
                "cached": False
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions (e.g., 403 for non-premium)
        raise
        
    except Exception as e:
        # Unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "INTERNAL_ERROR",
                "message": f"Failed to generate learning path: {str(e)}"
            }
        )


@router.get(
    "/learning-path/latest",
    response_model=APIResponse[Optional[CachedRecommendation]],
    summary="Get Latest Cached Recommendation (Premium Only)",
    response_description="Last generated recommendation or null"
)
async def get_latest_recommendation(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    **Pro Tier Feature**
    
    Get the most recently generated learning path recommendation.
    
    **NO LLM CALL** - Returns cached recommendation from database.
    
    **Use Cases:**
    - Student wants to review their plan
    - Student asks "What was my study plan again?"
    - Fallback when LLM is unavailable
    
    **Constitutional Compliance:**
    - Premium-gated (Principle VIII)
    - Zero LLM cost (cached data)
    """
    try:
        recommendation = await adaptive_service.get_latest_recommendation(
            user=current_user,
            db=db
        )
        
        return APIResponse(
            data=recommendation,
            error=None,
            meta={
                "message": "Cached recommendation retrieved",
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
                "message": f"Failed to retrieve cached recommendation: {str(e)}"
            }
        )
