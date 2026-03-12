"""
LLM-Graded Assessments Service

Evaluates free-form written answers using LLM analysis.

Constitutional Compliance:
- Principle VIII: Premium-gated only, user-initiated
- Principle X: Cost-tracked via llm_service
- Principle XI: Grounded in course content, structured output
- Guard: model_answer_criteria NEVER exposed to students
"""

import json
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User, UserTier
from app.models.assessment import AssessmentQuestion, AssessmentResult
from app.models.llm_usage import LLMUsage
from app.schemas.assessment import (
    AssessmentQuestionResponse,
    AssessmentGradeResponse,
    AssessmentResultSummary
)
from app.services.llm_service import llm_service
from app.services.exceptions import LLMUnavailableError, LLMParseError
from app.config import settings


class AssessmentService:
    """
    Service for LLM-graded written assessments.
    
    Provides conceptual evaluation beyond MCQ right/wrong.
    """
    
    # System prompt for educational grading
    SYSTEM_PROMPT = """You are an expert educator grading a student's written answer for an AI Agent Development course. Grade based ONLY on the provided course content and the model answer criteria. Do not give credit for concepts not covered in the provided chapter content. Return ONLY valid JSON matching the specified schema. No preamble, no markdown, no explanation outside JSON. Hallucination guard: If the student mentions concepts not in the course content, do not mark them as correct."""
    
    async def get_questions(
        self,
        chapter_id: str,
        user: User,
        db: AsyncSession
    ) -> List[AssessmentQuestionResponse]:
        """
        Get open-ended assessment questions for a chapter.
        
        CRITICAL: Does NOT return model_answer_criteria
        
        Args:
            chapter_id: Chapter identifier
            user: Current user
            db: Async database session
            
        Returns:
            List of questions (without criteria)
            
        Raises:
            HTTPException: 403 if user is not premium/pro tier
        """
        # Premium gate check
        if user.tier not in [UserTier.PREMIUM, UserTier.PRO]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "PREMIUM_REQUIRED",
                    "message": "LLM-graded assessments are a premium feature. Upgrade to access.",
                    "upgrade_url": "/upgrade"
                }
            )
        
        # Check chapter access
        from app.services.access_service import AccessService
        access_service = AccessService()
        has_access = await access_service.check_chapter_access(
            chapter_id=chapter_id,
            user=user,
            db=db
        )
        
        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "CHAPTER_LOCKED",
                    "message": f"Chapter {chapter_id} is locked. Upgrade to access."
                }
            )
        
        # Query questions (WITHOUT model_answer_criteria)
        stmt = (
            select(
                AssessmentQuestion.id,
                AssessmentQuestion.question_text,
                AssessmentQuestion.difficulty,
                AssessmentQuestion.sequence_order
            )
            .where(AssessmentQuestion.chapter_id == chapter_id)
            .order_by(AssessmentQuestion.sequence_order)
        )
        
        result = await db.execute(stmt)
        questions = result.all()
        
        # Convert to response objects
        return [
            AssessmentQuestionResponse(
                question_id=str(q.id),
                question_text=q.question_text,
                difficulty=q.difficulty
            )
            for q in questions
        ]
    
    async def grade_answer(
        self,
        chapter_id: str,
        question_id: UUID,
        answer_text: str,
        user: User,
        db: AsyncSession
    ) -> AssessmentGradeResponse:
        """
        Grade a written answer using LLM analysis.
        
        Args:
            chapter_id: Chapter identifier
            question_id: Question UUID
            answer_text: Student's written answer
            user: Current user
            db: Async database session
            
        Returns:
            Graded assessment with detailed feedback
            
        Raises:
            HTTPException: 403 if not premium, 422 if word count invalid
            HTTPException: 503 if LLM unavailable
        """
        # 1. Premium gate check
        if user.tier not in [UserTier.PREMIUM, UserTier.PRO]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "PREMIUM_REQUIRED",
                    "message": "LLM-graded assessments are a premium feature. Upgrade to access.",
                    "upgrade_url": "/upgrade"
                }
            )
        
        # 2. Validate word count BEFORE LLM call (no wasted tokens)
        word_count = len(answer_text.split())
        if word_count < 20:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "error": "ANSWER_TOO_SHORT",
                    "message": f"Answer must be at least 20 words (currently {word_count})",
                    "word_count": word_count,
                    "minimum": 20
                }
            )
        if word_count > 500:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "error": "ANSWER_TOO_LONG",
                    "message": f"Answer must be at most 500 words (currently {word_count})",
                    "word_count": word_count,
                    "maximum": 500
                }
            )
        
        # 3. Fetch question with model_answer_criteria
        stmt = select(AssessmentQuestion).where(
            AssessmentQuestion.id == question_id,
            AssessmentQuestion.chapter_id == chapter_id
        )
        result = await db.execute(stmt)
        question = result.scalar_one_or_none()
        
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "QUESTION_NOT_FOUND",
                    "message": f"Question {question_id} not found in chapter {chapter_id}"
                }
            )
        
        # 4. Fetch chapter content from R2 (for grounding)
        from app.services.r2_service import r2_service
        try:
            chapter_content = await r2_service.get_chapter_content(chapter_id)
        except Exception:
            # Fallback: use question criteria only if R2 fails
            chapter_content = ""
        
        # 5. Build LLM prompts
        user_prompt = f"""Chapter Content (use as grading reference):
{chapter_content}

Question: {question.question_text}

Model Answer Criteria: {question.model_answer_criteria}

Student's Answer: {answer_text}

Grade this answer and return JSON with this exact schema:
{{
  "score": 85,
  "grade": "B",
  "correct_concepts": ["concept1", "concept2"],
  "missing_concepts": ["concept3"],
  "feedback": "Your answer demonstrates a solid understanding of...",
  "improvement_suggestions": "To improve, consider adding...",
  "word_count": 120
}}

Grade based ONLY on the provided course content and model answer criteria. Do not give credit for concepts not covered in the course content."""
        
        # 6. Call LLM service
        try:
            llm_response, llm_usage = await llm_service.call_claude(
                system_prompt=self.SYSTEM_PROMPT,
                user_prompt=user_prompt,
                max_tokens=settings.LLM_MAX_TOKENS,
                feature_name="assessment_grading",
                user_id=str(user.id),
                db=db
            )
            
            # 7. Parse LLM response
            try:
                response = AssessmentGradeResponse(
                    score=llm_response["score"],
                    grade=llm_response["grade"],
                    correct_concepts=llm_response["correct_concepts"],
                    missing_concepts=llm_response["missing_concepts"],
                    feedback=llm_response["feedback"],
                    improvement_suggestions=llm_response["improvement_suggestions"],
                    word_count=word_count
                )
            except (KeyError, ValueError) as e:
                raise LLMParseError(
                    f"LLM response missing required fields: {str(e)}",
                    raw_response=str(llm_response)
                )
            
            # 8. Store result in database
            assessment_result = AssessmentResult(
                user_id=user.id,
                question_id=question_id,
                chapter_id=chapter_id,
                answer_text=answer_text,
                score=response.score,
                grade=response.grade,
                correct_concepts=response.correct_concepts,
                missing_concepts=response.missing_concepts,
                feedback=response.feedback,
                improvement_suggestions=response.improvement_suggestions,
                word_count=word_count,
                llm_usage_id=llm_usage.id
            )
            
            db.add(assessment_result)
            await db.commit()
            await db.refresh(assessment_result)
            
            return response
            
        except LLMUnavailableError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={
                    "error": "LLM_UNAVAILABLE",
                    "message": "Assessment grading temporarily unavailable. Please retry.",
                    "retry_after": 30  # Suggest retry in 30 seconds
                }
            )
    
    async def get_results(
        self,
        chapter_id: str,
        user: User,
        db: AsyncSession
    ) -> List[AssessmentResultSummary]:
        """
        Get all past assessment results for a chapter.
        
        NO LLM CALL - returns cached results from database.
        
        Args:
            chapter_id: Chapter identifier
            user: Current user
            db: Async database session
            
        Returns:
            List of assessment summaries
        """
        # Premium gate check
        if user.tier not in [UserTier.PREMIUM, UserTier.PRO]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "PREMIUM_REQUIRED",
                    "message": "LLM-graded assessments are a premium feature. Upgrade to access.",
                    "upgrade_url": "/upgrade"
                }
            )
        
        # Query results
        stmt = (
            select(AssessmentResult)
            .where(
                AssessmentResult.user_id == user.id,
                AssessmentResult.chapter_id == chapter_id
            )
            .order_by(AssessmentResult.submitted_at.desc())
        )
        
        result = await db.execute(stmt)
        assessments = result.scalars().all()
        
        # Convert to summaries
        return [
            assessment.to_summary_dict()
            for assessment in assessments
        ]


# Global instance for dependency injection
assessment_service = AssessmentService()
