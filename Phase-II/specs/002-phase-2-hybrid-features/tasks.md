# Tasks: Phase 2 Hybrid Intelligence Layer

**Input**: Design documents from `specs/002-phase-2-hybrid-features/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md (optional), data-model.md (optional), contracts/ (optional)

**Tests**: Included (Phase 2 requires comprehensive testing for constitutional compliance)

**Organization**: Tasks organized by user story to enable independent implementation and testing.

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., [US1], [US2], [US3])
- Include exact file paths in descriptions

---

## ⚠️ PHASE 2 EXECUTION RULES

**BEFORE STARTING ANY PHASE 2 TASK:**

1. Verify Phase 1 is complete:
   ```bash
   cd backend
   pytest tests/ -v
   # All Phase 1 tests MUST pass
   ```

2. After EACH Phase 2 task, verify Phase 1 files unchanged:
   ```bash
   git diff backend/app/routers/chapters.py \
            backend/app/routers/quizzes.py \
            backend/app/routers/progress.py \
            backend/app/routers/search.py \
            backend/app/routers/access.py
   # Output MUST be empty (no changes to Phase 1 files)
   ```

3. Every task involving LLM calls MUST implement cost logging to `llm_usage` table

4. **Phase 1 files MUST NOT be modified** during any Phase 2 task

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and Phase 2 dependency setup

**Note**: Phase 1 backend is already complete. This phase adds Phase 2 dependencies only.

- [ ] T001 [P] Add anthropic dependency to backend/pyproject.toml
- [ ] T002 [P] Add Phase 2 environment variables to backend/.env.example:
  ```bash
  ANTHROPIC_API_KEY=sk-ant-...
  CLAUDE_MODEL=claude-sonnet-4-20250514
  LLM_MAX_TOKENS=1000
  ADAPTIVE_PATH_MAX_COST_USD=0.05
  ASSESSMENT_MAX_COST_USD=0.03
  USER_MONTHLY_LLM_CAP_USD=2.00
  ```
- [ ] T003 [P] Verify `import anthropic` works in Python environment

**Checkpoint**: Phase 2 dependencies installed, Phase 1 tests still pass

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Models

- [ ] T004 [P] Create LLMUsage model in backend/app/models/llm_usage.py
  - Fields: id (UUID), user_id (UUID, FK), feature_name (String), model (String), input_tokens (Integer), output_tokens (Integer), cost_usd (Numeric), created_at (DateTime)
  - Relationships: backref to User model

- [ ] T005 [P] Create AdaptiveRecommendation model in backend/app/models/adaptive.py
  - Fields: id (UUID), user_id (UUID, FK), recommended_chapters (JSONB), weak_areas (JSONB), strengths (JSONB), overall_assessment (Text), suggested_daily_minutes (Integer), llm_usage_id (UUID, FK), created_at (DateTime)
  - Relationships: backref to User model, one-to-one with LLMUsage

- [ ] T006 [P] Create AssessmentQuestion model in backend/app/models/assessment.py
  - Fields: id (UUID), chapter_id (String, FK to chapters), question_text (Text), model_answer_criteria (Text), difficulty (String: 'conceptual'|'analytical'|'applied'), sequence_order (Integer)
  - Relationships: backref to Chapter model

- [ ] T007 [P] Create AssessmentResult model in backend/app/models/assessment.py (same file as T006)
  - Fields: id (UUID), user_id (UUID, FK), question_id (UUID, FK), chapter_id (String, FK), answer_text (Text), score (Integer 0-100), grade (String 2 chars), correct_concepts (JSONB), missing_concepts (JSONB), feedback (Text), improvement_suggestions (Text), word_count (Integer), llm_usage_id (UUID, FK), submitted_at (DateTime)
  - Relationships: backref to User model, backref to AssessmentQuestion, one-to-one with LLMUsage

### Database Migration

- [ ] T008 Create Alembic migration backend/alembic/versions/002_phase2_tables.py
  - Creates tables: llm_usage, adaptive_recommendations, assessment_questions, assessment_results
  - Adds foreign key constraints
  - Creates indexes on user_id, chapter_id, created_at
  - Reversible (downgrade removes Phase 2 tables only, Phase 1 untouched)

- [ ] T009 Run migration and verify:
  ```bash
  cd backend
  alembic upgrade head
  # Verify: 4 new tables created, Phase 1 tables unchanged
  ```

### LLM Service (Shared Claude Wrapper)

- [ ] T010 Create custom exceptions in backend/app/services/llm_service.py:
  ```python
  class LLMParseError(Exception):
      """Raised when LLM response is not valid JSON"""
  
  class LLMUnavailableError(Exception):
      """Raised when LLM API times out or is unavailable"""
  ```

- [ ] T011 Create LLMService class in backend/app/services/llm_service.py:
  - `__init__`: Initialize AsyncAnthropic client with API key from env
  - `async call_claude()`: 
    - Accepts: system_prompt, user_prompt, max_tokens, feature_name, user_id, db session
    - Calls Claude Sonnet (claude-sonnet-4-20250514)
    - Parses JSON response (raises LLMParseError if invalid)
    - Calculates cost: (input_tokens × $0.000003) + (output_tokens × $0.000015)
    - Creates LLMUsage record BEFORE returning
    - Returns: tuple (parsed_json_dict, llm_usage_record)
    - Timeout: 15 seconds (raises LLMUnavailableError)

- [ ] T012 Write unit tests for LLMService in backend/tests/test_llm_service.py:
  - Test cost calculation with known token counts
  - Test JSON parsing with valid response
  - Test LLMParseError with invalid JSON
  - Test LLMUnavailableError with timeout
  - Mock anthropic.AsyncAnthropic - NO real API calls

### Pydantic Schemas

- [ ] T013 [P] Create Adaptive schemas in backend/app/schemas/adaptive.py:
  - `AdaptivePathRequest`: Empty request body (user derived from auth)
  - `RecommendedChapter`: chapter_id (str), title (str), priority (int), reason (str), estimated_time_minutes (int)
  - `AdaptiveRecommendationResponse`: recommended_chapters (list), weak_areas (list), strengths (list), overall_assessment (str), suggested_daily_goal_minutes (int)

- [ ] T014 [P] Create Assessment schemas in backend/app/schemas/assessment.py:
  - `AssessmentQuestionResponse`: question_id (UUID), question_text (str), difficulty (str) - NO model_answer_criteria
  - `SubmitAnswerRequest`: question_id (UUID), answer_text (str, 20-500 chars)
  - `AssessmentGradeResponse`: score (int 0-100), grade (str), correct_concepts (list), missing_concepts (list), feedback (str), improvement_suggestions (str), word_count (int)
  - `AssessmentResultSummary`: result_id (UUID), question_text (str), score (int), grade (str), submitted_at (datetime)

- [ ] T015 [P] Create LLM Usage schemas in backend/app/schemas/llm_usage.py:
  - `FeatureUsage`: feature_name (str), calls (int), cost_usd (float)
  - `CostSummaryResponse`: current_month (str), total_cost_usd (float), monthly_cap_usd (float), remaining_usd (float), usage_by_feature (dict)

**Checkpoint**: Foundation complete - all models, migration, LLM service, and schemas ready for user stories

---

## Phase 3: User Story 1 - Premium Student Gets Personalized Study Plan (Priority: P1) 🎯 MVP

**Goal**: Implement Adaptive Learning Path feature (Feature A)

**Independent Test**: Premium user can request learning path and receive structured recommendation; free user receives 403

### Tests for User Story 1 ⚠️

> **Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T016 [P] [US1] Write integration test: Free user POST /adaptive/learning-path → 403 in backend/tests/test_adaptive_path.py
- [ ] T017 [P] [US1] Write integration test: Premium user POST /adaptive/learning-path → 200 with recommendation structure
- [ ] T018 [P] [US1] Write integration test: GET /adaptive/learning-path/latest with no prior data → 200 with null
- [ ] T019 [P] [US1] Write integration test: GET /adaptive/learning-path/latest after POST → returns stored data, NO new LLM call
- [ ] T020 [P] [US1] Write integration test: LLM unavailable → fallback to latest recommendation

### Implementation for User Story 1

- [ ] T021 [US1] Create AdaptiveService class in backend/app/services/adaptive_service.py:
  - `async generate_learning_path(user, db)`:
    - Check user.tier == "premium" (raise HTTP 403 if not)
    - Collect data: progress_service.get_progress_summary(), get all chapters metadata
    - Build system_prompt and user_prompt per spec.md Appendix A
    - Call llm_service.call_claude()
    - Parse JSON into AdaptiveRecommendationResponse
    - Store in adaptive_recommendations table
    - Return response
  - `async get_latest_recommendation(user, db)`:
    - Check user.tier == "premium"
    - Query adaptive_recommendations for most recent by user_id
    - Return None if no records exist

- [ ] T022 [US1] Implement system and user prompt templates in backend/app/services/adaptive_service.py:
  - System prompt: "You are an educational analytics expert..." (per spec.md Appendix A)
  - User prompt template with student_progress_json and chapters_metadata_json
  - Hallucination guard: "Base ALL recommendations strictly on provided data"

- [ ] T023 Create Adaptive Path router in backend/app/routers/adaptive_path.py:
  - `POST /api/v2/adaptive/learning-path`:
    - Auth: required (get user from auth token)
    - Premium only check
    - Call adaptive_service.generate_learning_path()
    - Return APIResponse[AdaptiveRecommendationResponse]
  - `GET /api/v2/adaptive/learning-path/latest`:
    - Auth: required
    - Premium only check
    - Call adaptive_service.get_latest_recommendation()
    - Return APIResponse[AdaptiveRecommendationResponse | null]
    - Verify: NO LLM call (check llm_usage table - no new record)

- [ ] T024 [US1] Add error handling to adaptive_path.py:
  - Catch LLMUnavailableError → return 503 with "AI analysis temporarily unavailable"
  - Catch LLMParseError → return 500 with "AI response parsing failed"
  - Log all errors with user_id for debugging

- [ ] T025 [US1] Run integration tests for User Story 1:
  ```bash
  cd backend
  pytest tests/test_adaptive_path.py -v
  # All tests MUST pass
  ```

**Checkpoint**: User Story 1 complete - Adaptive Learning Path fully functional and independently testable

---

## Phase 4: User Story 2 - Premium Student Submits Written Answer for Feedback (Priority: P2)

**Goal**: Implement LLM-Graded Assessments feature (Feature B)

**Independent Test**: Premium user can submit written answer and receive detailed feedback; free user receives 403; word count validation works

### Seed Assessment Questions

- [ ] T026 [P] [US2] Create content/assessments/ch-001-assessments.json through ch-005-assessments.json:
  - 2 open-ended questions per chapter (10 total)
  - Each question: question_text, model_answer_criteria (3-4 bullet points), difficulty
  - Questions test conceptual understanding, not recall
  - Example: "In your own words, explain what an AI Agent is..."

- [ ] T027 [US2] Create seed script backend/seed/seed_assessments.py:
  - Reads JSON files from content/assessments/
  - Inserts into assessment_questions table
  - Preserves sequence_order
  - Idempotent (can run multiple times safely)

- [ ] T028 Run seed script and verify 10 questions inserted

### Tests for User Story 2 ⚠️

> **Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T029 [P] [US2] Write integration test: Free user GET /assessments/{id}/questions → 403
- [ ] T030 [P] [US2] Write integration test: Premium user GET questions → NO model_answer_criteria in response
- [ ] T031 [P] [US2] Write integration test: Submit answer < 20 words → 422 (too short)
- [ ] T032 [P] [US2] Write integration test: Submit answer > 500 words → 422 (too long)
- [ ] T033 [P] [US2] Write integration test: Submit valid answer → 200 with grade structure
- [ ] T034 [P] [US2] Write integration test: GET /assessments/{id}/results → returns previous submissions, NO LLM call

### Implementation for User Story 2

- [ ] T035 [US2] Create AssessmentService class in backend/app/services/assessment_service.py:
  - `async get_questions(chapter_id, user, db)`:
    - Check user.tier == "premium"
    - Check chapter access via access_service (Phase 1)
    - Query assessment_questions by chapter_id
    - Return list WITHOUT model_answer_criteria
  - `async grade_answer(chapter_id, question_id, answer_text, user, db)`:
    - Check user.tier == "premium"
    - Validate answer_text: 20-500 words (raise HTTP 422 if outside range)
    - Fetch question + model_answer_criteria from DB
    - Fetch chapter content from r2_service (Phase 1)
    - Build prompts per spec.md Appendix A
    - Call llm_service.call_claude()
    - Parse structured JSON response
    - Store in assessment_results table
    - Return AssessmentGradeResponse
  - `async get_results(chapter_id, user, db)`:
    - Check user.tier == "premium"
    - Query assessment_results by user_id + chapter_id
    - Return list of summaries (NO LLM call)

- [ ] T036 [US2] Implement assessment grading prompts in backend/app/services/assessment_service.py:
  - System prompt: "You are an expert educator grading..." (per spec.md Appendix A)
  - User prompt template with chapter_content, question_text, model_answer_criteria, student_answer
  - Hallucination guard: "Grade based ONLY on provided course content"
  - Expected JSON schema: score, grade, correct_concepts, missing_concepts, feedback, improvement_suggestions, word_count

- [ ] T037 Create Assessments router in backend/app/routers/assessments.py:
  - `GET /api/v2/assessments/{chapter_id}/questions`:
    - Auth: required, premium only
    - Call assessment_service.get_questions()
    - Return APIResponse[List[AssessmentQuestionResponse]]
    - CRITICAL: NO model_answer_criteria in response
  - `POST /api/v2/assessments/{chapter_id}/submit`:
    - Auth: required, premium only
    - Body: SubmitAnswerRequest (question_id, answer_text)
    - Call assessment_service.grade_answer()
    - Return APIResponse[AssessmentGradeResponse]
  - `GET /api/v2/assessments/{chapter_id}/results`:
    - Auth: required, premium only
    - Call assessment_service.get_results()
    - Return APIResponse[List[AssessmentResultSummary]]
    - Verify: NO LLM call

- [ ] T038 [US2] Add error handling to assessments.py:
  - Catch word count validation → 422 with "Answer must be 20-500 words"
  - Catch LLMUnavailableError → 503 with "Assessment grading temporarily unavailable"
  - Catch LLMParseError → 500 with "AI response parsing failed"

- [ ] T039 [US2] Run integration tests for User Story 2:
  ```bash
  cd backend
  pytest tests/test_assessments.py -v
  # All tests MUST pass
  ```

**Checkpoint**: User Story 2 complete - LLM-Graded Assessments fully functional and independently testable

---

## Phase 5: User Story 3 - Student Views Cost Usage Transparency (Priority: P3)

**Goal**: Implement cost tracking dashboard endpoint

**Independent Test**: Student can view monthly LLM usage breakdown with accurate costs

### Tests for User Story 3

- [ ] T040 [P] [US3] Write integration test: GET /users/me/cost-summary → accurate monthly total
- [ ] T041 [P] [US3] Write integration test: Free user sees { total_cost_usd: 0, note: "No hybrid features used" }
- [ ] T042 [P] [US3] Write integration test: After 2 LLM calls, cost summary reflects both calls

### Implementation for User Story 3

- [ ] T043 [US3] Add cost summary endpoint to backend/app/routers/users.py (ADD ONLY - no changes to existing endpoints):
  - `GET /api/v2/users/me/cost-summary`:
    - Auth: required (all tiers)
    - Query llm_usage for current calendar month by user_id
    - Calculate: total_cost_usd, calls per feature
    - Return CostSummaryResponse with:
      - current_month (e.g., "2026-03")
      - total_cost_usd
      - monthly_cap_usd (based on user tier: $2 premium, $5 pro)
      - remaining_usd
      - usage_by_feature: { "adaptive_path": { calls, cost_usd }, "assessment_grading": { calls, cost_usd } }
    - Free users: return { total_cost_usd: 0, monthly_cap_usd: 0, note: "No hybrid features used" }

- [ ] T044 [US3] Run integration tests for User Story 3:
  ```bash
  cd backend
  pytest tests/test_cost_tracking.py -v
  # All tests MUST pass
  ```

**Checkpoint**: User Story 3 complete - Cost transparency fully functional

---

## Phase 6: ChatGPT App Updates

**Purpose**: Update ChatGPT App configuration for Phase 2 features

- [ ] T045 Update chatgpt-app/openapi.yaml:
  - ADD 6 new Phase 2 endpoints (do NOT remove Phase 1 endpoints):
    - POST /api/v2/adaptive/learning-path
    - GET /api/v2/adaptive/learning-path/latest
    - GET /api/v2/assessments/{chapter_id}/questions
    - POST /api/v2/assessments/{chapter_id}/submit
    - GET /api/v2/assessments/{chapter_id}/results
    - GET /api/v2/users/me/cost-summary
  - All endpoints use APIKey authentication
  - All Phase 2 endpoints marked as premium-only in description
  - Validate OpenAPI 3.1 spec

- [ ] T046 Update chatgpt-app/system-prompt.md - ADD section:
  ```markdown
  ## Premium Feature Behavior
  
  ### Adaptive Learning Path
  Trigger: When student asks "What should I study?", "Give me a study plan", "What's next for me?"
  Action: Call POST /adaptive/learning-path
  Present: Narrate the recommendation warmly — don't just dump JSON
  Note: Only call this if student explicitly requests it.
  
  ### LLM Assessments
  Trigger: When student asks "Test my understanding", "Grade my answer", "I want a written test"
  Action: Call GET /assessments/{chapter_id}/questions, collect answer, call POST /assessments/{chapter_id}/submit
  Present: Lead with strengths ("Great job on X!"), then gently address gaps
  Note: Warn student that answers must be 20-500 words before they type.
  
  ### Free User Upgrade Prompt
  When a free user triggers a Phase 2 endpoint and receives 403:
  Say: "This is a premium feature. With Course Companion Premium, you get personalized study paths and detailed written feedback. Upgrade at [upgrade_url]."
  Never be pushy — mention upgrade once, then move on.
  ```

**Checkpoint**: ChatGPT App updated with Phase 2 features

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, compliance audit, and documentation

### Comprehensive Testing

- [ ] T047 Run full test suite:
  ```bash
  cd backend
  pytest tests/ -v
  # Phase 1 tests + Phase 2 tests MUST ALL pass
  ```

- [ ] T048 Verify test coverage:
  ```bash
  pytest --cov=app --cov-report=term-missing
  # Minimum 80% coverage on business logic
  ```

### Constitutional Compliance Audit

- [ ] T049 Run Phase 2 compliance audit script:
  ```bash
  # Verify Phase 1 files unchanged
  git diff HEAD -- backend/app/routers/chapters.py \
                  backend/app/routers/quizzes.py \
                  backend/app/routers/progress.py \
                  backend/app/routers/search.py \
                  backend/app/routers/access.py
  # Expected: empty output (no changes)
  
  # Verify anthropic imported ONLY in llm_service.py
  grep -r "import anthropic" backend/app/ --include="*.py"
  # Expected: only backend/app/services/llm_service.py
  
  # Verify premium gate in all Phase 2 routers
  grep -n "premium\|tier" backend/app/routers/adaptive_path.py \
                       backend/app/routers/assessments.py
  # Expected: premium checks present
  
  # Verify llm_usage logging
  grep -n "llm_usage\|log_usage" backend/app/services/adaptive_service.py \
                                   backend/app/services/assessment_service.py
  # Expected: logging present in both services
  ```

- [ ] T050 Manual verification checklist:
  - [ ] Phase 1 files unchanged (git diff empty)
  - [ ] Exactly 2 hybrid features implemented (Adaptive Path + LLM Assessment)
  - [ ] Both features premium-gated (test with free user token → 403)
  - [ ] Both features user-initiated (no auto-triggers in code)
  - [ ] llm_usage table populated after every LLM call
  - [ ] Cost tracking accessible via /users/me/cost-summary
  - [ ] LLM fallback works when API unavailable (mock test)
  - [ ] All LLM responses are structured JSON (not raw text)

### Documentation

- [ ] T051 Create docs/phase2-cost-analysis.md:
  - Feature A cost breakdown (tokens, cost per request, monthly estimate)
  - Feature B cost breakdown (tokens, cost per request, monthly estimate)
  - Total cost per premium user/month
  - Revenue vs cost analysis (gross margin calculation)
  - Why hybrid is justified for each feature (per spec.md LLM justification)

- [ ] T052 Update backend/README.md:
  - ADD Phase 2 setup section (ANTHROPIC_API_KEY configuration)
  - ADD Phase 2 features overview
  - ADD testing instructions for Phase 2

- [ ] T053 Create specs/002-phase-2-hybrid-features/CHECKPOINT-P2-FINAL.md:
  - Complete Phase 2 constitution checklist (Section 7 from constitution.md v2.0.0)
  - Sign-off: All constitutional requirements verified
  - Reviewer notes and approval

**Checkpoint**: Phase 2 complete and ready for submission

---

## Dependency Graph

```
Phase 1: Setup (T001-T003)
    ↓
Phase 2: Foundational (T004-T015)
    ├─ Models (T004-T007)
    ├─ Migration (T008-T009)
    ├─ LLM Service (T010-T012)
    └─ Schemas (T013-T015)
    ↓
Phase 3: User Story 1 - Adaptive Path (T016-T025) [P1 - MVP]
    ├─ Tests (T016-T020)
    ├─ Service (T021-T022)
    ├─ Router (T023-T024)
    └─ Integration Test (T025)
    ↓
Phase 4: User Story 2 - Assessments (T026-T039) [P2]
    ├─ Seed Questions (T026-T028)
    ├─ Tests (T029-T034)
    ├─ Service (T035-T036)
    ├─ Router (T037-T038)
    └─ Integration Test (T039)
    ↓
Phase 5: User Story 3 - Cost Transparency (T040-T044) [P3]
    ├─ Tests (T040-T042)
    ├─ Endpoint (T043)
    └─ Integration Test (T044)
    ↓
Phase 6: ChatGPT App Updates (T045-T046)
    ↓
Phase 7: Polish & Compliance (T047-T053)
```

---

## Parallel Execution Opportunities

**Within Phases (different files, no dependencies):**

- **Phase 1**: T001, T002, T003 can all run in parallel
- **Phase 2**: T004, T005, T006, T007 (models) can run in parallel; T013, T014, T015 (schemas) can run in parallel
- **Phase 3**: T016, T017, T018, T019, T020 (tests) can run in parallel
- **Phase 4**: T029, T030, T031, T032, T033, T034 (tests) can run in parallel
- **Phase 5**: T040, T041, T042 (tests) can run in parallel

**Across User Stories (after Phase 2 foundational):**

- User Story 1 (Phase 3) and User Story 2 (Phase 4) can run in PARALLEL after T015 complete
  - Different routers, different services, different models
  - Shared dependency: llm_service.py (T010-T012) must be complete first
- User Story 3 (Phase 5) can run in parallel with US1 or US2
  - Only depends on llm_usage table (T004) and schemas (T015)

**Recommended Parallel Strategy:**

```
After T015 (Foundation complete):
  Team A: User Story 1 (T016-T025) - Adaptive Path
  Team B: User Story 2 (T026-T039) - Assessments
  Team C: User Story 3 (T040-T044) - Cost Transparency + ChatGPT App (T045-T046)
  
All teams merge at Phase 7 (T047-T053) for integration testing and compliance audit
```

---

## Implementation Strategy

### MVP Scope (Minimum Viable Phase 2)

**MVP = User Story 1 Only (Adaptive Learning Path)**

- T001-T015: Foundation (required for any Phase 2)
- T016-T025: User Story 1 (Adaptive Path)
- T045-T046: ChatGPT App updates (minimal - just Adaptive Path triggers)
- T047, T049, T050: Compliance audit (constitutional requirement)

**MVP delivers:**
- Premium users can request personalized learning path
- Free users blocked with 403
- Cost tracking functional
- Constitutional compliance verified

**MVP Independent Test:**
```bash
# Premium user flow
curl -X POST http://localhost:8000/api/v2/adaptive/learning-path \
  -H "Authorization: Bearer PREMIUM_USER_TOKEN"
# Expected: 200 with recommendation structure

# Free user flow
curl -X POST http://localhost:8000/api/v2/adaptive/learning-path \
  -H "Authorization: Bearer FREE_USER_TOKEN"
# Expected: 403 with upgrade message
```

### Incremental Delivery

**After MVP → Full Phase 2:**

1. **Increment 1**: User Story 2 (LLM Assessments)
   - Adds written assessment capability
   - Requires T026-T039
   - Independent testable from User Story 1

2. **Increment 2**: User Story 3 (Cost Transparency)
   - Adds /users/me/cost-summary endpoint
   - Requires T040-T044
   - Completes constitutional requirement (CC-04)

3. **Increment 3**: Polish & Documentation
   - Full test suite (T047-T048)
   - Compliance audit (T049-T050)
   - Documentation (T051-T053)

---

## Task Summary

| Phase | Description | Task Count | Story |
|-------|-------------|------------|-------|
| Phase 1 | Setup | 3 | - |
| Phase 2 | Foundational | 12 | - |
| Phase 3 | User Story 1 (Adaptive Path) | 10 | US1 |
| Phase 4 | User Story 2 (Assessments) | 14 | US2 |
| Phase 5 | User Story 3 (Cost Transparency) | 5 | US3 |
| Phase 6 | ChatGPT App Updates | 2 | - |
| Phase 7 | Polish & Compliance | 7 | - |
| **Total** | **All Phases** | **53 tasks** | **-** |

**Parallelizable Tasks:** 18 tasks marked [P]

**Independent Test Criteria:**
- US1: Premium user gets recommendation, free user gets 403
- US2: Premium user submits answer, gets feedback; word count enforced
- US3: Student views accurate cost summary

---

**Tasks Status**: ✅ **READY FOR IMPLEMENTATION**

**Next Command**: `/sp.implement` - Start implementation with Phase 1 Setup tasks

**Branch**: `1-phase-2-hybrid-features`

**Tasks File**: `specs/002-phase-2-hybrid-features/tasks.md`
