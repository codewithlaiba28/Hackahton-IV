# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.user import UserResponse

router = APIRouter()


@router.get("/me", response_model=APIResponse[UserResponse])
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information."""
    return APIResponse(data=UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        tier=current_user.tier.value
    ))
