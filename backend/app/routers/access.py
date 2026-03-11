# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.chapter import Chapter
from app.schemas.common import APIResponse
from app.schemas.user import AccessCheckResponse
from app.services.access_service import get_access_service

router = APIRouter()


@router.get("/check", response_model=APIResponse[AccessCheckResponse])
async def check_access(
    resource_type: str,
    resource_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Check if user has access to a resource."""
    access_service = get_access_service()

    # Only chapter access is implemented
    if resource_type != "chapter":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported resource type: {resource_type}"
        )

    # Get chapter from DB
    result = await db.execute(
        select(Chapter).where(Chapter.id == resource_id)
    )
    chapter = result.scalar_one_or_none()

    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chapter {resource_id} not found"
        )

    # Check access using service
    access_result = access_service.check_chapter_access(current_user, chapter)

    return APIResponse(data=AccessCheckResponse(
        has_access=access_result.has_access,
        reason=access_result.reason,
        upgrade_required=access_result.upgrade_required
    ))
