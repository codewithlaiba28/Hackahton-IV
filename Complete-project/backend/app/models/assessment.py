"""
Assessment Models

Open-ended written assessments with LLM-graded feedback.
Separate from MCQ quiz_questions - these require semantic understanding.
"""

from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Index, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class AssessmentQuestion(Base):
    """
    Open-ended assessment questions for conceptual evaluation.
    
    Unlike MCQ quiz questions, these require students to write
    paragraph-length answers demonstrating conceptual understanding.
    
    Constitutional Compliance:
    - model_answer_criteria NEVER exposed to students (only used for LLM grading)
    - Premium-gated access (Principle VIII)
    """
    
    __tablename__ = "assessment_questions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(String(20), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    model_answer_criteria = Column(Text, nullable=False)  # NEVER exposed to students
    difficulty = Column(String(20), nullable=False)  # 'conceptual', 'analytical', 'applied'
    sequence_order = Column(Integer, nullable=False)
    
    # Relationships
    chapter = relationship("Chapter", back_populates="assessment_questions")
    results = relationship("AssessmentResult", back_populates="question", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<AssessmentQuestion(chapter={self.chapter_id}, difficulty={self.difficulty})>"
    
    def to_public_dict(self) -> dict:
        """
        Convert to dictionary for API response.
        CRITICAL: Does NOT include model_answer_criteria
        """
        return {
            "question_id": str(self.id),
            "question_text": self.question_text,
            "difficulty": self.difficulty
        }


class AssessmentResult(Base):
    """
    LLM-graded assessment results.
    
    Stores student's written answer and LLM-generated feedback.
    Provides detailed educational feedback beyond MCQ right/wrong.
    
    Constitutional Compliance:
    - Premium-gated only (Principle VIII)
    - Cost-tracked via llm_usage_id (Principle X)
    - User-initiated (student submits answer explicitly)
    """
    
    __tablename__ = "assessment_results"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(UUID(as_uuid=True), ForeignKey("assessment_questions.id", ondelete="CASCADE"), nullable=False)
    chapter_id = Column(String(20), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Student's answer
    answer_text = Column(Text, nullable=False)
    
    # LLM-graded results
    score = Column(Integer, nullable=False)  # 0-100
    grade = Column(String(2), nullable=False)  # A/B/C/D/F
    correct_concepts = Column(JSONB, nullable=False)  # List of concepts student understood
    missing_concepts = Column(JSONB, nullable=False)  # List of concepts student missed
    feedback = Column(Text, nullable=False)  # Educational feedback
    improvement_suggestions = Column(Text, nullable=False)  # Specific suggestions
    word_count = Column(Integer, nullable=False)
    
    # Link to LLM usage for cost tracking
    llm_usage_id = Column(UUID(as_uuid=True), ForeignKey("llm_usage.id"), nullable=True)
    llm_usage = relationship("LLMUsage")
    
    submitted_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="assessment_results")
    question = relationship("AssessmentQuestion", back_populates="results")
    chapter = relationship("Chapter")
    
    def __repr__(self):
        return f"<AssessmentResult(user_id={self.user_id}, score={self.score}, grade={self.grade})>"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API response"""
        return {
            "result_id": str(self.id),
            "question_text": self.question.question_text,
            "score": self.score,
            "grade": self.grade,
            "correct_concepts": self.correct_concepts,
            "missing_concepts": self.missing_concepts,
            "feedback": self.feedback,
            "improvement_suggestions": self.improvement_suggestions,
            "word_count": self.word_count,
            "submitted_at": self.submitted_at.isoformat()
        }
    
    def to_summary_dict(self) -> dict:
        """Convert to summary for list responses"""
        return {
            "result_id": str(self.id),
            "question_text": self.question.question_text[:100] + "...",
            "score": self.score,
            "grade": self.grade,
            "submitted_at": self.submitted_at.isoformat()
        }


# Constraints
__table_args__ = (
    CheckConstraint("score >= 0 AND score <= 100", name="check_assessment_score_range"),
    CheckConstraint("word_count >= 0", name="check_word_count_positive"),
)


# Index for efficient user result queries
Index(
    "ix_assessment_results_user_chapter",
    AssessmentResult.user_id,
    AssessmentResult.chapter_id
)
