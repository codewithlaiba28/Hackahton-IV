# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

import uuid
from datetime import datetime, date
from sqlalchemy import String, DateTime, ForeignKey, UniqueConstraint, Date, Uuid as UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ChapterProgress(Base):
    """Track user's progress through chapters."""
    
    __tablename__ = "chapter_progress"
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    chapter_id: Mapped[str] = mapped_column(String(20), ForeignKey("chapters.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="not_started")
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    
    # Ensure one progress record per user per chapter
    __table_args__ = (
        UniqueConstraint('user_id', 'chapter_id', name='uq_user_chapter_progress'),
    )
    
    # Relationships
    user = relationship("User", back_populates="chapter_progress")
    chapter = relationship("Chapter", back_populates="chapter_progress")


class DailyActivity(Base):
    """Track daily activity for streak calculation."""
    
    __tablename__ = "daily_activity"
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    activity_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    # Ensure one activity record per user per day
    __table_args__ = (
        UniqueConstraint('user_id', 'activity_date', name='uq_user_daily_activity'),
    )
    
    # Relationships
    user = relationship("User", back_populates="daily_activity")
