# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

from pydantic import BaseModel, Field
from typing import List, Optional


class ChapterMeta(BaseModel):
    """Chapter metadata for list responses."""
    id: str
    title: str
    difficulty: str
    estimated_read_min: int
    is_free: bool
    is_locked: bool
    sequence_order: int
    prev_chapter_id: Optional[str] = None
    next_chapter_id: Optional[str] = None


class ChapterDetail(BaseModel):
    """Full chapter details including content."""
    id: str
    title: str
    difficulty: str
    estimated_read_min: int
    is_free: bool
    is_locked: bool = False
    sequence_order: int
    prev_chapter_id: Optional[str] = None
    next_chapter_id: Optional[str] = None
    content: str  # Raw Markdown from R2


class ChapterListResponse(BaseModel):
    """Response for chapter list endpoint."""
    chapters: List[ChapterMeta]
