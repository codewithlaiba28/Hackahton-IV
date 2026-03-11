# Tasks: Course Companion FTE - Phase 1 Core Features

**Input**: Design documents from `/specs/001-complete-phase-1/`
**Prerequisites**: plan.md (required), spec.md (for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are INCLUDED in this task list to ensure comprehensive coverage.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `backend/` at repository root
- Paths shown below assume single project structure from plan.md

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend directory structure per plan.md:
  - backend/app/ with __init__.py files
  - backend/app/models/, /schemas/, /routers/, /services/, /utils/
  - backend/tests/, backend/alembic/, backend/seed/
  - backend/pyproject.toml, backend/.env.example, backend/Dockerfile
- [ ] T002 [P] Initialize pyproject.toml with dependencies:
  - fastapi, uvicorn, SQLAlchemy[asyncio], asyncpg, pydantic-settings
  - boto3, alembic, pytest, httpx, pytest-asyncio
- [ ] T003 [P] Create .env.example with all required variables:
  - DATABASE_URL, R2_ENDPOINT_URL, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME
- [ ] T004 Create README.md with project overview, setup instructions, API reference

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 [P] Implement Pydantic Settings class in backend/app/config.py
- [ ] T006 [P] Implement async SQLAlchemy engine and session factory in backend/app/database.py
- [ ] T007 [P] Create standard response envelope schemas in backend/app/schemas/common.py:
  - APIResponse[T], ErrorResponse, MetaInfo
- [ ] T008 [P] Implement API key authentication in backend/app/auth.py:
  - get_current_user dependency reading X-API-Key header
  - Returns 401 for missing/invalid keys
- [ ] T009 [P] Create all SQLAlchemy ORM models in backend/app/models/:
  - user.py (User, UserTier enum)
  - chapter.py (Chapter with tsvector)
  - quiz.py (QuizQuestion, QuizAttempt)
  - progress.py (ChapterProgress, DailyActivity)
- [ ] T010 Configure Alembic and create initial migration:
  - backend/alembic/env.py configured for async
  - backend/alembic/versions/001_initial_schema.py
- [ ] T011 Create test fixtures in backend/tests/conftest.py:
  - async test fixtures, test DB setup, auth fixtures

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Access Course Content (P1) 🎯 MVP

**Goal**: Students can view chapter list and read chapter content with freemium enforcement

**Independent Test**: Can fetch chapter list and read individual chapters; free users blocked from chapters 4+

### Implementation for User Story 1

- [ ] T012 [P] [US1] Create R2 service in backend/app/services/r2_service.py:
  - Initialize boto3 client with R2 endpoint
  - get_chapter_content() fetches from R2, returns raw Markdown
  - Include simple LRU cache (max 50 items, 5 min TTL)
- [ ] T013 [P] [US1] Create chapter schemas in backend/app/schemas/chapter.py:
  - ChapterMeta (id, title, difficulty, is_free, is_locked, etc.)
  - ChapterDetail (extends ChapterMeta with content: str)
  - ChapterListResponse (list of ChapterMeta)
- [ ] T014 [P] [US1] Create access service in backend/app/services/access_service.py:
  - check_chapter_access(user, chapter) -> AccessResult
  - Free users: chapters 1-3 only
- [ ] T015 [US1] Implement chapters router in backend/app/routers/chapters.py:
  - GET /chapters → returns ChapterListResponse with is_locked per user tier
  - GET /chapters/{chapter_id} → returns ChapterDetail with content from R2
  - Enforce freemium gate (403 for chapters 4+ on free tier)
- [ ] T016 [US1] Create seed script for course content in backend/seed/seed_chapters.py:
  - Upload 5 chapters to R2 (ch-001 through ch-005)
  - Insert chapter metadata into DB
  - Chapters 1-3: free, Chapters 4-5: premium
- [ ] T017 [US1] Add integration tests in backend/tests/test_chapters.py:
  - Test free user can access chapters 1-3
  - Test free user gets 403 on chapters 4-5
  - Test premium user can access all chapters
  - Test content retrieved from R2 correctly

**Checkpoint**: User Story 1 complete - MVP ready (content delivery works with freemium gate)

---

## Phase 4: User Story 2 - Navigate Through Course (P2)

**Goal**: Students can navigate to next/previous chapters in sequence

**Independent Test**: Can fetch next/prev chapter metadata; boundaries return null

### Implementation for User Story 2

- [ ] T018 [P] [US2] Add navigation endpoints to backend/app/routers/chapters.py:
  - GET /chapters/{chapter_id}/next → returns ChapterMeta of next chapter
  - GET /chapters/{chapter_id}/prev → returns ChapterMeta of previous chapter
  - Return null at boundaries (first chapter has no prev, last has no next)
  - Enforce freemium gate (free users can't navigate to gated chapters)
- [ ] T019 [US2] Add navigation tests in backend/tests/test_chapters.py:
  - Test first chapter returns null for prev
  - Test last chapter returns null for next
  - Test middle chapters return correct adjacent metadata
  - Test freemium gate enforced on navigation

**Checkpoint**: User Stories 1 AND 2 complete - content delivery with navigation works

---

## Phase 5: User Story 3 - Test Understanding with Quizzes (P3)

**Goal**: Students can take quizzes, get graded, and see feedback

**Independent Test**: Can fetch quiz questions (without answers), submit answers, receive graded results

### Implementation for User Story 3

- [ ] T020 [P] [US3] Create quiz schemas in backend/app/schemas/quiz.py:
  - QuizQuestion (id, question_text, question_type, options - NO correct_answer)
  - QuizSubmission (answers: list of {question_id, answer})
  - QuestionResult (question_id, correct, correct_answer, explanation)
  - QuizResult (score, total, percentage, results)
  - QuizAttemptSummary (chapter_id, best_score, attempts_count)
- [ ] T021 [P] [US3] Create quiz service in backend/app/services/quiz_service.py:
  - get_quiz_questions(chapter_id) → returns questions WITHOUT answers
  - grade_quiz(chapter_id, submission, user) → grades by exact string match
  - get_best_score(chapter_id, user_id) → returns best attempt
  - Record all attempts in quiz_attempts table
- [ ] T022 [US3] Implement quizzes router in backend/app/routers/quizzes.py:
  - GET /quizzes/{chapter_id} → returns questions without answers
  - POST /quizzes/{chapter_id}/submit → grades and returns result
  - GET /quizzes/{chapter_id}/best-score → returns best attempt
  - Enforce freemium gate on all quiz endpoints
- [ ] T023 [P] [US3] Create seed script for quiz bank in backend/seed/seed_quizzes.py:
  - Seed 5 quizzes (one per chapter) with 5 questions each
  - Mix of MCQ and true_false question types
  - Load from content/quizzes/ch-XXX-quiz.json files
- [ ] T024 [US3] Add quiz tests in backend/tests/test_quizzes.py:
  - Test get_quiz_questions does NOT return answer keys
  - Test grade_quiz with all correct → 100%
  - Test grade_quiz with all wrong → 0%
  - Test grade_quiz with mixed → correct percentage
  - Test freemium gate enforced
  - Test attempts recorded in database

**Checkpoint**: User Stories 1, 2, AND 3 complete - content, navigation, and quizzes work

---

## Phase 6: User Story 4 - Track Learning Progress (P4)

**Goal**: Students can see their progress, streaks, and completed chapters

**Independent Test**: Can fetch progress summary showing chapters completed, streak, overall percentage

### Implementation for User Story 4

- [ ] T025 [P] [US4] Create progress schemas in backend/app/schemas/progress.py:
  - ChapterProgressStatus (chapter_id, status, started_at, completed_at)
  - ProgressSummary (chapters_completed, chapters_in_progress, overall_percentage, current_streak_days, longest_streak_days, last_activity_date)
  - UpdateProgressRequest (status: 'in_progress' | 'completed')
- [ ] T026 [P] [US4] Create progress service in backend/app/services/progress_service.py:
  - update_chapter_progress(user_id, chapter_id, status) → upserts chapter_progress
  - get_progress_summary(user_id) → aggregates all progress
  - calculate_streak(user_id) → returns (current_streak, longest_streak)
  - Streak algorithm: count consecutive days in daily_activity table
- [ ] T027 [US4] Implement progress router in backend/app/routers/progress.py:
  - GET /progress/{user_id} → returns ProgressSummary
  - PUT /progress/{user_id}/chapter/{chapter_id} → updates chapter status
  - GET /progress/{user_id}/quiz-scores → returns all quiz attempt summaries
  - Enforce auth: users can only access their own progress
- [ ] T028 [US4] Add progress tests in backend/tests/test_progress.py:
  - Test update chapter progress persists to DB
  - Test streak increments for consecutive days
  - Test streak resets when day is missed
  - Test overall_percentage calculation
  - Test users can only access their own progress

**Checkpoint**: User Stories 1-4 complete - content, navigation, quizzes, and progress tracking work

---

## Phase 7: User Story 5 - Ask Content-Grounded Questions (P5)

**Goal**: Students can search course content and get relevant excerpts

**Independent Test**: Can search for terms and receive up to 5 relevant results from accessible chapters

### Implementation for User Story 5

- [ ] T029 [P] [US5] Create search service in backend/app/services/search_service.py:
  - search_chapters(query, user, chapter_id=None) → List[SearchResult]
  - Use PostgreSQL tsvector full-text search
  - Exclude gated chapters for free users
  - Return max 5 results
- [ ] T030 [US5] Implement search router in backend/app/routers/search.py:
  - GET /search?q={query}&chapter_id={optional}
  - Query parameter q is required (422 if missing)
  - Returns list of SearchResult (chapter_id, chapter_title, excerpt, relevance_score)
  - Returns empty array (not error) when no results
- [ ] T031 [US5] Add search tests in backend/tests/test_search.py:
  - Test search uses tsvector (no LLM calls)
  - Test free users don't get results from gated chapters
  - Test search returns empty list for unknown terms
  - Test chapter_id parameter limits search to specific chapter

**Checkpoint**: User Stories 1-5 complete - all core learning features work

---

## Phase 8: User Story 6 - Freemium Access Control (P6)

**Goal**: Platform operators can enforce free vs premium access reliably

**Independent Test**: Free users receive 403 on gated content; premium users can access everything

### Implementation for User Story 6

- [ ] T032 [P] [US6] Create user schemas in backend/app/schemas/user.py:
  - UserResponse (id, email, tier - NEVER api_key)
  - AccessResult (has_access, reason, upgrade_required)
- [ ] T033 [US6] Implement access router in backend/app/routers/access.py:
  - GET /access/check?resource_type={type}&resource_id={id}
  - Returns AccessResult based on user tier and resource
- [ ] T034 [US6] Implement users router in backend/app/routers/users.py:
  - GET /users/me → returns current user info (id, email, tier)
  - NEVER returns api_key
- [ ] T035 [US6] Add access control tests in backend/tests/test_access.py:
  - Test free user accessing chapter 1 → has_access: true
  - Test free user accessing chapter 4 → has_access: false, upgrade_required: true
  - Test premium user accessing any chapter → has_access: true
  - Test user tier cannot be spoofed via request parameters

**Checkpoint**: All 6 user stories complete - full Phase 1 feature set ready

---

## Phase 9: ChatGPT App & Agent Skills

**Purpose**: Create ChatGPT App manifest and Agent Skills for conversational interface

- [ ] T036 Create ChatGPT App manifest in chatgpt-app/openapi.yaml:
  - Valid OpenAPI 3.1 spec
  - Documents all 13 backend endpoints
  - Includes apiKey authentication scheme
  - Includes request/response schemas
- [ ] T037 Create system prompt in chatgpt-app/system-prompt.md:
  - Role: "Course Companion, 24/7 AI tutor for AI Agent Development"
  - Content grounding: "Base explanations on API-retrieved content only"
  - Hallucination guard: "Say 'not covered' if not in content"
  - Freemium behavior: "Explain tiers gracefully when hitting gate"
  - Tone: "Encouraging, patient, adaptive"
  - References 4 SKILL.md files
- [ ] T038 Create Agent Skills in chatgpt-app/skills/:
  - concept-explainer.md (triggers: "explain", "what is", "how does")
  - quiz-master.md (triggers: "quiz", "test me", "practice")
  - socratic-tutor.md (triggers: "help me think", "I'm stuck")
  - progress-motivator.md (triggers: "my progress", "streak", "motivate me")
  - Each skill includes: purpose, triggers, workflow, response templates, key principles, API calls

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, documentation, and compliance checks

- [ ] T039 [P] Create architecture diagram in docs/architecture-diagram.png:
  - Shows User ↔ ChatGPT App ↔ FastAPI Backend ↔ (PostgreSQL, R2) flow
  - Clearly marks Zero-Backend-LLM boundary
- [ ] T040 [P] Create cost analysis in docs/cost-analysis.md:
  - Phase 1 cost breakdown (R2, DB, compute)
  - Target: <$50/month for 10K users
- [ ] T041 Run full test suite: pytest backend/tests/
  - All tests must pass
  - Coverage must be ≥80% on business logic
- [ ] T042 Run Zero-LLM compliance audit:
  - grep -r "openai\|anthropic\|langchain\|llama_index" backend/app/
  - Must return zero results
- [ ] T043 Update README.md with final setup instructions and API reference
- [ ] T044 [CHECKPOINT E] Complete Phase 1 checklist from constitution:
  - Zero LLM calls in backend ✅
  - All 6 features implemented ✅
  - Freemium gate works ✅
  - Progress persists in DB ✅
  - OpenAPI docs at /docs ✅
  - ChatGPT manifest valid ✅
  - All type hints present ✅
  - Tests pass ≥80% coverage ✅

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Foundational)**: Depends on Setup - **BLOCKS all user stories**
- **Phases 3-8 (User Stories)**: All depend on Foundational phase completion
  - Can proceed sequentially (P1 → P2 → P3 → P4 → P5 → P6)
  - Or parallel if team capacity allows
- **Phase 9 (ChatGPT App)**: Depends on all backend APIs being complete
- **Phase 10 (Polish)**: Depends on all features complete

### User Story Dependencies

- **US1 (P1) - Content Delivery**: Can start after Foundational - No dependencies
- **US2 (P2) - Navigation**: Can start after US1 (uses same router)
- **US3 (P3) - Quizzes**: Can start after Foundational - Independent
- **US4 (P4) - Progress**: Can start after Foundational - Independent
- **US5 (P5) - Search**: Can start after Foundational - Independent
- **US6 (P6) - Freemium Gate**: Integrated throughout, but explicit endpoints after Foundational

### Within Each User Story

1. Models (if new ones needed) → Services → Routers → Tests
2. Tasks marked [P] can run in parallel within the story

### Parallel Opportunities

**Phase 1 (Setup)**:
- T002, T003 can run in parallel with T001

**Phase 2 (Foundational)**:
- T005, T006, T007, T008, T009, T010, T011 can ALL run in parallel (different files)

**Phase 3+ (User Stories)**:
- Within each story, [P] tasks can run in parallel
- Different stories can be worked on in parallel by different developers

---

## Parallel Example: Foundational Phase

```bash
# Launch all foundational tasks together:
Task: "Implement Pydantic Settings in backend/app/config.py"
Task: "Implement async engine in backend/app/database.py"
Task: "Create response schemas in backend/app/schemas/common.py"
Task: "Implement auth in backend/app/auth.py"
Task: "Create all models in backend/app/models/"
Task: "Configure Alembic"
Task: "Create test fixtures in backend/tests/conftest.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Content Delivery)
4. **STOP and VALIDATE**: Test content delivery with freemium gate
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 (Content) → Test independently → Deploy/Demo (MVP!)
3. Add US2 (Navigation) → Test independently → Deploy/Demo
4. Add US3 (Quizzes) → Test independently → Deploy/Demo
5. Add US4 (Progress) → Test independently → Deploy/Demo
6. Add US5 (Search) → Test independently → Deploy/Demo
7. Add US6 (Freemium) → Test independently → Deploy/Demo
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Content)
   - Developer B: User Story 3 (Quizzes)
   - Developer C: User Story 4 (Progress)
3. Stories complete and integrate independently
4. Remaining stories (US2, US5, US6) can be assigned as capacity allows

---

## Notes

- [P] tasks = different files, no dependencies - can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at checkpoints to validate before continuing
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- **CRITICAL**: Zero LLM imports in backend - enforce via code review and grep audit

---

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Phase 1 | T001-T004 | Setup (4 tasks) |
| Phase 2 | T005-T011 | Foundational (7 tasks) |
| Phase 3 | T012-T017 | US1: Content Delivery (6 tasks) |
| Phase 4 | T018-T019 | US2: Navigation (2 tasks) |
| Phase 5 | T020-T024 | US3: Quizzes (5 tasks) |
| Phase 6 | T025-T028 | US4: Progress (4 tasks) |
| Phase 7 | T029-T031 | US5: Search (3 tasks) |
| Phase 8 | T032-T035 | US6: Freemium Gate (4 tasks) |
| Phase 9 | T036-T038 | ChatGPT App (3 tasks) |
| Phase 10 | T039-T044 | Polish & Validation (6 tasks) |
| **Total** | **44 tasks** | |

**Ready for implementation!** 🚀
