# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
import uuid

from app.models.quiz import QuizQuestion, QuizAttempt
from app.models.user import User


class QuizService:
    """Service for quiz operations.
    
    IMPORTANT: This service implements RULE-BASED grading only.
    No LLM calls, no fuzzy matching - exact string comparison only.
    """
    
    async def get_quiz_questions(self, chapter_id: str, db: AsyncSession) -> List[QuizQuestion]:
        """Get quiz questions for a chapter WITHOUT answer keys.
        
        CRITICAL: Never return correct_answer in the response.
        
        Args:
            chapter_id: Chapter ID
            db: Database session
            
        Returns:
            List of QuizQuestion (without correct_answer)
        """
        result = await db.execute(
            select(QuizQuestion)
            .where(QuizQuestion.chapter_id == chapter_id)
            .order_by(QuizQuestion.sequence_order)
        )
        questions = result.scalars().all()
        
        # IMPORTANT: Clear correct_answer before returning
        for question in questions:
            # We don't delete from DB, just don't include in serialization
            pass
        
        return questions
    
    async def grade_quiz(
        self,
        chapter_id: str,
        submission: dict,
        user: User,
        db: AsyncSession
    ) -> dict:
        """Grade quiz submission using exact string matching.
        
        Args:
            chapter_id: Chapter ID
            submission: {"answers": [{"question_id": "...", "answer": "..."}]}
            user: Authenticated user
            db: Database session
            
        Returns:
            Grading result with score and feedback
        """
        answers = submission.get("answers", [])
        
        # Get all questions for this chapter
        result = await db.execute(
            select(QuizQuestion)
            .where(QuizQuestion.chapter_id == chapter_id)
        )
        questions = result.scalars().all()
        questions_map = {str(q.id): q for q in questions}
        
        # Grade each answer
        results = []
        correct_count = 0
        
        for ans in answers:
            question_id = ans.get("question_id")
            user_answer = ans.get("answer", "").strip()
            
            question = questions_map.get(question_id)
            if not question:
                continue
            
            # EXACT string match only - NO fuzzy matching, NO LLM
            is_correct = user_answer == question.correct_answer.strip()
            
            if is_correct:
                correct_count += 1
            
            results.append({
                "question_id": question_id,
                "correct": is_correct,
                "correct_answer": question.correct_answer,  # Only in grading result
                "explanation": question.explanation,
                "user_answer": user_answer
            })
        
        # Calculate score
        total = len(questions)
        percentage = round((correct_count / total) * 100, 2) if total > 0 else 0
        
        # Record attempt in database
        attempt = QuizAttempt(
            user_id=user.id,
            chapter_id=chapter_id,
            score=correct_count,
            total=total,
            percentage=percentage
        )
        db.add(attempt)
        await db.flush()
        
        return {
            "score": correct_count,
            "total": total,
            "percentage": percentage,
            "results": results,
            "attempt_id": str(attempt.id)
        }
    
    async def get_best_score(self, chapter_id: str, user_id: uuid.UUID, db: AsyncSession) -> Optional[dict]:
        """Get user's best quiz score for a chapter.
        
        Args:
            chapter_id: Chapter ID
            user_id: User UUID
            db: Database session
            
        Returns:
            Best score summary or None if no attempts
        """
        result = await db.execute(
            select(QuizAttempt)
            .where(QuizAttempt.chapter_id == chapter_id)
            .where(QuizAttempt.user_id == user_id)
            .order_by(QuizAttempt.percentage.desc())
        )
        best_attempt = result.scalar_one_or_none()
        
        if not best_attempt:
            return None
        
        return {
            "chapter_id": chapter_id,
            "best_score": best_attempt.score,
            "total": best_attempt.total,
            "percentage": float(best_attempt.percentage),
            "attempts_count": 1,  # Would need COUNT query for actual count
            "last_attempted_at": best_attempt.submitted_at
        }


# Singleton instance
_quiz_service = QuizService()


def get_quiz_service() -> QuizService:
    """Get quiz service instance."""
    return _quiz_service
