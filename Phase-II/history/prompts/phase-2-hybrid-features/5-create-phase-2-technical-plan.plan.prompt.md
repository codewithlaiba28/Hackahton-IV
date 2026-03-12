---
id: 5
title: "Create Phase 2 Technical Implementation Plan"
stage: "plan"
date_iso: "2026-03-11"
surface: "agent"
model: "qwen-code"
feature: "phase-2-hybrid-features"
branch: "1-phase-2-hybrid-features"
user: "Administrator"
command: "/sp.plan Phase 2 Technical Implementation Plan"
labels: ["plan", "phase-2", "hybrid-intelligence", "technical-design", "llm-integration"]
links:
  spec: "specs/002-phase-2-hybrid-features/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml: |
  - specs/002-phase-2-hybrid-features/plan.md
  - specs/002-phase-2-hybrid-features/spec.md
  - .specify/memory/constitution.md (v2.0.0)
tests_yaml: |
  - Constitution Check: All Phase 1 principles PASS
  - Constitution Check: All Phase 2 principles PASS
  - Technical context complete (no NEEDS CLARIFICATION markers)
  - Project structure defined (new files identified)
  - LLM service architecture documented
  - API endpoints specified (6 new, 0 modified)
  - Database schema outlined (4 new tables)
prompt_text: |
  /sp.plan Phase 2 Technical Implementation Plan

  Purpose: Defines HOW Phase 2 will be built on top of Phase 1. New database tables,
  new services, new routes, and the LLM integration pattern.

  Key Requirements:
  - Preserve Phase 1 Zero-Backend-LLM architecture
  - Add selective LLM calls for premium features only
  - Implement cost tracking and premium gating
  - Maintain architectural separation (Phase 1 files unchanged)
response_text: |
  Phase 2 Implementation Plan completed at specs/002-phase-2-hybrid-features/plan.md

  Key Deliverables:
  - Technical Context: Python 3.12+, FastAPI, anthropic SDK, PostgreSQL
  - Constitution Check: All 12 principles verified (PASS)
  - Project Structure: 7 new files identified (routers, services, models, schemas)
  - LLM Service Architecture: llm_service.py as single point of Anthropic integration
  - API Endpoints: 6 new (/api/v2/...), 0 Phase 1 modifications
  - Database Schema: 4 new tables (llm_usage, adaptive_recommendations, assessment_questions, assessment_results)
  - Cost Calculation: Claude Sonnet pricing ($0.000003/input token, $0.000015/output token)

  Constitutional Compliance:
  - Phase 1 Principles (I-VII): All PASS ✅
  - Phase 2 Principles (VIII-XII): All PASS ✅
  - Zero modifications to Phase 1 files ✅
  - Premium gating before LLM calls ✅
  - Cost tracking per user ✅

  Architecture Highlights:
  - Single responsibility: llm_service.py ONLY file importing anthropic
  - Async HTTP for non-blocking LLM calls
  - Structured JSON output for all LLM responses
  - Fallback handling for LLM failures
  - Per-request cost ceilings ($0.05/$0.03)
  - Monthly user caps ($2/$5)

  Next Phase: /sp.tasks - Create Implementation Tasks
---

## Prompt

/sp.plan Phase 2 Technical Implementation Plan

Purpose: Defines HOW Phase 2 will be built on top of Phase 1. New database tables,
new services, new routes, and the LLM integration pattern.

Key Requirements:
- Preserve Phase 1 Zero-Backend-LLM architecture
- Add selective LLM calls for premium features only
- Implement cost tracking and premium gating
- Maintain architectural separation (Phase 1 files unchanged)

## Response snapshot

Phase 2 Implementation Plan completed at specs/002-phase-2-hybrid-features/plan.md

**Key Deliverables:**
- Technical Context: Python 3.12+, FastAPI, anthropic SDK, PostgreSQL
- Constitution Check: All 12 principles verified (PASS)
- Project Structure: 7 new files identified (routers, services, models, schemas)
- LLM Service Architecture: llm_service.py as single point of Anthropic integration
- API Endpoints: 6 new (/api/v2/...), 0 Phase 1 modifications
- Database Schema: 4 new tables (llm_usage, adaptive_recommendations, assessment_questions, assessment_results)
- Cost Calculation: Claude Sonnet pricing ($0.000003/input token, $0.000015/output token)

**Constitutional Compliance:**
- Phase 1 Principles (I-VII): All PASS ✅
- Phase 2 Principles (VIII-XII): All PASS ✅
- Zero modifications to Phase 1 files ✅
- Premium gating before LLM calls ✅
- Cost tracking per user ✅

**Architecture Highlights:**
- Single responsibility: llm_service.py ONLY file importing anthropic
- Async HTTP for non-blocking LLM calls
- Structured JSON output for all LLM responses
- Fallback handling for LLM failures
- Per-request cost ceilings ($0.05/$0.03)
- Monthly user caps ($2/$5)

**Next Phase:** /sp.tasks - Create Implementation Tasks

## Outcome

- ✅ Impact: Phase 2 technical plan complete, ready for task breakdown
- 🧪 Tests: Constitution Check passed (12/12 principles)
- 📁 Files: 1 plan created, branch 1-phase-2-hybrid-features
- 🔁 Next prompts: Create implementation tasks (/sp.tasks)
- 🧠 Reflection: Plan maintains Phase 1 purity while adding Phase 2 capabilities

## Evaluation notes (flywheel)

- Failure modes observed: None - plan generation smooth
- Graders run and results (PASS/FAIL): PASS - Constitution Check 12/12
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Create implementation tasks with clear dependencies

## Plan Highlights

### Constitution Check Results

**Phase 1 Principles (Preserved):**
- I. Zero-Backend-LLM: ✅ PASS (Phase 1 endpoints unchanged)
- II. Determinism: ✅ PASS (Phase 1 remains rule-based)
- III. Content Verbatim: ✅ PASS (unchanged)
- IV. ChatGPT is Brain: ✅ PASS (Phase 2 additive only)
- V. Progress Persistence: ✅ PASS (same PostgreSQL)
- VI. Single Responsibility: ✅ PASS (new endpoints follow pattern)
- VII. Freemium Enforcement: ✅ PASS (enhanced with premium gating)

**Phase 2 Principles (Added):**
- VIII. Hybrid Selectivity Law: ✅ PASS (2 features, premium-only, user-initiated, cost-tracked)
- IX. Architectural Separation: ✅ PASS (separate routers, /api/v2/ versioning)
- X. Cost Control Standards: ✅ PASS (ceilings, caps, logging, transparency)
- XI. LLM Quality Standards: ✅ PASS (grounding, guards, structured output, fallbacks)
- XII. Premium Gate Enforcement: ✅ PASS (tier checks, clear messages, no partial access)

**Overall: 12/12 PASS (100%)**

### Technical Architecture

**New Files (7):**
1. `routers/adaptive_path.py` - Feature A endpoint
2. `routers/assessments.py` - Feature B endpoint
3. `services/llm_service.py` - Claude API wrapper (ONLY anthropic import)
4. `services/adaptive_service.py` - Feature A business logic
5. `services/assessment_service.py` - Feature B business logic
6. `models/adaptive.py` - AdaptiveRecommendation model
7. `models/assessment.py` - AssessmentQuestion, AssessmentResult models
8. `models/llm_usage.py` - LLMUsage cost tracking model
9. `schemas/adaptive.py` - Feature A request/response schemas
10. `schemas/assessment.py` - Feature B request/response schemas
11. `schemas/llm_usage.py` - Cost summary schema

**New Tables (4):**
1. `llm_usage` - Cost tracking (user_id, feature, tokens, cost)
2. `adaptive_recommendations` - Personalized learning paths
3. `assessment_questions` - Open-ended questions (separate from MCQ)
4. `assessment_results` - LLM-graded submissions

**New Endpoints (6):**
1. POST /api/v2/adaptive/learning-path - Generate path (LLM)
2. GET /api/v2/adaptive/learning-path/latest - Get cached (no LLM)
3. GET /api/v2/assessments/{chapter_id}/questions - Get questions
4. POST /api/v2/assessments/{chapter_id}/submit - Grade answer (LLM)
5. GET /api/v2/assessments/{chapter_id}/results - Get results
6. GET /api/v2/users/me/cost-summary - Usage dashboard

**Phase 1 Endpoints Modified: 0** ✅

### LLM Integration Pattern

**Service Architecture:**
```
ChatGPT App → Router → Service → llm_service.py → Anthropic API
                         ↓
                   Phase 1 Services (unchanged)
                         ↓
                   Progress, R2, Access
```

**Key Design:**
- `llm_service.py` is ONLY file importing `anthropic`
- All other Phase 2 services call `llm_service`, never `anthropic` directly
- Ensures clean separation, easy testing, single point of failure handling

**Cost Calculation:**
- Input: $0.000003/token
- Output: $0.000015/token
- Example: 2000 input + 1000 output = $0.021

### Cost Control Implementation

**Per-Request Ceilings:**
- Adaptive Path: $0.05 max (~16,667 tokens)
- Assessment: $0.03 max (~10,000 tokens)

**Monthly User Caps:**
- Premium tier: $2.00 max
- Pro tier: $5.00 max

**Enforcement:**
- Check before LLM call
- Return 429 if cap exceeded
- Log every call to `llm_usage` table
- Expose via `/users/me/cost-summary`

## Files Modified

**Primary:**
- `specs/002-phase-2-hybrid-features/plan.md` - Complete implementation plan

**Branch:**
- `1-phase-2-hybrid-features` - Created and checked out

**Related:**
- `specs/002-phase-2-hybrid-features/spec.md` - Input specification
- `.specify/memory/constitution.md` - v2.0.0 (compliance verified)

## Next Steps

1. ✅ Constitution v2.0.0 complete
2. ✅ Skills created (4 Phase 2 skills)
3. ✅ Specification complete
4. ✅ Technical plan complete (this deliverable)
5. ⏳ Create implementation tasks (/sp.tasks)
6. ⏳ Phase 0: Research (Anthropic SDK patterns)
7. ⏳ Phase 1: Design (data model, API contracts)
8. ⏳ Phase 2: Implementation (7 new files)
9. ⏳ Database migration
10. ⏳ Integration tests
11. ⏳ Demo video
