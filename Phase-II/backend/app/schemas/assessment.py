"""
Pydantic Schemas for LLM-Graded Assessments Feature

Request/Response models for Feature B.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional
from datetime import datetime
import uuid


class AssessmentQuestionResponse(BaseModel):
    """
    Open-ended assessment question (public view).
    
    CRITICAL: Does NOT include model_answer_criteria
    """
    
    question_id: str = Field(..., description="Question UUID")
    question_text: str = Field(..., description="The question to answer")
    difficulty: str = Field(..., description="Question difficulty level")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question_id": "550e8400-e29b-41d4-a716-446655440000",
                "question_text": "In your own words, explain what an AI Agent is and how it differs from a traditional software program.",
                "difficulty": "conceptual"
            }
        }


class SubmitAnswerRequest(BaseModel):
    """Student submitting an answer for grading."""
    
    question_id: str = Field(..., description="Question UUID")
    answer_text: str = Field(..., min_length=20, max_length=2000, description="Student's written answer (20-500 words)")
    
    @field_validator('answer_text')
    @classmethod
    def validate_word_count(cls, v: str) -> str:
        """Validate answer is between 20-500 words."""
        word_count = len(v.split())
        if word_count < 20:
            raise ValueError(f"Answer must be at least 20 words (currently {word_count})")
        if word_count > 500:
            raise ValueError(f"Answer must be at most 500 words (currently {word_count})")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "question_id": "550e8400-e29b-41d4-a716-446655440000",
                "answer_text": "An AI Agent is an autonomous system that perceives its environment through sensors and acts upon it through actuators to achieve goals..."
            }
        }


class AssessmentGradeResponse(BaseModel):
    """LLM-graded assessment result."""
    
    score: int = Field(..., ge=0, le=100, description="Score 0-100")
    grade: str = Field(..., description="Letter grade (A/B/C/D/F)")
    correct_concepts: List[str] = Field(..., description="Concepts student understood")
    missing_concepts: List[str] = Field(..., description="Concepts student missed")
    feedback: str = Field(..., description="Educational feedback")
    improvement_suggestions: str = Field(..., description="Specific suggestions for improvement")
    word_count: int = Field(..., ge=0, description="Actual word count of answer")
    
    class Config:
        json_schema_extra = {
            "example": {
                "score": 85,
                "grade": "B",
                "correct_concepts": ["Autonomous system", "Perception-action loop", "Goal-directed behavior"],
                "missing_concepts": ["Learning capability", "Environment modeling"],
                "feedback": "Your answer demonstrates a solid understanding of AI agents as autonomous systems with perception-action loops.",
                "improvement_suggestions": "Consider adding how agents can learn from experience and build internal models.",
                "word_count": 120
            }
        }


class AssessmentResultSummary(BaseModel):
    """Summary of a past assessment result."""
    
    result_id: str = Field(..., description="Result UUID")
    question_text: str = Field(..., description="Question text (truncated)")
    score: int = Field(..., ge=0, le=100, description="Score 0-100")
    grade: str = Field(..., description="Letter grade")
    submitted_at: datetime = Field(..., description="When submitted")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "result_id": "550e8400-e29b-41d4-a716-446655440001",
                "question_text": "In your own words, explain what an AI Agent is...",
                "score": 85,
                "grade": "B",
                "submitted_at": "2026-03-11T10:30:00Z"
            }
        }
