"""
Adaptive Learning Path Service

Generates personalized learning recommendations using LLM analysis.

Constitutional Compliance:
- Principle VIII: Premium-gated only, user-initiated
- Principle X: Cost-tracked via llm_service
- Principle XI: Grounded in student data, structured output
"""

import json
from typing import Optional, List, Dict, Any
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User, UserTier
from app.models.adaptive import AdaptiveRecommendation
from app.models.llm_usage import LLMUsage
from app.schemas.adaptive import AdaptiveRecommendationResponse, RecommendedChapter
from app.services.llm_service import llm_service
from app.services.exceptions import LLMUnavailableError, LLMParseError
from app.config import settings


class AdaptiveService:
    """
    Service for generating personalized learning paths.
    
    Uses LLM to analyze student's learning patterns and generate
    actionable recommendations.
    """
    
    # System prompt for educational analytics
    SYSTEM_PROMPT = """You are an educational analytics expert analyzing a student's learning data for an AI Agent Development course. Base ALL recommendations strictly on the provided student data and chapter information. Do not recommend chapters or topics not present in the provided chapter list. Return ONLY valid JSON matching the specified schema. No preamble, no explanation outside JSON."""
    
    async def generate_learning_path(
        self,
        user: User,
        db: AsyncSession
    ) -> AdaptiveRecommendationResponse:
        """
        Generate personalized learning path using LLM analysis.
        
        Args:
            user: Current user (must be premium/pro tier)
            db: Async database session
            
        Returns:
            Personalized learning path recommendation
            
        Raises:
            HTTPException: 403 if user is not premium/pro tier
            HTTPException: 503 if LLM is unavailable
        """
        # 1. Premium gate check (Constitutional Principle VIII)
        if user.tier not in [UserTier.PREMIUM, UserTier.PRO]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "PREMIUM_REQUIRED",
                    "message": "Adaptive learning paths are a premium feature. Upgrade to access.",
                    "upgrade_url": "/upgrade"
                }
            )
        
        # 2. Collect student data
        # Import here to avoid circular imports
        from app.models.chapter import Chapter
        from app.models.quiz import QuizAttempt
        
        # Get all chapters metadata
        chapters_stmt = select(Chapter).order_by(Chapter.sequence_order)
        chapters_result = await db.execute(chapters_stmt)
        chapters = chapters_result.scalars().all()
        
        # Get user's quiz attempts
        quiz_attempts_stmt = select(QuizAttempt).where(
            QuizAttempt.user_id == user.id
        )
        quiz_attempts_result = await db.execute(quiz_attempts_stmt)
        quiz_attempts = quiz_attempts_result.scalars().all()
        
        # Get user's chapter progress
        from app.models.chapter import ChapterProgress
        progress_stmt = select(ChapterProgress).where(
            ChapterProgress.user_id == user.id
        )
        progress_result = await db.execute(progress_stmt)
        chapter_progress = progress_result.scalars().all()
        
        # 3. Build student data JSON for LLM
        student_data = {
            "user_id": str(user.id),
            "tier": user.tier.value,
            "quiz_attempts": [
                {
                    "chapter_id": attempt.chapter_id,
                    "score": attempt.score,
                    "attempt_number": attempt.attempt_number,
                    "submitted_at": attempt.submitted_at.isoformat()
                }
                for attempt in quiz_attempts
            ],
            "chapter_progress": [
                {
                    "chapter_id": prog.chapter_id,
                    "completed": prog.completed,
                    "completed_at": prog.completed_at.isoformat() if prog.completed_at else None
                }
                for prog in chapter_progress
            ]
        }
        
        chapters_metadata = [
            {
                "chapter_id": ch.id,
                "title": ch.title,
                "difficulty": ch.difficulty,
                "sequence_order": ch.sequence_order,
                "is_free": ch.is_free
            }
            for ch in chapters
        ]
        
        # 4. Build LLM prompts
        user_prompt = f"""Student Learning Data: {json.dumps(student_data, indent=2)}
Available Chapters: {json.dumps(chapters_metadata, indent=2)}

Generate a personalized learning path recommendation. Return JSON with this exact schema:
{{
  "recommended_chapters": [
    {{
      "chapter_id": "ch-XXX",
      "title": "...",
      "priority": 1,
      "reason": "...",
      "estimated_time_minutes": 30
    }}
  ],
  "weak_areas": ["...", "..."],
  "strengths": ["...", "..."],
  "overall_assessment": "...",
  "suggested_daily_goal_minutes": 45
}}

Base ALL recommendations strictly on the provided student data. Do not invent chapters or topics not in the chapter list."""
        
        # 5. Call LLM service
        try:
            llm_response, llm_usage = await llm_service.call_claude(
                system_prompt=self.SYSTEM_PROMPT,
                user_prompt=user_prompt,
                max_tokens=settings.LLM_MAX_TOKENS,
                feature_name="adaptive_path",
                user_id=str(user.id),
                db=db
            )
            
            # 6. Parse LLM response into schema
            try:
                recommended_chapters = [
                    RecommendedChapter(**ch)
                    for ch in llm_response["recommended_chapters"]
                ]
                
                response = AdaptiveRecommendationResponse(
                    recommended_chapters=recommended_chapters,
                    weak_areas=llm_response["weak_areas"],
                    strengths=llm_response["strengths"],
                    overall_assessment=llm_response["overall_assessment"],
                    suggested_daily_goal_minutes=llm_response["suggested_daily_goal_minutes"]
                )
            except (KeyError, ValueError) as e:
                raise LLMParseError(
                    f"LLM response missing required fields: {str(e)}",
                    raw_response=str(llm_response)
                )
            
            # 7. Store recommendation in database
            recommendation = AdaptiveRecommendation(
                user_id=user.id,
                recommended_chapters=[ch.model_dump() for ch in recommended_chapters],
                weak_areas=response.weak_areas,
                strengths=response.strengths,
                overall_assessment=response.overall_assessment,
                suggested_daily_minutes=response.suggested_daily_goal_minutes,
                llm_usage_id=llm_usage.id
            )
            
            db.add(recommendation)
            await db.commit()
            await db.refresh(recommendation)
            
            return response
            
        except LLMUnavailableError as e:
            # Fallback: try to get last cached recommendation
            last_rec = await self.get_latest_recommendation(user, db)
            if last_rec:
                return last_rec
            else:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail={
                        "error": "LLM_UNAVAILABLE",
                        "message": "AI analysis temporarily unavailable. Please try again in a moment.",
                        "fallback": "No cached recommendations available."
                    }
                )
    
    async def get_latest_recommendation(
        self,
        user: User,
        db: AsyncSession
    ) -> Optional[AdaptiveRecommendationResponse]:
        """
        Get most recent cached recommendation (NO LLM call).
        
        Args:
            user: Current user
            db: Async database session
            
        Returns:
            Last cached recommendation or None if no history
        """
        # Premium gate check
        if user.tier not in [UserTier.PREMIUM, UserTier.PRO]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "PREMIUM_REQUIRED",
                    "message": "Adaptive learning paths are a premium feature. Upgrade to access.",
                    "upgrade_url": "/upgrade"
                }
            )
        
        # Query for latest recommendation
        stmt = (
            select(AdaptiveRecommendation)
            .where(AdaptiveRecommendation.user_id == user.id)
            .order_by(AdaptiveRecommendation.created_at.desc())
            .limit(1)
        )
        
        result = await db.execute(stmt)
        recommendation = result.scalar_one_or_none()
        
        if not recommendation:
            return None
        
        # Convert to response schema
        return AdaptiveRecommendationResponse(
            recommended_chapters=[
                RecommendedChapter(**ch)
                for ch in recommendation.recommended_chapters
            ],
            weak_areas=recommendation.weak_areas,
            strengths=recommendation.strengths,
            overall_assessment=recommendation.overall_assessment,
            suggested_daily_goal_minutes=recommendation.suggested_daily_minutes
        )


# Global instance for dependency injection
adaptive_service = AdaptiveService()
