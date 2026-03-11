# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import String, DateTime, Enum as SQLEnum, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserTier(str, Enum):
    """User subscription tier."""
    FREE = "free"
    PREMIUM = "premium"
    PRO = "pro"


class User(Base):
    """User model for authentication and progress tracking."""
    
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    api_key: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    tier: Mapped[UserTier] = mapped_column(
        SQLEnum(UserTier),
        nullable=False,
        default=UserTier.FREE
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )
    
    # Relationships
    chapter_progress = relationship("ChapterProgress", back_populates="user", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")
    daily_activity = relationship("DailyActivity", back_populates="user", cascade="all, delete-orphan")
