# Implementation Guidance for AI Agents

**Purpose**: Step-by-step execution instructions for implementing Course Companion FTE Phase 1

**Last Updated**: 2026-03-10
**Branch**: 001-complete-phase-1

---

## Pre-Implementation Checklist

Before writing any code, the AI agent MUST confirm:

- [x] I have read /sp.constitution and understand the Zero-Backend-LLM law
- [x] I have read /sp.spec and understand all 6 feature requirements
- [x] I have read /sp.plan and understand the directory structure and tech stack
- [x] I have read /sp.tasks and understand the task execution order
- [x] I will NOT make any LLM API calls in the backend under any circumstances
- [x] I will stop at each [CHECKPOINT] for human review

---

## Critical Implementation Guards

### Guard 1: LLM Import Prevention

At the top of EVERY backend Python file, add this comment block:

```python
# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.
```

### Guard 2: Answer Key Never Exposed

In `quiz_service.py`, the `get_quiz_questions` function MUST select only:

```python
# NEVER select correct_answer in this query
stmt = select(
    QuizQuestion.id,
    QuizQuestion.question_text,
    QuizQuestion.question_type,
    QuizQuestion.options,
    QuizQuestion.sequence_order
    # QuizQuestion.correct_answer  ← NEVER include this
).where(QuizQuestion.chapter_id == chapter_id)
```

### Guard 3: Access Control in Service Layer

Access control MUST happen in the service layer, not just the router. This ensures it applies even if called from other services.

### Guard 4: User ID from Auth Token

```python
# CORRECT — user_id from authenticated token
@router.get("/progress/{user_id}")
async def get_progress(user_id: UUID, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Cannot access another user's progress")
    ...

# WRONG — never trust user_id from request body
@router.post("/progress")  # ← Don't do this
async def update_progress(body: {"user_id": UUID, ...}):  # ← Never accept user_id in body
    ...
```

### Guard 5: Consistent Response Envelope

Every endpoint response MUST use the `APIResponse[T]` wrapper:

```python
from app.schemas.common import APIResponse

@router.get("/chapters", response_model=APIResponse[ChapterListResponse])
async def list_chapters(...):
    chapters = await chapter_service.get_chapters(...)
    return APIResponse(data=chapters)
```

---

## Execution Protocol

### Step 1: Environment Setup

```bash
# Create project root
mkdir course-companion-fte && cd course-companion-fte

# Initialize Python project
uv init backend
cd backend
uv add fastapi uvicorn[standard] sqlalchemy[asyncio] asyncpg pydantic-settings boto3 alembic python-dotenv

# Dev dependencies
uv add --dev pytest pytest-asyncio httpx

# Initialize Alembic
alembic init alembic
```

### Step 2: Execute Tasks 001–006 (Infrastructure)

**Tasks:**
- T001: Create backend directory structure
- T002: Initialize pyproject.toml
- T003: Create .env.example
- T004: Create README.md
- T005: Implement Pydantic Settings
- T006: Implement async SQLAlchemy engine
- T007: Create standard response schemas
- T008: Implement API key authentication
- T009: Create all SQLAlchemy ORM models
- T010: Configure Alembic and create initial migration
- T011: Create test fixtures

**Deliverables:**
- `backend/app/config.py` - Pydantic Settings class
- `backend/app/database.py` - Async SQLAlchemy engine, session factory
- `backend/app/auth.py` - get_current_user dependency
- `backend/app/schemas/common.py` - APIResponse envelope
- `backend/app/models/` - All ORM models (user, chapter, quiz, progress)
- `backend/alembic/` - Configured for async SQLAlchemy
- `backend/tests/conftest.py` - Test fixtures

**Stop at CHECKPOINT A** - Core Infrastructure Review

### Step 3: Execute Tasks 007–010 (Content Delivery - US1)

**Tasks:**
- T012: Create R2 service
- T013: Create chapter schemas
- T014: Create access service
- T015: Implement chapters router
- T016: Seed course content
- T017: Add integration tests

**Deliverables:**
- `backend/app/services/r2_service.py` - Cloudflare R2 client with LRU cache
- `backend/app/schemas/chapter.py` - Chapter schemas
- `backend/app/services/access_service.py` - Freemium gate logic
- `backend/app/routers/chapters.py` - Content delivery endpoints
- `backend/seed/seed_chapters.py` - Content seeding script
- `backend/tests/test_chapters.py` - Integration tests

**Stop at CHECKPOINT B** - Content Delivery Review

### Step 4: Execute Tasks 011–012 (Search - US5)

**Tasks:**
- T029: Create search service
- T030: Implement search router
- T031: Add search tests

**Deliverables:**
- `backend/app/services/search_service.py` - PostgreSQL full-text search
- `backend/app/routers/search.py` - Search endpoint
- `backend/tests/test_search.py` - Search tests

### Step 5: Execute Tasks 013–016 (Quizzes - US3)

**Tasks:**
- T020: Create quiz schemas
- T021: Create quiz service
- T022: Implement quizzes router
- T023: Seed quiz bank
- T024: Add quiz tests

**Deliverables:**
- `backend/app/schemas/quiz.py` - Quiz schemas
- `backend/app/services/quiz_service.py` - Rule-based grading
- `backend/app/routers/quizzes.py` - Quiz endpoints
- `backend/seed/seed_quizzes.py` - Quiz seeding script
- `backend/tests/test_quizzes.py` - Quiz tests

**Stop at CHECKPOINT C** - Quiz Feature Review

### Step 6: Execute Tasks 017–019 (Progress - US4)

**Tasks:**
- T025: Create progress schemas
- T026: Create progress service
- T027: Implement progress router
- T028: Add progress tests

**Deliverables:**
- `backend/app/schemas/progress.py` - Progress schemas
- `backend/app/services/progress_service.py` - Streak calculation
- `backend/app/routers/progress.py` - Progress endpoints
- `backend/tests/test_progress.py` - Progress tests

### Step 7: Execute Tasks 020–021 (Access Control - US6)

**Tasks:**
- T032: Create user schemas
- T033: Implement access router
- T034: Implement users router
- T035: Add access control tests

**Deliverables:**
- `backend/app/schemas/user.py` - User schemas
- `backend/app/routers/access.py` - Access check endpoint
- `backend/app/routers/users.py` - User info endpoint
- `backend/tests/test_access.py` - Access control tests

**Stop at CHECKPOINT D** - All Features Integration Review

### Step 8: Execute Tasks 022–024 (ChatGPT App)

**Tasks:**
- T036: Create OpenAPI manifest
- T037: Create system prompt
- T038: Create Agent Skills

**Deliverables:**
- `chatgpt-app/openapi.yaml` - ChatGPT App manifest
- `chatgpt-app/system-prompt.md` - System prompt
- `chatgpt-app/skills/` - 4 SKILL.md files

### Step 9: Execute Tasks 025–027 (Quality & Docs)

**Tasks:**
- T039: Create architecture diagram
- T040: Create cost analysis
- T041: Run full test suite
- T042: Run Zero-LLM compliance audit
- T043: Update README
- T044: Complete Phase 1 checklist

**Deliverables:**
- `docs/architecture-diagram.png`
- `docs/cost-analysis.md`
- `README.md` (complete)
- Test coverage report (≥80%)
- Zero-LLM audit results

**Stop at CHECKPOINT E** - Pre-Submission Review

---

## Testing Protocol

After each task group, run:

```bash
# Run tests
cd backend && pytest tests/ -v

# Check coverage
pytest tests/ --cov=app --cov-report=term-missing

# Run Zero-LLM audit
grep -r "openai\|anthropic\|langchain\|llama_index" app/ --include="*.py" && echo "VIOLATION FOUND" || echo "COMPLIANT"
```

---

## Common Pitfalls to Avoid

| Pitfall | Prevention |
|---------|------------|
| Adding `import openai` "just to test" | Re-read Guard 1. There are no exceptions. |
| Forgetting to enforce freemium gate in search | Access service MUST be called in search service |
| Returning `correct_answer` in quiz list | See Guard 2. Always verify with a test. |
| Using in-memory dict for progress storage | Progress MUST use PostgreSQL. See NF requirements. |
| Accepting `user_id` from request body | See Guard 4. Always derive from auth token. |
| Skipping [CHECKPOINT] reviews | Checkpoints exist to prevent rework. Respect them. |
| Making content summaries (violates verbatim rule) | R2 service returns raw Markdown. No processing. |

---

## Task Execution Order

**Follow tasks.md exactly:**

1. **Phase 1 (Setup)**: T001-T004
2. **Phase 2 (Foundational)**: T005-T011
3. **Phase 3 (US1: Content)**: T012-T017
4. **Phase 4 (US2: Navigation)**: T018-T019
5. **Phase 5 (US3: Quizzes)**: T020-T024
6. **Phase 6 (US4: Progress)**: T025-T028
7. **Phase 7 (US5: Search)**: T029-T031
8. **Phase 8 (US6: Freemium)**: T032-T035
9. **Phase 9 (ChatGPT App)**: T036-T038
10. **Phase 10 (Polish)**: T039-T044

**Mark tasks as complete** in `tasks.md` by changing `- [ ]` to `- [X]`

---

## Success Criteria

Implementation is complete when:

- ✅ All 44 tasks marked [X] in tasks.md
- ✅ All tests pass (pytest)
- ✅ Code coverage ≥80%
- ✅ Zero-LLM audit passes (no forbidden imports)
- ✅ All 6 features functional
- ✅ ChatGPT App manifest valid
- ✅ README complete with setup instructions
- ✅ All checkpoints reviewed and approved

---

**Ready to start implementation!** 🚀

**Next Command**: Run `/sp.implement` to begin execution, or manually start with Phase 1 tasks.
