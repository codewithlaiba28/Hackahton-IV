# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    """User information response (NEVER includes api_key)."""
    id: str
    email: str
    tier: str  # 'free', 'premium', or 'pro'


class AccessCheckResponse(BaseModel):
    """Access check response."""
    has_access: bool
    reason: str
    upgrade_required: bool
