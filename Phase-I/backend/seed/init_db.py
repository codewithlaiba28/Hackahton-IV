import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# Import all models to register them with Base.metadata
from app.models.user import User
from app.models.chapter import Chapter
from app.models.progress import ChapterProgress, DailyActivity
from app.models.quiz import QuizQuestion, QuizAttempt

from app.database import init_db

if __name__ == "__main__":
    print("Initializing Database with Base.metadata.create_all()...")
    asyncio.run(init_db())
    print("Database Initialized!")
