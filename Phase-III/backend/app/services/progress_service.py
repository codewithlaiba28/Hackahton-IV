# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import List, Optional, Tuple
from datetime import datetime, date, timedelta
import uuid

from app.models.user import User
from app.models.chapter import Chapter
from app.models.quiz import QuizAttempt
from app.models.progress import ChapterProgress, DailyActivity


class ProgressService:
    """Service for tracking and aggregating user progress."""
    
    async def update_chapter_progress(
        self,
        user_id: uuid.UUID,
        chapter_id: str,
        status: str,
        db: AsyncSession
    ) -> ChapterProgress:
        """Update chapter progress for a user.
        
        Args:
            user_id: User UUID
            chapter_id: Chapter ID
            status: 'not_started', 'in_progress', or 'completed'
            db: Database session
            
        Returns:
            Updated ChapterProgress
        """
        # Upsert chapter progress
        result = await db.execute(
            select(ChapterProgress)
            .where(ChapterProgress.user_id == user_id)
            .where(ChapterProgress.chapter_id == chapter_id)
        )
        progress = result.scalar_one_or_none()
        
        if not progress:
            progress = ChapterProgress(
                user_id=user_id,
                chapter_id=chapter_id,
                status=status
            )
            db.add(progress)
        else:
            progress.status = status
        
        # Set timestamps based on status
        if status == "in_progress" and not progress.started_at:
            progress.started_at = datetime.utcnow()
        elif status == "completed":
            if not progress.started_at:
                progress.started_at = datetime.utcnow()
            if not progress.completed_at:
                progress.completed_at = datetime.utcnow()
            
            # Record daily activity for streak
            await self._record_activity(user_id, db)
        
        await db.flush()
        await db.refresh(progress)
        return progress
    
    async def _record_activity(self, user_id: uuid.UUID, db: AsyncSession) -> None:
        """Record daily activity for streak tracking."""
        today = date.today()
        
        # Check if already recorded today
        result = await db.execute(
            select(DailyActivity)
            .where(DailyActivity.user_id == user_id)
            .where(DailyActivity.activity_date == today)
        )
        existing = result.scalar_one_or_none()
        
        if not existing:
            activity = DailyActivity(user_id=user_id, activity_date=today)
            db.add(activity)
    
    async def get_progress_summary(self, user_id: uuid.UUID, db: AsyncSession) -> dict:
        """Get complete progress summary for a user.
        
        Args:
            user_id: User UUID
            db: Database session
            
        Returns:
            Dictionary with progress summary
        """
        # Get all chapter progress
        result = await db.execute(
            select(ChapterProgress)
            .options(selectinload(ChapterProgress.chapter))
            .where(ChapterProgress.user_id == user_id)
        )
        all_progress = result.scalars().all()
        
        # Calculate statistics
        completed = [p for p in all_progress if p.status == "completed"]
        in_progress = [p for p in all_progress if p.status == "in_progress"]
        
        # Get total chapters
        total_chapters_result = await db.execute(select(func.count(Chapter.id)))
        total_chapters = total_chapters_result.scalar() or 0
        
        # Get best quiz score
        best_score_result = await db.execute(
            select(func.max(QuizAttempt.percentage))
            .where(QuizAttempt.user_id == user_id)
        )
        best_score = best_score_result.scalar() or 0
        
        # Get daily activity & study time
        activity_result = await db.execute(
            select(DailyActivity)
            .where(DailyActivity.user_id == user_id)
            .order_by(DailyActivity.activity_date.asc())
        )
        activities = activity_result.scalars().all()
        
        total_study_time = 0
        formatted_activity = []
        for activity in activities:
            formatted_activity.append({
                "date": activity.activity_date.isoformat(),
                "chapters_completed": 0, # Should ideally be calculated per day
                "study_time": 0 # Should ideally be tracked
            })

        # Calculate streak
        current_streak, longest_streak = await self._calculate_streak(user_id, db)
        
        return {
            "chapters_completed": [p.chapter_id for p in completed],
            "chapters_in_progress": [p.chapter_id for p in in_progress],
            "overall_percentage": round((len(completed) / total_chapters) * 100, 2) if total_chapters > 0 else 0,
            "current_streak_days": current_streak,
            "longest_streak_days": longest_streak,
            "total_chapters": total_chapters,
            "best_quiz_score": float(best_score),
            "total_study_time": total_study_time,
            "last_activity_date": self._get_last_activity_date(all_progress),
            "daily_activity": formatted_activity
        }
    
    async def _calculate_streak(self, user_id: uuid.UUID, db: AsyncSession) -> Tuple[int, int]:
        """Calculate current and longest streak.
        
        Returns:
            Tuple of (current_streak, longest_streak)
        """
        result = await db.execute(
            select(DailyActivity.activity_date)
            .where(DailyActivity.user_id == user_id)
            .order_by(DailyActivity.activity_date.desc())
        )
        dates = [row[0] for row in result.all()]
        
        if not dates:
            return 0, 0
        
        # Calculate current streak
        current_streak = 1
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        # Check if streak is active (activity today or yesterday)
        if dates[0] not in [today, yesterday]:
            return 0, max(dates)  # Streak is broken
        
        # Count consecutive days
        for i in range(1, len(dates)):
            if dates[i-1] - dates[i] == timedelta(days=1):
                current_streak += 1
            else:
                break
        
        # Calculate longest streak
        longest_streak = current_streak
        temp_streak = 1
        
        for i in range(1, len(dates)):
            if dates[i-1] - dates[i] == timedelta(days=1):
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 1
        
        return current_streak, longest_streak
    
    def _get_last_activity_date(self, all_progress: List[ChapterProgress]) -> Optional[date]:
        """Get last activity date from progress list."""
        completed_dates = [p.completed_at.date() for p in all_progress if p.completed_at]
        return max(completed_dates) if completed_dates else None

    async def get_all_quiz_scores(self, user_id: uuid.UUID, db: AsyncSession) -> List[dict]:
        """Get all quiz scores for a user.

        Args:
            user_id: User UUID
            db: Database session

        Returns:
            List of quiz attempt summaries
        """
        result = await db.execute(
            select(QuizAttempt)
            .where(QuizAttempt.user_id == user_id)
            .order_by(QuizAttempt.submitted_at.desc())
        )
        attempts = result.scalars().all()

        return [
            {
                "attempt_id": str(attempt.id),
                "chapter_id": attempt.chapter_id,
                "score": attempt.score,
                "total": attempt.total,
                "percentage": float(attempt.percentage),
                "submitted_at": attempt.submitted_at.isoformat() if attempt.submitted_at else None
            }
            for attempt in attempts
        ]


# Singleton instance
_progress_service = ProgressService()


def get_progress_service() -> ProgressService:
    """Get progress service instance."""
    return _progress_service
