---
name: phase-2-hybrid-implementation
description: |
  [What] Complete implementation guide for Phase 2 Hybrid Intelligence features.
  [When] Use when implementing premium LLM-powered features: Adaptive Learning Path and LLM Assessment Grading.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
---

# Phase 2: Hybrid Intelligence Implementation Skill

## Purpose

This skill guides you through implementing **Phase 2 Hybrid Intelligence** features for the Course Companion FTE, adding selective LLM-powered premium features while maintaining Zero-Backend-LLM architecture for core functionality.

## ⚠️ Phase 2 Context

**Current Status:**
- ✅ Phase 1 Complete (Zero-Backend-LLM)
- 🎯 Phase 2 In Progress (Hybrid Intelligence - Premium)
- ⏳ Phase 3 Pending (Web App)

**Phase 2 Goal:** Add 2 premium features that:
1. Use backend LLM calls (Hybrid)
2. Are cost-justified as premium features
3. Are cleanly isolated from Phase 1 logic
4. Provide clear additional educational value

## Required Hybrid Features (Choose 2)

Per Hackahton.md §6.3, implement **exactly 2** hybrid features:

| Feature | Status | Location |
|---------|--------|----------|
| **A. Adaptive Learning Path** | ✅ Skill exists | `skills/adaptive-learning-path/` |
| **B. LLM-Graded Assessments** | ✅ Skill exists | `skills/llm-assessment-grader/` |
| C. Cross-Chapter Synthesis | ⏳ Optional | - |
| D. AI Mentor Agent | ⏳ Optional | - |

**Recommended:** Features A + B (already have skills created)

## Phase 2 Rules (STRICT)

### ✅ Hybrid Intelligence MUST be:

```
✓ Feature-scoped (limited to specific features)
✓ User-initiated (user requests it)
✓ Premium-gated (paid users only)
✓ Isolated (separate API routes)
✓ Cost-tracked (monitor per-user cost)
```

### ❌ You may NOT:

```
✗ Convert entire app to hybrid
✗ Auto-trigger hybrid features
✗ Make hybrid required for core UX
✗ Hide hybrid costs from analysis
```

## Implementation Workflow

### Step 1: Verify Phase 1 Foundation

Before Phase 2, ensure Phase 1 is solid:

```bash
# 1. Verify Zero-Backend-LLM compliance
cd backend
grep -r "openai\|anthropic\|llm" app/ --include="*.py"
# Should return 0 results for Phase 1 routes

# 2. Verify all 6 features work
python -m pytest tests/ -v

# 3. Check backend runs
uv run uvicorn app.main:app --reload
# Test: http://127.0.0.1:8000/docs
```

**Acceptance Criteria:**
- [ ] Zero LLM calls in Phase 1 routes
- [ ] All tests passing
- [ ] Backend serves content correctly
- [ ] Progress tracking works
- [ ] Freemium gate functional

### Step 2: Set Up LLM Infrastructure

```bash
# 1. Install LLM dependencies
cd backend
uv add anthropic openai

# 2. Add environment variables
# Edit .env or .env.example:
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
LLM_MODEL_CLAUDE=claude-sonnet-4-20250514
LLM_MODEL_GPT=gpt-4o

# 3. Create LLM config
# File: app/config/llm_config.py
```

**Create LLM Configuration:**

```python
# app/config/llm_config.py
from pydantic_settings import BaseSettings
from typing import Optional

class LLMConfig(BaseSettings):
    """LLM configuration for Phase 2 Hybrid features"""
    
    # Anthropic (Claude)
    anthropic_api_key: str = ""
    claude_model: str = "claude-sonnet-4-20250514"
    claude_max_tokens: int = 2000
    
    # OpenAI (GPT)
    openai_api_key: str = ""
    gpt_model: str = "gpt-4o"
    gpt_max_tokens: int = 2000
    
    # Cost tracking
    cost_per_1k_input_claude: float = 0.003
    cost_per_1k_output_claude: float = 0.015
    cost_per_1k_input_gpt: float = 0.005
    cost_per_1k_output_gpt: float = 0.015
    
    # Budget limits
    monthly_budget_per_pro_user: float = 5.0
    alert_threshold_percent: float = 80.0
    
    class Config:
        env_file = ".env"
        extra = "ignore"

llm_config = LLMConfig()
```

### Step 3: Create Cost Tracking Service

```python
# app/services/cost_tracker.py
from datetime import datetime, timedelta
from typing import Optional
import asyncpg

class CostTracker:
    """Track LLM costs per user for Phase 2 features"""
    
    def __init__(self, db_pool):
        self.db_pool = db_pool
    
    async def record_usage(
        self,
        user_id: int,
        feature: str,
        input_tokens: int,
        output_tokens: int,
        model: str,
        cost: float
    ):
        """Record LLM usage for a user"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO llm_usage_logs
                (user_id, feature, input_tokens, output_tokens, model, cost, created_at)
                VALUES ($1, $2, $3, $4, $5, $6, NOW())
            """, user_id, feature, input_tokens, output_tokens, model, cost)
    
    async def get_monthly_cost(self, user_id: int) -> dict:
        """Get user's monthly LLM costs"""
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT 
                    SUM(cost) as total_cost,
                    COUNT(*) as request_count
                FROM llm_usage_logs
                WHERE user_id = $1
                AND created_at >= DATE_TRUNC('month', CURRENT_DATE)
            """, user_id)
            
            return {
                "total_cost": float(row["total_cost"] or 0),
                "request_count": int(row["request_count"] or 0),
                "budget_remaining": 5.0 - float(row["total_cost"] or 0),
                "budget_limit": 5.0
            }
    
    async def check_access(self, user_id: int) -> dict:
        """Check if user can use hybrid features"""
        monthly_cost = await self.get_monthly_cost(user_id)
        
        return {
            "can_use": monthly_cost["budget_remaining"] > 0,
            "budget_used_percent": (monthly_cost["total_cost"] / 5.0) * 100,
            "alert": monthly_cost["budget_used_percent"] >= 80.0,
            "details": monthly_cost
        }
```

### Step 4: Create Database Migration

```sql
-- alembic/versions/002_add_llm_tracking.sql
-- Add LLM usage tracking tables

CREATE TABLE IF NOT EXISTS llm_usage_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    feature VARCHAR(50) NOT NULL, -- 'adaptive_path' or 'llm_grading'
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL,
    model VARCHAR(50) NOT NULL,
    cost DECIMAL(10, 4) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_llm_usage_user_month 
ON llm_usage_logs(user_id, DATE_TRUNC('month', created_at));

-- Add Pro tier to subscription_tiers if not exists
INSERT INTO subscription_tiers (name, price, features)
VALUES ('Pro', 19.99, 'Everything in Premium + Adaptive Learning + LLM Assessments')
ON CONFLICT (name) DO NOTHING;

-- Add llm_usage column to users for quick lookup
ALTER TABLE users 
ADD COLUMN monthly_llm_budget DECIMAL(10, 2) DEFAULT 5.00;
```

### Step 5: Implement Adaptive Learning Path API

```python
# app/routers/adaptive_learning.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.adaptive import LearningPathRecommendation, StudentAnalysis
from app.services.llm_service import LLMService
from app.services.cost_tracker import CostTracker
from app.auth import get_current_user, User

router = APIRouter(prefix="/api/v2", tags=["adaptive-learning"])

@router.post("/learning-path/generate", 
             response_model=LearningPathRecommendation,
             summary="Generate Personalized Learning Path (Pro Only)")
async def generate_learning_path(
    current_user: User = Depends(get_current_user),
    llm_service: LLMService = Depends(),
    cost_tracker: CostTracker = Depends()
):
    """
    **Pro Tier Feature**
    
    Generate a personalized learning path using AI analysis of:
    - Quiz performance
    - Learning patterns
    - Knowledge gaps
    - Optimal review timing
    
    **Cost:** Included in Pro tier ($5 monthly LLM budget)
    """
    # 1. Verify Pro access
    if current_user.tier not in ["Pro"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This feature requires Pro tier. Upgrade to access."
        )
    
    # 2. Check cost budget
    access = await cost_tracker.check_access(current_user.id)
    if not access["can_use"]:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Monthly LLM budget exceeded. Resets on next month."
        )
    
    if access["alert"]:
        # Warn user but continue
        pass
    
    # 3. Gather student data
    student_data = await gather_student_data(current_user.id)
    
    # 4. Call LLM for analysis
    try:
        analysis = await llm_service.analyze_learning_patterns(student_data)
        recommendations = await llm_service.generate_learning_path(analysis)
        
        # 5. Record cost
        await cost_tracker.record_usage(
            user_id=current_user.id,
            feature="adaptive_path",
            input_tokens=analysis.input_tokens,
            output_tokens=analysis.output_tokens,
            model="claude-sonnet-4",
            cost=analysis.cost
        )
        
        return recommendations
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"LLM service unavailable: {str(e)}"
        )

async def gather_student_data(user_id: int) -> dict:
    """Gather comprehensive student data for analysis"""
    # Implementation: Query quiz scores, progress, engagement
    pass
```

### Step 6: Implement LLM Assessment Grading API

```python
# app/routers/llm_assessment.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.assessment import AssessmentSubmission, GradingResult
from app.services.llm_service import LLMService
from app.services.cost_tracker import CostTracker
from app.auth import get_current_user, User

router = APIRouter(prefix="/api/v2", tags=["llm-assessment"])

@router.post("/assessment/grade",
             response_model=GradingResult,
             summary="Grade Written Assessment with LLM (Pro Only)")
async def grade_assessment(
    submission: AssessmentSubmission,
    current_user: User = Depends(get_current_user),
    llm_service: LLMService = Depends(),
    cost_tracker: CostTracker = Depends()
):
    """
    **Pro Tier Feature**
    
    Grade free-form written assessments using AI analysis.
    Provides detailed feedback beyond rule-based grading.
    
    **Cost:** Included in Pro tier (50 assessments/month)
    """
    # 1. Verify Pro access
    if current_user.tier not in ["Pro"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="LLM-graded assessments require Pro tier."
        )
    
    # 2. Check assessment count
    monthly_count = await cost_tracker.get_assessment_count(current_user.id)
    if monthly_count >= 50:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Monthly assessment limit reached (50)."
        )
    
    # 3. Verify question type requires LLM
    if submission.question_type in ["multiple_choice", "true_false", "fill_blank"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use rule-based grading for this question type."
        )
    
    # 4. Call LLM for grading
    try:
        grading_result = await llm_service.grade_assessment(
            question=submission.question,
            student_answer=submission.answer,
            rubric=submission.rubric
        )
        
        # 5. Record usage
        await cost_tracker.record_usage(
            user_id=current_user.id,
            feature="llm_grading",
            input_tokens=grading_result.input_tokens,
            output_tokens=grading_result.output_tokens,
            model="claude-sonnet-4",
            cost=grading_result.cost
        )
        
        return grading_result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Grading service unavailable: {str(e)}"
        )
```

### Step 7: Create LLM Service

```python
# app/services/llm_service.py
from anthropic import AsyncAnthropic
from typing import Dict, List, Optional
import json

class LLMService:
    """LLM service for Phase 2 Hybrid features"""
    
    def __init__(self, anthropic_client: AsyncAnthropic):
        self.client = anthropic_client
    
    async def analyze_learning_patterns(self, student_data: dict) -> dict:
        """Analyze student learning patterns using LLM"""
        
        prompt = self._build_analysis_prompt(student_data)
        
        response = await self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse response
        analysis = json.loads(response.content[0].text)
        
        return {
            "strengths": analysis["strengths"],
            "weaknesses": analysis["weaknesses"],
            "patterns": analysis["patterns"],
            "recommendations": analysis["recommendations"],
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "cost": self._calculate_cost(
                response.usage.input_tokens,
                response.usage.output_tokens
            )
        }
    
    async def generate_learning_path(self, analysis: dict) -> dict:
        """Generate personalized learning path from analysis"""
        
        prompt = self._build_path_prompt(analysis)
        
        response = await self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        path = json.loads(response.content[0].text)
        
        return {
            "daily_plan": path["daily_plan"],
            "weekly_goals": path["weekly_goals"],
            "review_sessions": path["review_sessions"],
            "milestones": path["milestones"],
            "rationale": path["rationale"]
        }
    
    async def grade_assessment(self, question: str, answer: str, rubric: dict) -> dict:
        """Grade written assessment using LLM"""
        
        prompt = self._build_grading_prompt(question, answer, rubric)
        
        response = await self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        grading = json.loads(response.content[0].text)
        
        return {
            "score": grading["score"],
            "max_score": grading["max_score"],
            "percentage": grading["percentage"],
            "strengths": grading["strengths"],
            "weaknesses": grading["weaknesses"],
            "feedback": grading["feedback"],
            "model_answer_points": grading["model_answer"],
            "next_steps": grading["next_steps"],
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "cost": self._calculate_cost(
                response.usage.input_tokens,
                response.usage.output_tokens
            )
        }
    
    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate LLM cost"""
        input_cost = (input_tokens / 1000) * 0.003
        output_cost = (output_tokens / 1000) * 0.015
        return round(input_cost + output_cost, 4)
```

### Step 8: Update Schemas

```python
# app/schemas/adaptive.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import date

class StudentAnalysis(BaseModel):
    """Analysis of student learning patterns"""
    strengths: List[str]
    weaknesses: List[str]
    patterns: Dict[str, str]
    knowledge_gaps: List[str]
    learning_velocity: str  # "fast", "average", "slow"

class DailyPlan(BaseModel):
    """Daily learning plan"""
    day: str
    activities: List[str]
    estimated_time_minutes: int
    focus_area: str

class LearningPathRecommendation(BaseModel):
    """Personalized learning path recommendation"""
    generated_at: date
    student_summary: StudentAnalysis
    daily_plan: List[DailyPlan]
    weekly_goals: List[str]
    review_sessions: List[str]
    milestones: List[Dict]
    rationale: str
    expected_completion: date

# app/schemas/assessment.py
class AssessmentSubmission(BaseModel):
    """Written assessment submission"""
    question_id: int
    question: str
    question_type: str  # "essay", "explanation", "analysis"
    answer: str
    rubric: Dict

class GradingResult(BaseModel):
    """LLM grading result"""
    score: float
    max_score: float
    percentage: float
    strengths: List[str]
    weaknesses: List[str]
    feedback: str
    model_answer_points: List[str]
    next_steps: List[str]
```

### Step 9: Update Main App

```python
# app/main.py
from fastapi import FastAPI
from app.routers import adaptive_learning, llm_assessment

app = FastAPI(title="Course Companion FTE API")

# Phase 1 Routes (Zero-Backend-LLM)
app.include_router(chapters.router)
app.include_router(quizzes.router)
app.include_router(progress.router)

# Phase 2 Routes (Hybrid Intelligence - Premium)
app.include_router(adaptive_learning.router)
app.include_router(llm_assessment.router)
```

### Step 10: Create Cost Analysis Document

```markdown
# Phase 2 Cost Analysis

## Hybrid Feature Costs

### Adaptive Learning Path

| Component | Tokens | Cost |
|-----------|--------|------|
| Analysis | ~2,000 | $0.018 |
| Path Generation | ~2,500 | $0.023 |
| **Total per request** | **~4,500** | **$0.041** |

**Monthly Budget (Pro tier):** $5.00
**Included requests:** ~120 per month
**Average usage:** 2-4 per student per month

### LLM Assessment Grading

| Component | Tokens | Cost |
|-----------|--------|------|
| Short answer | ~1,000 | $0.009 |
| Medium answer | ~2,000 | $0.018 |
| Long essay | ~3,500 | $0.032 |
| **Average** | **~2,000** | **$0.018** |

**Monthly Budget (Pro tier):** $5.00
**Included assessments:** 50 per month
**Average usage:** 5-10 per student per month

## Monetization

### Pro Tier Pricing

| Component | Cost |
|-----------|------|
| Infrastructure | $0.50/user/month |
| LLM Budget | $5.00/user/month |
| Support & Ops | $2.00/user/month |
| **Total Cost** | **$7.50/user/month** |
| **Price** | **$19.99/month** |
| **Margin** | **62%** |

### Cost Controls

1. **Monthly Budget:** $5 LLM credits per Pro user
2. **Alerts:** Warning at 80% usage
3. **Hard Limits:** Stop at 100% (offer top-up)
4. **Tracking:** Per-request cost logging
5. **Optimization:** Cache common analyses

## Break-Even Analysis

**Assumptions:**
- 100 Pro users
- 60% average LLM budget usage
- Infrastructure: $50/month total

**Monthly Costs:**
- LLM: 100 × $3 = $300
- Infrastructure: $50
- **Total:** $350

**Monthly Revenue:**
- 100 × $19.99 = $1,999

**Profit:** $1,649/month (82% margin)

## Cost Optimization Strategies

1. Use Claude Sonnet (cost-effective)
2. Cache analysis results (7-day TTL)
3. Batch similar requests
4. Optimize prompts (reduce tokens)
5. Monitor and alert on anomalies
```

### Step 11: Update Architecture Diagram

Add Phase 2 hybrid layer to architecture:

```
User → ChatGPT App → Backend
                      ├─ Deterministic APIs (Phase 1)
                      └─ Hybrid Intelligence APIs (Phase 2, gated)
                          ├─ Adaptive Learning Path (Pro)
                          └─ LLM Assessment Grading (Pro)
```

## Testing Phase 2

### Test Adaptive Learning Path

```bash
# 1. Test Pro user can access
curl -X POST http://localhost:8000/api/v2/learning-path/generate \
  -H "Authorization: Bearer PRO_USER_TOKEN"

# Expected: Learning path recommendation

# 2. Test Free user cannot access
curl -X POST http://localhost:8000/api/v2/learning-path/generate \
  -H "Authorization: Bearer FREE_USER_TOKEN"

# Expected: 403 Forbidden

# 3. Test budget exceeded
# Use up budget, then try again
# Expected: 429 Too Many Requests
```

### Test LLM Assessment Grading

```bash
# 1. Test grading written answer
curl -X POST http://localhost:8000/api/v2/assessment/grade \
  -H "Authorization: Bearer PRO_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain how neural networks learn",
    "question_type": "explanation",
    "answer": "Neural networks learn through backpropagation...",
    "rubric": {...}
  }'

# Expected: Grading result with feedback

# 2. Test rule-based question rejected
curl -X POST http://localhost:8000/api/v2/assessment/grade \
  -H "Authorization: Bearer PRO_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is AI?",
    "question_type": "multiple_choice",
    "answer": "A"
  }'

# Expected: 400 Bad Request
```

## Phase 2 Completion Checklist

### Architecture Correctness (10 points)

- [ ] Phase 1 routes remain Zero-Backend-LLM
- [ ] Phase 2 routes clearly separated (/api/v2/)
- [ ] LLM calls only in Phase 2 routes
- [ ] Cost tracking implemented
- [ ] Premium gating functional

### Hybrid Feature Value (5 points)

- [ ] Adaptive Learning Path implemented
- [ ] LLM Assessment Grading implemented
- [ ] Clear value over free features
- [ ] User-initiated (not auto-triggered)
- [ ] Educational justification documented

### Cost Justification (5 points)

- [ ] Cost analysis document created
- [ ] Per-request costs tracked
- [ ] Monthly budget enforced
- [ ] Pricing model sustainable
- [ ] Margin analysis included

### Architecture Separation (5 points)

- [ ] Phase 1 and Phase 2 code separated
- [ ] Different API prefixes (/api/v1 vs /api/v2)
- [ ] LLM service isolated
- [ ] Cost tracker service reusable
- [ ] Clean dependency injection

### Premium Gating (5 points)

- [ ] Pro tier verification works
- [ ] Free users get 403 errors
- [ ] Upgrade prompts shown
- [ ] Budget limits enforced
- [ ] Usage alerts at 80%

**Total Phase 2 Points: 25/25**

## Common Issues & Solutions

### Issue: LLM Costs Too High

**Solution:**
```python
# 1. Reduce token usage
max_tokens=1500  # Instead of 2000

# 2. Use cheaper model
model="claude-haiku-3-5"  # Instead of claude-sonnet

# 3. Cache results
@cache(ttl="7 days")
async def get_learning_path(user_id):
    ...

# 4. Batch requests
async def batch_analyze(student_ids):
    ...
```

### Issue: Phase 1 Contaminated with LLM Calls

**Solution:**
```python
# WRONG - Don't do this in Phase 1 routes
from app.services.llm_service import LLMService  # ❌

# CORRECT - Keep Phase 1 pure
# No LLM imports in Phase 1 routers ✅
```

### Issue: Budget Not Tracked

**Solution:**
```python
# Always record usage AFTER successful LLM call
try:
    result = await llm_service.analyze(...)
    await cost_tracker.record_usage(
        user_id=user.id,
        feature="adaptive_path",
        cost=result.cost
    )
except Exception:
    # Don't record if failed
    raise
```

## Integration with Existing Skills

| Skill | Integration Point |
|-------|-------------------|
| **adaptive-learning-path** | Uses Phase 2 API directly |
| **llm-assessment-grader** | Uses Phase 2 API directly |
| **content-delivery** | Hand-off after path generated |
| **quiz-master** | Hand-off for practice quizzes |
| **progress-motivator** | Celebrates path milestones |
| **socratic-tutor** | Help when struggling with path |

## Next Steps After Phase 2

1. ✅ Complete Phase 2 implementation
2. ⏳ Start Phase 3 (Web App)
3. ⏳ Record demo video
4. ⏳ Submit to hackathon

## References

- `skills/adaptive-learning-path/SKILL.md` - Detailed adaptive learning logic
- `skills/llm-assessment-grader/SKILL.md` - Detailed grading logic
- `Hackahton.md §6` - Phase 2 requirements
- `docs/cost-analysis.md` - Phase 1 cost analysis
- `specs/001-complete-phase-1/` - Phase 1 completion docs
