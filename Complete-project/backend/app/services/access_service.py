# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

from dataclasses import dataclass
from typing import Optional

from app.models.user import User
from app.models.chapter import Chapter
from app.config import get_settings

settings = get_settings()


@dataclass
class AccessResult:
    """Result of access check."""
    has_access: bool
    reason: str
    upgrade_required: bool


class AccessService:
    """Service for enforcing freemium access control.
    
    Access control happens at the SERVICE layer, not just router,
    to ensure it applies even if called from other services.
    """
    
    def check_chapter_access(self, user: User, chapter: Chapter) -> AccessResult:
        """Check if user can access a chapter.
        
        Args:
            user: Authenticated user
            chapter: Chapter to check access for
            
        Returns:
            AccessResult with access decision
        """
        # Premium/Pro users can access everything
        if str(user.tier) in ["premium", "pro"]:
            return AccessResult(
                has_access=True,
                reason="Premium user",
                upgrade_required=False
            )
        
        # Free users can only access free chapters (first 3)
        if chapter.is_free:
            return AccessResult(
                has_access=True,
                reason="Free chapter",
                upgrade_required=False
            )
        
        # Free user trying to access premium chapter
        return AccessResult(
            has_access=False,
            reason=f"Chapter {chapter.id} requires premium access",
            upgrade_required=True
        )
    
    def is_free_tier(self, user: User) -> bool:
        """Check if user is on free tier."""
        return str(user.tier) == "free"


# Singleton instance
_access_service = AccessService()


def get_access_service() -> AccessService:
    """Get access service instance."""
    return _access_service
