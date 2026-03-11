# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

from sqlalchemy import String, Integer, Boolean, ForeignKey, Text, DateTime, Text as TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.database import Base


class Chapter(Base):
    """Chapter model for course content metadata.
    
    Note: Actual content is stored in Cloudflare R2, not in the database.
    This model only stores metadata for listing and navigation.
    """
    
    __tablename__ = "chapters"
    
    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), nullable=False)
    estimated_read_min: Mapped[int] = mapped_column(Integer, nullable=False)
    is_free: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sequence_order: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    
    # Navigation
    prev_chapter_id: Mapped[str | None] = mapped_column(String(20), ForeignKey("chapters.id"))
    next_chapter_id: Mapped[str | None] = mapped_column(String(20), ForeignKey("chapters.id"))
    
    # R2 storage key for content
    r2_content_key: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Full-text search vector (PostgreSQL)
    search_vector: Mapped[TSVECTOR | None] = mapped_column(TSVECTOR)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Self-referential relationships for navigation
    prev_chapter = relationship("Chapter", foreign_keys=[prev_chapter_id], remote_side="Chapter.id")
    next_chapter = relationship("Chapter", foreign_keys=[next_chapter_id], remote_side="Chapter.id")
    
    # Relationships
    quiz_questions = relationship("QuizQuestion", back_populates="chapter", cascade="all, delete-orphan")
    chapter_progress = relationship("ChapterProgress", back_populates="chapter", cascade="all, delete-orphan")
