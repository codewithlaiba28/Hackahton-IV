# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, List
from datetime import datetime, UTC

T = TypeVar('T')


class MetaInfo(BaseModel):
    """Metadata for API responses."""
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    request_id: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response schema."""
    message: str
    detail: Optional[str] = None
    code: Optional[str] = None


class APIResponse(BaseModel, Generic[T]):
    """Standard API response envelope.
    
    All endpoints MUST use this envelope for consistency.
    
    Example:
        {
            "data": { ... },
            "error": null,
            "meta": {
                "timestamp": "2026-03-10T10:00:00Z",
                "request_id": "req_abc123"
            }
        }
    """
    data: Optional[T] = None
    error: Optional[ErrorResponse] = None
    meta: MetaInfo = Field(default_factory=MetaInfo)


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response for list endpoints."""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
