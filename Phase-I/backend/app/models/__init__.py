# Models package
# PHASE 1 COMPLIANCE: No LLM API calls

# Import all models to register them with SQLAlchemy
# This must be done before using any model with relationships
from app.models.user import User
from app.models.chapter import Chapter
from app.models.quiz import QuizQuestion, QuizAttempt
from app.models.progress import ChapterProgress, DailyActivity

__all__ = ["User", "Chapter", "QuizQuestion", "QuizAttempt", "ChapterProgress", "DailyActivity"]
