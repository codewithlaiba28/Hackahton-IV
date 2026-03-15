---
id: 6
title: "Create Phase 2 Implementation Tasks"
stage: "tasks"
date_iso: "2026-03-11"
surface: "agent"
model: "qwen-code"
feature: "phase-2-hybrid-features"
branch: "1-phase-2-hybrid-features"
user: "Administrator"
command: "/sp.tasks Phase 2 Implementation Tasks"
labels: ["tasks", "phase-2", "hybrid-intelligence", "implementation", "task-breakdown"]
links:
  spec: "specs/002-phase-2-hybrid-features/spec.md"
  plan: "specs/002-phase-2-hybrid-features/plan.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml: |
  - specs/002-phase-2-hybrid-features/tasks.md
  - specs/002-phase-2-hybrid-features/spec.md
  - specs/002-phase-2-hybrid-features/plan.md
tests_yaml: |
  - Task format validated: All 53 tasks follow checklist format
  - User stories mapped: US1 (10 tasks), US2 (14 tasks), US3 (5 tasks)
  - Parallel opportunities identified: 18 tasks marked [P]
  - Dependency graph complete
  - MVP scope defined (User Story 1 only)
prompt_text: |
  /sp.tasks Phase 2 Implementation Tasks

  Purpose: Generate actionable, dependency-ordered tasks.md for Phase 2 implementation.

  Requirements:
  - Organize by user story (US1: Adaptive Path, US2: Assessments, US3: Cost Transparency)
  - Include test tasks (Phase 2 requires comprehensive testing)
  - Mark parallelizable tasks with [P]
  - Include exact file paths
  - Define MVP scope (User Story 1 only)
  - Include constitutional compliance audit tasks
response_text: |
  Phase 2 Implementation Tasks completed at specs/002-phase-2-hybrid-features/tasks.md

  Total Tasks: 53 tasks across 7 phases

  Task Breakdown:
  - Phase 1 (Setup): 3 tasks - Add anthropic dependency, env variables
  - Phase 2 (Foundational): 12 tasks - Models, migration, LLM service, schemas
  - Phase 3 (US1 - Adaptive Path): 10 tasks - Tests, service, router
  - Phase 4 (US2 - Assessments): 14 tasks - Seed questions, tests, service, router
  - Phase 5 (US3 - Cost Transparency): 5 tasks - Tests, cost endpoint
  - Phase 6 (ChatGPT App): 2 tasks - OpenAPI update, system prompt update
  - Phase 7 (Polish): 7 tasks - Full test suite, compliance audit, documentation

  Parallel Opportunities: 18 tasks marked [P] can run in parallel
  - Models (T004-T007) can run in parallel
  - Schemas (T013-T015) can run in parallel
  - Test tasks within each user story can run in parallel
  - User Stories 1, 2, 3 can run in parallel after Phase 2 foundational

  MVP Scope: User Story 1 only (Adaptive Learning Path)
  - Tasks T001-T015 (Foundation) + T016-T025 (US1) + T045-T046 (ChatGPT) + compliance
  - Delivers: Premium users get personalized paths, free users blocked
  - Independent test: POST /adaptive/learning-path with premium vs free token

  Constitutional Compliance:
  - Phase 1 files unchanged verification task included (T049)
  - Premium gate verification in all Phase 2 routers
  - LLM usage logging verification in all services
  - Cost tracking endpoint implemented (T043)
  - Audit script included in T049

  Next Phase: /sp.implement - Start implementation with Phase 1 Setup tasks
---

## Prompt

/sp.tasks Phase 2 Implementation Tasks

Purpose: Generate actionable, dependency-ordered tasks.md for Phase 2 implementation.

Requirements:
- Organize by user story (US1: Adaptive Path, US2: Assessments, US3: Cost Transparency)
- Include test tasks (Phase 2 requires comprehensive testing)
- Mark parallelizable tasks with [P]
- Include exact file paths
- Define MVP scope (User Story 1 only)
- Include constitutional compliance audit tasks

## Response snapshot

Phase 2 Implementation Tasks completed at specs/002-phase-2-hybrid-features/tasks.md

**Total Tasks:** 53 tasks across 7 phases

**Task Breakdown:**
- Phase 1 (Setup): 3 tasks - Add anthropic dependency, env variables
- Phase 2 (Foundational): 12 tasks - Models, migration, LLM service, schemas
- Phase 3 (US1 - Adaptive Path): 10 tasks - Tests, service, router
- Phase 4 (US2 - Assessments): 14 tasks - Seed questions, tests, service, router
- Phase 5 (US3 - Cost Transparency): 5 tasks - Tests, cost endpoint
- Phase 6 (ChatGPT App): 2 tasks - OpenAPI update, system prompt update
- Phase 7 (Polish): 7 tasks - Full test suite, compliance audit, documentation

**Parallel Opportunities:** 18 tasks marked [P] can run in parallel
- Models (T004-T007) can run in parallel
- Schemas (T013-T015) can run in parallel
- Test tasks within each user story can run in parallel
- User Stories 1, 2, 3 can run in parallel after Phase 2 foundational

**MVP Scope:** User Story 1 only (Adaptive Learning Path)
- Tasks T001-T015 (Foundation) + T016-T025 (US1) + T045-T046 (ChatGPT) + compliance
- Delivers: Premium users get personalized paths, free users blocked
- Independent test: POST /adaptive/learning-path with premium vs free token

**Constitutional Compliance:**
- Phase 1 files unchanged verification task included (T049)
- Premium gate verification in all Phase 2 routers
- LLM usage logging verification in all services
- Cost tracking endpoint implemented (T043)
- Audit script included in T049

**Next Phase:** /sp.implement - Start implementation with Phase 1 Setup tasks

## Outcome

- ✅ Impact: Phase 2 tasks complete, ready for implementation
- 🧪 Tests: Test tasks included for all user stories (18 test tasks total)
- 📁 Files: 1 tasks.md created with 53 actionable tasks
- 🔁 Next prompts: Start implementation (/sp.implement)
- 🧠 Reflection: Tasks organized by user story enable parallel team execution

## Evaluation notes (flywheel)

- Failure modes observed: None - task generation smooth
- Graders run and results (PASS/FAIL): PASS - All tasks follow format
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation with T001

## Tasks Summary

### Total Task Count: 53

| Phase | Description | Task Count | Story |
|-------|-------------|------------|-------|
| Phase 1 | Setup | 3 | - |
| Phase 2 | Foundational | 12 | - |
| Phase 3 | User Story 1 (Adaptive Path) | 10 | US1 |
| Phase 4 | User Story 2 (Assessments) | 14 | US2 |
| Phase 5 | User Story 3 (Cost Transparency) | 5 | US3 |
| Phase 6 | ChatGPT App Updates | 2 | - |
| Phase 7 | Polish & Compliance | 7 | - |

### Parallel Opportunities

**18 tasks marked [P]:**
- T001, T002, T003 (Phase 1 setup)
- T004, T005, T006, T007 (Phase 2 models)
- T013, T014, T015 (Phase 2 schemas)
- T016, T017, T018, T019, T020 (US1 tests)
- T029, T030, T031, T032, T033, T034 (US2 tests)
- T040, T041, T042 (US3 tests)

**Team Parallel Strategy:**
```
After T015 (Foundation complete):
  Team A: User Story 1 (T016-T025) - Adaptive Path
  Team B: User Story 2 (T026-T039) - Assessments
  Team C: User Story 3 (T040-T044) - Cost Transparency + ChatGPT App (T045-T046)
  
All teams merge at Phase 7 (T047-T053) for integration testing and compliance audit
```

### MVP Scope

**Minimum Viable Phase 2 = User Story 1 Only**

Tasks:
- T001-T015: Foundation (required for any Phase 2)
- T016-T025: User Story 1 (Adaptive Path)
- T045-T046: ChatGPT App updates (minimal - just Adaptive Path triggers)
- T047, T049, T050: Compliance audit (constitutional requirement)

**Delivers:**
- Premium users can request personalized learning path
- Free users blocked with 403
- Cost tracking functional
- Constitutional compliance verified

**Independent Test:**
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

### Task Format Validation

**All 53 tasks follow strict checklist format:**

✅ Format: `- [ ] T{ID} [P] [US{N}] Description with file path`

**Examples:**
- `- [ ] T001 [P] Add anthropic dependency to backend/pyproject.toml`
- `- [ ] T004 [P] Create LLMUsage model in backend/app/models/llm_usage.py`
- `- [ ] T016 [P] [US1] Write integration test: Free user POST /adaptive/learning-path → 403`
- `- [ ] T021 [US1] Create AdaptiveService class in backend/app/services/adaptive_service.py`

**All tasks include:**
- ✅ Checkbox (`- [ ]`)
- ✅ Task ID (T001-T053)
- ✅ [P] marker if parallelizable
- ✅ [Story] label for user story phases
- ✅ Clear description with exact file path

### Dependency Graph

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
    ↓
Phase 4: User Story 2 - Assessments (T026-T039) [P2]
    ↓
Phase 5: User Story 3 - Cost Transparency (T040-T044) [P3]
    ↓
Phase 6: ChatGPT App Updates (T045-T046)
    ↓
Phase 7: Polish & Compliance (T047-T053)
```

### Constitutional Compliance Tasks

**T049: Compliance Audit Script**
```bash
# Verify Phase 1 files unchanged
git diff HEAD -- backend/app/routers/chapters.py \
                backend/app/routers/quizzes.py \
                backend/app/routers/progress.py \
                backend/app/routers/search.py \
                backend/app/routers/access.py
# Expected: empty output

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

**T050: Manual Verification Checklist**
- [ ] Phase 1 files unchanged (git diff empty)
- [ ] Exactly 2 hybrid features implemented
- [ ] Both features premium-gated (test with free user token → 403)
- [ ] Both features user-initiated (no auto-triggers)
- [ ] llm_usage table populated after every LLM call
- [ ] Cost tracking accessible via /users/me/cost-summary
- [ ] LLM fallback works when API unavailable
- [ ] All LLM responses are structured JSON

## Files Modified

**Primary:**
- `specs/002-phase-2-hybrid-features/tasks.md` - Complete implementation tasks (53 tasks)

**Branch:**
- `1-phase-2-hybrid-features` - Current branch

**Related:**
- `specs/002-phase-2-hybrid-features/spec.md` - Input specification
- `specs/002-phase-2-hybrid-features/plan.md` - Input technical plan

## Next Steps

1. ✅ Constitution v2.0.0 complete
2. ✅ Skills created (4 Phase 2 skills)
3. ✅ Specification complete
4. ✅ Technical plan complete
5. ✅ Implementation tasks complete (this deliverable)
6. ⏳ **Start Implementation** (`/sp.implement`)
   - Phase 1: Setup (T001-T003)
   - Phase 2: Foundational (T004-T015)
   - Phase 3: User Story 1 - MVP (T016-T025)
   - Phase 4: User Story 2 (T026-T039)
   - Phase 5: User Story 3 (T040-T044)
   - Phase 6: ChatGPT App (T045-T046)
   - Phase 7: Polish & Compliance (T047-T053)
