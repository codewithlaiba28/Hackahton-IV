# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from typing import List, Optional

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.chapter import Chapter
from app.schemas.common import APIResponse
from pydantic import BaseModel

router = APIRouter()


class SearchResult(BaseModel):
    """Search result item."""
    chapter_id: str
    chapter_title: str
    excerpt: str
    relevance_score: float


@router.get("", response_model=APIResponse[List[SearchResult]])
async def search_chapters(
    q: str = Query(..., description="Search query"),
    chapter_id: Optional[str] = Query(None, description="Limit search to specific chapter"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Search course content using PostgreSQL full-text search.

    Returns up to 5 relevant sections.
    Freemium gate enforced - free users don't see gated chapter results.
    """
    # Build search query using PostgreSQL tsvector
    # Use websearch_to_tsquery for natural language search
    search_query = func.websearch_to_tsquery('english', q)
    
    # Build base query
    stmt = select(
        Chapter.id,
        Chapter.title,
        func.ts_rank_cd(Chapter.search_vector, search_query).label('relevance'),
        func.left(Chapter.r2_content_key, 200).label('excerpt')  # Use r2_content_key as placeholder
    ).where(
        Chapter.search_vector.op('@@')(search_query)
    )
    
    # Filter by specific chapter if provided
    if chapter_id:
        stmt = stmt.where(Chapter.id == chapter_id)
    
    # Free users only see free chapters
    if current_user.tier.value == 'free':
        stmt = stmt.where(Chapter.is_free == True)
    
    # Order by relevance and limit results
    stmt = stmt.order_by(text('relevance DESC')).limit(5)
    
    result = await db.execute(stmt)
    rows = result.all()
    
    # Convert to search results
    search_results = [
        SearchResult(
            chapter_id=row.id,
            chapter_title=row.title,
            excerpt=f"Content matches for: {q}",  # Placeholder until we fetch actual content
            relevance_score=float(row.relevance) if row.relevance else 0.0
        )
        for row in rows
    ]
    
    return APIResponse(data=search_results)
