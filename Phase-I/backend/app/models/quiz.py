# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

import uuid
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, Text, DateTime, Numeric, JSON as JSONB, Uuid as UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class QuizQuestion(Base):
    """Quiz question model.
    
    IMPORTANT: correct_answer is NEVER returned in API responses.
    It's only used server-side for grading.
    """
    
    __tablename__ = "quiz_questions"
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    chapter_id: Mapped[str] = mapped_column(String(20), ForeignKey("chapters.id"), nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(String(20), nullable=False)  # 'mcq' or 'true_false'
    options: Mapped[list | None] = mapped_column(JSONB)  # Array of options for MCQ
    correct_answer: Mapped[str] = mapped_column(Text, nullable=False)  # NEVER expose this
    explanation: Mapped[str | None] = mapped_column(Text)
    sequence_order: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Relationships
    chapter = relationship("Chapter", back_populates="quiz_questions")


class QuizAttempt(Base):
    """Quiz attempt model for tracking user submissions."""
    
    __tablename__ = "quiz_attempts"
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    chapter_id: Mapped[str] = mapped_column(String(20), ForeignKey("chapters.id"), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[int] = mapped_column(Integer, nullable=False)
    percentage: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="quiz_attempts")
