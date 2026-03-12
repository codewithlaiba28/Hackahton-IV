"""
LLM Usage Tracking Model

Tracks every LLM API call for cost management and transparency.
This is the ONLY model that directly relates to Phase 2 hybrid features.
"""

from sqlalchemy import Column, String, Integer, Numeric, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class LLMUsage(Base):
    """
    Tracks LLM API usage for cost control and transparency.
    
    Every LLM call (adaptive path, assessment grading) creates a record here.
    Used for:
    - Monthly cost caps per user
    - Cost transparency dashboard
    - Usage analytics
    - Constitutional compliance (Principle X)
    """
    
    __tablename__ = "llm_usage"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    feature_name = Column(String(50), nullable=False, index=True)  # 'adaptive_path' or 'assessment_grading'
    model = Column(String(100), nullable=False)  # e.g., 'claude-sonnet-4-20250514'
    input_tokens = Column(Integer, nullable=False)
    output_tokens = Column(Integer, nullable=False)
    cost_usd = Column(Numeric(10, 6), nullable=False)  # 6 decimal places for precision
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="llm_usage_records")
    
    def __repr__(self):
        return f"<LLMUsage(user_id={self.user_id}, feature={self.feature_name}, cost=${self.cost_usd})>"
    
    @property
    def total_tokens(self) -> int:
        """Total tokens used in this request"""
        return self.input_tokens + self.output_tokens


# Index for efficient monthly cost queries
Index(
    "ix_llm_usage_user_created",
    LLMUsage.user_id,
    LLMUsage.created_at
)
