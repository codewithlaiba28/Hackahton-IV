# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserTier(str):
    """User subscription tier constants."""
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
    api_key: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=True)
    password_salt: Mapped[str] = mapped_column(String(255), nullable=True)
    tier: Mapped[UserTier] = mapped_column(
        String(20),
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
    llm_usage_records = relationship("LLMUsage", back_populates="user", cascade="all, delete-orphan")
    adaptive_recommendations = relationship("AdaptiveRecommendation", back_populates="user", cascade="all, delete-orphan")
    assessment_results = relationship("AssessmentResult", back_populates="user", cascade="all, delete-orphan")
