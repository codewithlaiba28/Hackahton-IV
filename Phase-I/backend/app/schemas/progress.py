# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class ProgressSummary(BaseModel):
    """Complete progress summary for a user."""
    chapters_completed: List[str]
    chapters_in_progress: List[str]
    overall_percentage: float
    current_streak_days: int
    longest_streak_days: int
    last_activity_date: Optional[date] = None


class UpdateProgressRequest(BaseModel):
    """Request to update chapter progress."""
    status: str = Field(..., description="Status: 'not_started', 'in_progress', or 'completed'")
