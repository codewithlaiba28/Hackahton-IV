# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.chapter import Chapter
from app.schemas.common import APIResponse
from app.schemas.chapter import ChapterMeta, ChapterDetail, ChapterListResponse
from app.services.r2_service import get_r2_service, ContentNotFoundError
from app.services.access_service import get_access_service

router = APIRouter()


@router.get("", response_model=APIResponse[ChapterListResponse])
async def list_chapters(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all chapters (metadata only).
    
    Free users see all chapters with is_locked flag.
    Premium users see all chapters unlocked.
    """
    result = await db.execute(
        select(Chapter).order_by(Chapter.sequence_order)
    )
    chapters = result.scalars().all()
    
    # Convert to response schema with is_locked flag
    is_premium = str(current_user.tier) in ["premium", "pro"]
    chapter_items = []
    
    for chapter in chapters:
        is_locked = not chapter.is_free and not is_premium
        chapter_items.append(ChapterMeta(
            id=chapter.id,
            title=chapter.title,
            difficulty=chapter.difficulty,
            estimated_read_min=chapter.estimated_read_min,
            is_free=chapter.is_free,
            is_locked=is_locked,
            sequence_order=chapter.sequence_order,
            prev_chapter_id=chapter.prev_chapter_id,
            next_chapter_id=chapter.next_chapter_id
        ))
    
    return APIResponse(data=ChapterListResponse(chapters=chapter_items))


@router.get("/{chapter_id}", response_model=APIResponse[ChapterDetail])
async def get_chapter(
    chapter_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get chapter content by ID.
    
    Returns full chapter content from R2.
    Freemium gate enforced - free users blocked from premium chapters.
    """
    # Get chapter metadata
    result = await db.execute(
        select(Chapter).where(Chapter.id == chapter_id)
    )
    chapter = result.scalar_one_or_none()
    
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chapter {chapter_id} not found"
        )
    
    # Check access
    access_service = get_access_service()
    access_result = access_service.check_chapter_access(current_user, chapter)
    
    if not access_result.has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=access_result.reason
        )
    
    # Get content from R2
    r2_service = get_r2_service()
    try:
        content = r2_service.get_chapter_content(chapter_id)
    except ContentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content for chapter {chapter_id} not found"
        )
    
    return APIResponse(data=ChapterDetail(
        id=chapter.id,
        title=chapter.title,
        difficulty=chapter.difficulty,
        estimated_read_min=chapter.estimated_read_min,
        is_free=chapter.is_free,
        is_locked=False,  # Already passed access check
        sequence_order=chapter.sequence_order,
        prev_chapter_id=chapter.prev_chapter_id,
        next_chapter_id=chapter.next_chapter_id,
        content=content
    ))


@router.get("/{chapter_id}/next", response_model=APIResponse[ChapterMeta | None])
async def get_next_chapter(
    chapter_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get next chapter metadata."""
    result = await db.execute(
        select(Chapter).where(Chapter.id == chapter_id)
    )
    chapter = result.scalar_one_or_none()
    
    if not chapter or not chapter.next_chapter_id:
        return APIResponse(data=None)
    
    # Get next chapter
    next_result = await db.execute(
        select(Chapter).where(Chapter.id == chapter.next_chapter_id)
    )
    next_chapter = next_result.scalar_one_or_none()
    
    if not next_chapter:
        return APIResponse(data=None)
    
    # Check access to next chapter
    access_service = get_access_service()
    access_result = access_service.check_chapter_access(current_user, next_chapter)
    
    if not access_result.has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Next chapter requires premium access"
        )
    
    return APIResponse(data=ChapterMeta(
        id=next_chapter.id,
        title=next_chapter.title,
        difficulty=next_chapter.difficulty,
        estimated_read_min=next_chapter.estimated_read_min,
        is_free=next_chapter.is_free,
        is_locked=False,
        sequence_order=next_chapter.sequence_order,
        prev_chapter_id=next_chapter.prev_chapter_id,
        next_chapter_id=next_chapter.next_chapter_id
    ))


@router.get("/{chapter_id}/prev", response_model=APIResponse[ChapterMeta | None])
async def get_prev_chapter(
    chapter_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get previous chapter metadata."""
    result = await db.execute(
        select(Chapter).where(Chapter.id == chapter_id)
    )
    chapter = result.scalar_one_or_none()
    
    if not chapter or not chapter.prev_chapter_id:
        return APIResponse(data=None)
    
    # Get previous chapter
    prev_result = await db.execute(
        select(Chapter).where(Chapter.id == chapter.prev_chapter_id)
    )
    prev_chapter = prev_result.scalar_one_or_none()
    
    if not prev_chapter:
        return APIResponse(data=None)
    
    return APIResponse(data=ChapterMeta(
        id=prev_chapter.id,
        title=prev_chapter.title,
        difficulty=prev_chapter.difficulty,
        estimated_read_min=prev_chapter.estimated_read_min,
        is_free=prev_chapter.is_free,
        is_locked=False,
        sequence_order=prev_chapter.sequence_order,
        prev_chapter_id=prev_chapter.prev_chapter_id,
        next_chapter_id=prev_chapter.next_chapter_id
    ))
