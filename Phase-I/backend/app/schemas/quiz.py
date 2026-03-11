# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class QuizQuestion(BaseModel):
    """Quiz question (WITHOUT correct_answer)."""
    id: str
    question_text: str
    question_type: str  # 'mcq' or 'true_false'
    options: Optional[List[str]] = None  # For MCQ
    sequence_order: int


class QuestionResult(BaseModel):
    """Result for a single question."""
    question_id: str
    correct: bool
    correct_answer: str
    explanation: Optional[str] = None
    user_answer: str


class QuizResult(BaseModel):
    """Quiz grading result."""
    score: int
    total: int
    percentage: float
    results: List[QuestionResult]
    attempt_id: Optional[str] = None


class QuizAttemptSummary(BaseModel):
    """Summary of quiz attempts for a chapter."""
    chapter_id: str
    best_score: int
    total: int
    percentage: float
    attempts_count: int
    last_attempted_at: Optional[datetime] = None
