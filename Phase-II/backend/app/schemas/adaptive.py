"""
Pydantic Schemas for Adaptive Learning Path Feature

Request/Response models for Feature A.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class RecommendedChapter(BaseModel):
    """A single chapter recommendation with priority and rationale."""
    
    chapter_id: str = Field(..., description="Chapter ID (e.g., 'ch-003')")
    title: str = Field(..., description="Chapter title")
    priority: int = Field(..., ge=1, le=10, description="Priority (1=highest)")
    reason: str = Field(..., description="Why this chapter is recommended")
    estimated_time_minutes: int = Field(..., ge=5, le=120, description="Estimated study time")


class AdaptiveRecommendationResponse(BaseModel):
    """Complete personalized learning path recommendation."""
    
    recommended_chapters: List[RecommendedChapter] = Field(
        ..., 
        description="Ordered list of recommended chapters"
    )
    weak_areas: List[str] = Field(
        ..., 
        description="Identified knowledge gaps"
    )
    strengths: List[str] = Field(
        ..., 
        description="Student's strong areas"
    )
    overall_assessment: str = Field(
        ..., 
        description="Narrative summary of progress"
    )
    suggested_daily_goal_minutes: int = Field(
        ..., 
        ge=15, 
        le=180, 
        description="Recommended daily study time"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "recommended_chapters": [
                    {
                        "chapter_id": "ch-003",
                        "title": "MCP Basics",
                        "priority": 1,
                        "reason": "Your quiz score (40%) suggests gaps in prerequisites",
                        "estimated_time_minutes": 30
                    }
                ],
                "weak_areas": ["MCP protocol structure", "Agent tool integration"],
                "strengths": ["Claude Agent SDK", "Goal-directed behavior"],
                "overall_assessment": "You show strong understanding of agent fundamentals but need to strengthen MCP knowledge before advancing.",
                "suggested_daily_goal_minutes": 45
            }
        }


class AdaptivePathRequest(BaseModel):
    """
    Request to generate adaptive learning path.
    
    Empty body - user derived from auth token.
    """
    pass


class CachedRecommendation(BaseModel):
    """Previously generated recommendation (no LLM call)."""
    
    id: str
    recommended_chapters: List[RecommendedChapter]
    weak_areas: List[str]
    strengths: List[str]
    overall_assessment: str
    suggested_daily_goal_minutes: int
    created_at: datetime
    
    class Config:
        from_attributes = True
