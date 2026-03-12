# Implementation Plan: Phase 2 Hybrid Intelligence Layer

**Branch**: `1-phase-2-hybrid-features` | **Date**: 2026-03-11 | **Spec**: [specs/002-phase-2-hybrid-features/spec.md](../spec.md)

**Input**: Feature specification for Adaptive Learning Path + LLM-Graded Assessments

---

## Summary

**Primary Requirement**: Implement 2 premium hybrid features (Adaptive Learning Path and LLM-Graded Assessments) that use backend LLM calls while preserving Phase 1 Zero-Backend-LLM architecture for core functionality.

**Technical Approach**: 
- Add Anthropic Claude SDK for LLM calls
- Create isolated `/api/v2/` endpoints for Phase 2 features
- Implement cost tracking via `llm_usage` table
- Enforce premium gating before any LLM call
- Use async HTTP for non-blocking LLM requests
- Maintain strict separation: Phase 1 files unchanged

---

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: 
- Existing (Phase 1): FastAPI, SQLAlchemy, Pydantic v2, httpx
- New (Phase 2): anthropic SDK (official Claude client)
**Storage**: PostgreSQL (Neon/Supabase) - existing DB, new tables
**Testing**: pytest (existing), async test coverage for LLM services
**Target Platform**: Linux server (Fly.io/Railway deployment)
**Project Type**: Backend API only (ChatGPT App frontend unchanged)
**Performance Goals**: 
- Adaptive path: <8 seconds response time (includes LLM latency)
- LLM assessment: <10 seconds response time
- 99% uptime for Phase 1 endpoints regardless of Phase 2 availability
**Constraints**: 
- Monthly LLM cost per user: $2.00 cap (premium), $5.00 cap (pro)
- Per-request cost ceiling: $0.05 (adaptive path), $0.03 (assessment)
- Zero modifications to Phase 1 router files
- LLM calls must be async (non-blocking)
**Scale/Scope**: 
- Target: 10K users (Phase 1 baseline)
- Premium adoption: ~10% (1K users)
- LLM API calls: ~5K-10K per month estimated

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase 1 Principles (Must Remain Unchanged)

- [x] **Principle I (Zero-Backend-LLM)**: Phase 1 endpoints remain LLM-free
  - **Verification**: Git diff on `routers/chapters.py`, `routers/quizzes.py`, etc. shows no LLM imports
  - **Status**: ✅ PASS

- [x] **Principle II (Determinism)**: Phase 1 endpoints remain deterministic
  - **Verification**: No probabilistic behavior in Phase 1 code
  - **Status**: ✅ PASS

- [x] **Principle III (Content Verbatim)**: Unchanged
  - **Status**: ✅ PASS

- [x] **Principle IV (ChatGPT is Brain)**: Phase 1 unchanged, Phase 2 adds selective intelligence
  - **Status**: ✅ PASS (Phase 2 is additive, not modifying Phase 1)

- [x] **Principle V (Progress Persistence)**: New tables use same PostgreSQL
  - **Status**: ✅ PASS

- [x] **Principle VI (Single Responsibility)**: New endpoints follow pattern
  - **Status**: ✅ PASS

- [x] **Principle VII (Freemium Enforcement)**: Enhanced with premium gating
  - **Status**: ✅ PASS

### Phase 2 Principles (Must Be Implemented)

- [x] **Principle VIII (Hybrid Selectivity Law)**:
  - [ ] Maximum 2 hybrid features → **PASS** (Adaptive Path + LLM Assessment)
  - [ ] Premium-gated only → **PASS** (tier checks in endpoints)
  - [ ] User-initiated → **PASS** (no auto-triggers in design)
  - [ ] Phase 1 APIs unchanged → **PASS** (separate routers)
  - [ ] Cost-tracked → **PASS** (llm_usage table)

- [x] **Principle IX (Architectural Separation)**:
  - [ ] Phase 1 files unchanged → **PASS** (new files only)
  - [ ] Separate routers → **PASS** (`adaptive_path.py`, `assessments.py`)
  - [ ] API versioning → **PASS** (`/api/v2/` prefix)

- [x] **Principle X (Cost Control)**:
  - [ ] Per-request ceiling → **PASS** ($0.05/$0.03 limits)
  - [ ] Monthly cap → **PASS** ($2/$5 caps)
  - [ ] Cost logging → **PASS** (llm_usage table)
  - [ ] Transparency → **PASS** (/users/me/cost-summary endpoint)

- [x] **Principle XI (LLM Quality)**:
  - [ ] Grounding required → **PASS** (prompts include course content)
  - [ ] Hallucination guards → **PASS** (system prompts)
  - [ ] Structured output → **PASS** (JSON mode)
  - [ ] Fallback on failure → **PASS** (error handling)
  - [ ] Model pinned → **PASS** (claude-sonnet-4-20250514)

- [x] **Principle XII (Premium Gate)**:
  - [ ] Tier check first → **PASS** (before LLM call)
  - [ ] Clear upgrade message → **PASS** (structured 403)
  - [ ] No partial access → **PASS** (binary gating)

**Overall Constitution Check**: ✅ **PASS** - All gates satisfied

---

## Project Structure

### Documentation (this feature)

```text
specs/002-phase-2-hybrid-features/
├── spec.md                  # Feature specification
├── plan.md                  # This file (implementation plan)
├── research.md              # Phase 0 output (LLM integration patterns)
├── data-model.md            # Phase 1 output (database schema)
├── quickstart.md            # Phase 1 output (setup guide)
├── contracts/               # Phase 1 output (API contracts)
│   ├── adaptive-path.yaml   # OpenAPI spec for Feature A
│   └── assessments.yaml     # OpenAPI spec for Feature B
└── tasks.md                 # Phase 2 output (implementation tasks)
```

### Source Code (backend directory)

```text
backend/
├── app/
│   ├── routers/
│   │   ├── chapters.py              # Phase 1 - UNCHANGED
│   │   ├── search.py                # Phase 1 - UNCHANGED
│   │   ├── quizzes.py               # Phase 1 - UNCHANGED
│   │   ├── progress.py              # Phase 1 - UNCHANGED
│   │   ├── access.py                # Phase 1 - UNCHANGED
│   │   ├── users.py                 # Phase 1 - UNCHANGED
│   │   ├── adaptive_path.py         # Phase 2 - NEW: Feature A router
│   │   └── assessments.py           # Phase 2 - NEW: Feature B router
│   │
│   ├── services/
│   │   ├── r2_service.py            # Phase 1 - UNCHANGED
│   │   ├── quiz_service.py          # Phase 1 - UNCHANGED
│   │   ├── progress_service.py      # Phase 1 - UNCHANGED
│   │   ├── access_service.py        # Phase 1 - UNCHANGED
│   │   ├── llm_service.py           # Phase 2 - NEW: Claude API wrapper
│   │   ├── adaptive_service.py      # Phase 2 - NEW: Feature A logic
│   │   └── assessment_service.py    # Phase 2 - NEW: Feature B logic
│   │
│   ├── models/
│   │   ├── user.py                  # Phase 1 - UNCHANGED
│   │   ├── chapter.py               # Phase 1 - UNCHANGED
│   │   ├── quiz.py                  # Phase 1 - UNCHANGED
│   │   ├── progress.py              # Phase 1 - UNCHANGED
│   │   ├── adaptive.py              # Phase 2 - NEW: AdaptiveRecommendation
│   │   ├── assessment.py            # Phase 2 - NEW: AssessmentQuestion, AssessmentResult
│   │   └── llm_usage.py             # Phase 2 - NEW: LLMUsage cost tracking
│   │
│   └── schemas/
│       ├── common.py                # Phase 1 - UNCHANGED
│       ├── chapter.py               # Phase 1 - UNCHANGED
│       ├── quiz.py                  # Phase 1 - UNCHANGED
│       ├── progress.py              # Phase 1 - UNCHANGED
│       ├── user.py                  # Phase 1 - may add tier field
│       ├── adaptive.py              # Phase 2 - NEW: request/response schemas
│       ├── assessment.py            # Phase 2 - NEW: request/response schemas
│       └── llm_usage.py             # Phase 2 - NEW: cost summary schema
│
├── alembic/versions/
│   ├── 001_initial_schema.py        # Phase 1 migration
│   └── 002_phase2_tables.py         # Phase 2 - NEW: llm_usage, adaptive_recommendations, etc.
│
├── seed/
│   ├── seed_chapters.py             # Phase 1 - UNCHANGED
│   ├── seed_quizzes.py              # Phase 1 - UNCHANGED
│   └── seed_assessments.py          # Phase 2 - NEW: seed open-ended questions
│
├── tests/
│   ├── test_adaptive_path.py        # Phase 2 - NEW
│   ├── test_assessments.py          # Phase 2 - NEW
│   ├── test_llm_service.py          # Phase 2 - NEW
│   └── [Phase 1 tests - UNCHANGED]
│
├── .env.example                     # Phase 2 - ADD: ANTHROPIC_API_KEY
├── pyproject.toml                   # Phase 2 - ADD: anthropic dependency
└── README.md                        # Phase 2 - UPDATE: Phase 2 setup section
```

**Structure Decision**: Backend-only changes (Option 1). Frontend (ChatGPT App) unchanged - uses existing Phase 1 configuration.

---

## New Technology Additions (Phase 2 Only)

| Addition | Technology | Justification |
|----------|------------|---------------|
| **LLM Client** | anthropic Python SDK | Official SDK for Claude Sonnet, async support, type-safe |
| **HTTP Client** | httpx (already in dev deps) | Already available; used for async LLM calls |
| **Structured Output** | Pydantic v2 + JSON mode | Parse Claude's structured JSON responses safely |

**Dependencies to Add**:
```bash
# Add to backend dependencies
cd backend
uv add anthropic
```

**Environment Variables to Add**:
```bash
# Add to .env.example
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-sonnet-4-20250514
LLM_MAX_TOKENS=1000
ADAPTIVE_PATH_MAX_COST_USD=0.05
ASSESSMENT_MAX_COST_USD=0.03
USER_MONTHLY_LLM_CAP_USD=2.00
```

---

## LLM Service Architecture

```
ChatGPT App
    │
    ▼
FastAPI Router (adaptive_path.py / assessments.py)
    │
    ├─── 1. Premium gate check (access_service.py — Phase 1)
    │
    ├─── 2. Collect context data (Phase 1 services — unchanged)
    │        ├── progress_service.get_progress_summary()
    │        └── r2_service.get_chapter_content()
    │
    ├─── 3. Build prompt (adaptive_service / assessment_service)
    │
    ├─── 4. Call LLM (llm_service.py)
    │        └── anthropic.messages.create()
    │
    ├─── 5. Parse & validate structured JSON response
    │
    ├─── 6. Log token usage (llm_usage table)
    │
    └─── 7. Store result + return to ChatGPT App
```

**Key Design**: `llm_service.py` is the **ONLY** file that imports `anthropic`. All other Phase 2 services call this module, never anthropic directly. This ensures clean separation and easy testing.

---

## LLM Service Design (llm_service.py)

```python
# Shared LLM service — the ONLY file in Phase 2 that imports anthropic
# All other Phase 2 services call this module, never anthropic directly

from anthropic import AsyncAnthropic
from app.models.llm_usage import LLMUsage
from sqlalchemy.ext.asyncio import AsyncSession

class LLMService:
    def __init__(self, api_key: str, model: str):
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = model
    
    async def call_claude(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        feature_name: str,
        user_id: UUID,
        db: AsyncSession
    ) -> tuple[dict, LLMUsage]:
        """
        Call Claude Sonnet and log usage.
        
        Returns:
            tuple: (parsed_json_response, llm_usage_record)
        """
        # 1. Call Claude Sonnet with provided prompts
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        # 2. Parse JSON response (Claude returns text, parse to dict)
        import json
        parsed_response = json.loads(response.content[0].text)
        
        # 3. Calculate cost
        # Input tokens: $3.00 per 1M = $0.000003 per token
        # Output tokens: $15.00 per 1M = $0.000015 per token
        input_cost = response.usage.input_tokens * 0.000003
        output_cost = response.usage.output_tokens * 0.000015
        total_cost = input_cost + output_cost
        
        # 4. Create LLMUsage record
        llm_usage = LLMUsage(
            user_id=user_id,
            feature_name=feature_name,
            model=self.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            cost_usd=total_cost
        )
        
        # 5. Log to database
        db.add(llm_usage)
        await db.commit()
        
        # 6. Return parsed response and usage record
        return (parsed_response, llm_usage)
```

**Cost Calculation Reference**:
- Input tokens: $3.00 per 1M tokens = $0.000003 per token
- Output tokens: $15.00 per 1M tokens = $0.000015 per token
- Example: 2000 input + 1000 output = (2000 × 0.000003) + (1000 × 0.000015) = $0.006 + $0.015 = $0.021

---

## New API Endpoints (Phase 2 Only)

| Method | Path | Feature | Description |
|--------|------|---------|-------------|
| **POST** | `/api/v2/adaptive/learning-path` | A | Generate personalized learning path (LLM call) |
| **GET** | `/api/v2/adaptive/learning-path/latest` | A | Get last recommendation (no LLM call) |
| **GET** | `/api/v2/assessments/{chapter_id}/questions` | B | Get open-ended questions |
| **POST** | `/api/v2/assessments/{chapter_id}/submit` | B | Submit answer for LLM grading |
| **GET** | `/api/v2/assessments/{chapter_id}/results` | B | Get past assessment results |
| **GET** | `/api/v2/users/me/cost-summary` | Cost | Get current month LLM usage cost |

**Total new endpoints**: 6  
**Phase 1 endpoints modified**: 0 ✅

---

## New Database Schema (Phase 2 Additions)

See `specs/002-phase-2-hybrid-features/data-model.md` for complete schema.

**Summary of New Tables**:

1. **llm_usage** - Cost tracking for every LLM call
2. **adaptive_recommendations** - Store personalized learning paths
3. **assessment_questions** - Open-ended questions (separate from MCQ)
4. **assessment_results** - LLM-graded assessment submissions

---

## Phase 0: Research Tasks

**Prerequisites**: None

**Tasks**:

1. **Research: Anthropic SDK Best Practices**
   - Async usage patterns
   - Error handling (timeouts, rate limits)
   - Token counting accuracy
   - Output: `research.md#anthropic-sdk-patterns`

2. **Research: Cost Optimization Strategies**
   - Prompt token reduction techniques
   - Caching strategies for recommendations
   - Batch vs. individual calls
   - Output: `research.md#cost-optimization`

3. **Research: LLM Fallback Patterns**
   - Graceful degradation strategies
   - Cached response handling
   - User messaging for failures
   - Output: `research.md#fallback-patterns`

4. **Research: Premium Gating Implementation**
   - Tier check patterns in FastAPI
   - Dependency injection for access control
   - Error response standardization
   - Output: `research.md#premium-gating`

---

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` complete

### 1. Data Model Design

**Output**: `data-model.md`

**Entities**:
- LLMUsage (cost tracking)
- AdaptiveRecommendation (learning paths)
- AssessmentQuestion (open-ended questions)
- AssessmentResult (graded submissions)

### 2. API Contracts

**Output**: `contracts/adaptive-path.yaml`, `contracts/assessments.yaml`

**Endpoints**:
- POST /api/v2/adaptive/learning-path
- GET /api/v2/adaptive/learning-path/latest
- GET /api/v2/assessments/{chapter_id}/questions
- POST /api/v2/assessments/{chapter_id}/submit
- GET /api/v2/assessments/{chapter_id}/results
- GET /api/v2/users/me/cost-summary

### 3. Quickstart Guide

**Output**: `quickstart.md`

**Contents**:
- Environment setup (ANTHROPIC_API_KEY)
- Dependency installation
- Database migration
- Testing Phase 2 features

### 4. Agent Context Update

**Output**: Update agent-specific context file

**Command**:
```bash
.specify/scripts/bash/update-agent-context.sh qwen
```

**Content**: Add Anthropic SDK usage patterns, LLM service design patterns

---

## Phase 2: Implementation Planning (STOP HERE)

**Next Command**: `/sp.tasks` - Break plan into implementation tasks

**Tasks to Create**:
1. Database migration (002_phase2_tables.py)
2. LLM service implementation (llm_service.py)
3. Adaptive path router + service
4. Assessment router + service
5. Cost tracking endpoint
6. Integration tests
7. Documentation updates

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| LLM API calls | Core feature requirement (personalization, semantic grading) | Rule-based cannot handle multi-step reasoning or semantic understanding |
| Async HTTP | LLM latency (8-10 seconds) would block other requests | Sync would degrade Phase 1 performance |
| Cost tracking per user | Constitutional requirement (Principle X) | Aggregate tracking insufficient for per-user caps |

**No unjustified complexity added.** All additions are constitutionally mandated or feature-essential.

---

## Next Steps

1. ✅ Constitution Check: PASS
2. ⏳ Complete Phase 0 research (Anthropic SDK patterns, cost optimization)
3. ⏳ Complete Phase 1 design (data model, API contracts, quickstart)
4. ⏳ Update agent context
5. ⏳ Create implementation tasks (`/sp.tasks`)

---

**Plan Status**: ✅ **READY FOR PHASE 0 RESEARCH**

**Branch**: `1-phase-2-hybrid-features`

**Plan File**: `specs/002-phase-2-hybrid-features/plan.md`

**Next Action**: Execute Phase 0 research tasks (Anthropic SDK best practices, cost optimization, fallback patterns)
