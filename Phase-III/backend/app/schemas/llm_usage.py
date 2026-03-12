"""
Pydantic Schemas for LLM Usage Tracking

Cost transparency and usage analytics.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime


class FeatureUsage(BaseModel):
    """Usage breakdown for a single feature."""
    
    feature_name: str = Field(..., description="Feature identifier")
    calls: int = Field(..., ge=0, description="Number of calls this month")
    cost_usd: float = Field(..., ge=0, description="Total cost in USD")
    
    class Config:
        json_schema_extra = {
            "example": {
                "feature_name": "adaptive_path",
                "calls": 3,
                "cost_usd": 0.18
            }
        }


class CostSummaryResponse(BaseModel):
    """Monthly LLM usage cost summary."""
    
    current_month: str = Field(..., description="Month (YYYY-MM format)")
    total_cost_usd: float = Field(..., ge=0, description="Total cost this month")
    monthly_cap_usd: float = Field(..., ge=0, description="Monthly budget cap")
    remaining_usd: float = Field(..., ge=0, description="Remaining budget")
    usage_by_feature: Dict[str, FeatureUsage] = Field(
        ..., 
        description="Breakdown by feature"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "current_month": "2026-03",
                "total_cost_usd": 0.45,
                "monthly_cap_usd": 2.00,
                "remaining_usd": 1.55,
                "usage_by_feature": {
                    "adaptive_path": {
                        "feature_name": "adaptive_path",
                        "calls": 3,
                        "cost_usd": 0.18
                    },
                    "assessment_grading": {
                        "feature_name": "assessment_grading",
                        "calls": 15,
                        "cost_usd": 0.27
                    }
                }
            }
        }


class FreeUserCostSummary(BaseModel):
    """Cost summary for free users (no hybrid features used)."""
    
    total_cost_usd: float = Field(0, description="Always 0 for free users")
    monthly_cap_usd: float = Field(0, description="No cap for free users")
    remaining_usd: float = Field(0, description="No usage")
    note: str = Field(..., description="Explanation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_cost_usd": 0,
                "monthly_cap_usd": 0,
                "remaining_usd": 0,
                "note": "No hybrid features used - free tier has no access to Phase 2 features"
            }
        }
