# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user
from app.database import get_db
from app.models.user import User, UserTier
from app.models.llm_usage import LLMUsage
from app.schemas.common import APIResponse
from app.schemas.user import UserResponse
from app.schemas.llm_usage import CostSummaryResponse, FeatureUsage, FreeUserCostSummary

router = APIRouter()


@router.get("/me", response_model=APIResponse[UserResponse])
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information."""
    return APIResponse(data=UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        tier=current_user.tier.value
    ))


@router.get(
    "/me/cost-summary",
    response_model=APIResponse[CostSummaryResponse | FreeUserCostSummary],
    summary="Get Monthly LLM Usage Cost",
    response_description="Monthly cost breakdown by feature"
)
async def get_cost_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current month's LLM usage cost breakdown.
    
    **Free Users:** Always returns $0 cost (no access to hybrid features)
    
    **Premium/Pro Users:** Shows actual usage and remaining budget
    
    **Constitutional Compliance:**
    - Principle X: Cost transparency (CC-04)
    - Available to all tiers (free sees $0)
    """
    # Get current month in YYYY-MM format
    current_month = datetime.utcnow().strftime("%Y-%m")
    
    # Free users always see $0
    if current_user.tier == UserTier.FREE:
        return APIResponse(
            data=FreeUserCostSummary(
                total_cost_usd=0,
                monthly_cap_usd=0,
                remaining_usd=0,
                note="No hybrid features used - free tier has no access to Phase 2 features"
            ),
            error=None,
            meta={"message": "Free tier - no hybrid feature access"}
        )
    
    # Set monthly cap based on tier
    monthly_cap = Decimal("2.00") if current_user.tier == UserTier.PREMIUM else Decimal("5.00")
    
    # Query total cost for current month
    stmt = select(
        func.sum(LLMUsage.cost_usd).label("total_cost"),
        func.count(LLMUsage.id).label("total_calls")
    ).where(
        LLMUsage.user_id == current_user.id,
        func.date_trunc("month", LLMUsage.created_at) == func.date_trunc("month", datetime.utcnow())
    )
    
    result = await db.execute(stmt)
    row = result.first()
    
    total_cost = Decimal(str(row.total_cost)) if row.total_cost else Decimal("0")
    total_calls = row.total_calls or 0
    
    # Query breakdown by feature
    feature_stmt = select(
        LLMUsage.feature_name,
        func.sum(LLMUsage.cost_usd).label("feature_cost"),
        func.count(LLMUsage.id).label("feature_calls")
    ).where(
        LLMUsage.user_id == current_user.id,
        func.date_trunc("month", LLMUsage.created_at) == func.date_trunc("month", datetime.utcnow())
    ).group_by(LLMUsage.feature_name)
    
    feature_result = await db.execute(feature_stmt)
    feature_rows = feature_result.all()
    
    # Build usage by feature
    usage_by_feature = {}
    for feature_row in feature_rows:
        usage_by_feature[feature_row.feature_name] = FeatureUsage(
            feature_name=feature_row.feature_name,
            calls=feature_row.feature_calls,
            cost_usd=float(feature_row.feature_cost)
        )
    
    # Calculate remaining budget
    remaining = monthly_cap - total_cost
    
    return APIResponse(
        data=CostSummaryResponse(
            current_month=current_month,
            total_cost_usd=float(total_cost),
            monthly_cap_usd=float(monthly_cap),
            remaining_usd=float(remaining),
            usage_by_feature=usage_by_feature
        ),
        error=None,
        meta={
            "message": "Cost summary retrieved successfully",
            "warning": "Approaching monthly limit" if remaining < monthly_cap * Decimal("0.2") else None
        }
    )
