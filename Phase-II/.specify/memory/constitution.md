<!--
SYNC IMPACT REPORT
==================
Version change: 1.0.0 → 2.0.0
Modified principles:
  - Added Phase 2 Identity section
  - Added Hybrid Selectivity Law (ABSOLUTE - Phase 2 critical)
  - Added Architectural Separation Law (Phase 2)
  - Added Cost Control Standards (Phase 2)
  - Added LLM Quality Standards (Phase 2)
  - Added Premium Gate Enforcement (Phase 2)
  - Updated Project Identity table (Phase 2 values)
  - Updated Constitution Enforcement Checklist (Phase 2 additions)
Added sections:
  - Phase 2 Identity (complete)
  - The Hybrid Selectivity Law (5 rules - NON-NEGOTIABLE)
  - Architectural Separation Law (Phase 2)
  - Cost Control Standards (4 standards)
  - LLM Quality Standards (5 standards)
  - Premium Gate Enforcement (3 standards)
  - Phase 2 Constitution Checklist
Removed sections: None (all Phase 1 principles preserved)
Templates requiring updates:
  - ✅ .specify/templates/plan-template.md (Constitution Check aligned with Phase 2)
  - ✅ .specify/templates/spec-template.md (Scope constraints include Phase 2)
  - ✅ .specify/templates/tasks-template.md (Task categories include Phase 2)
  - ⚠ .specify/templates/commands/sp.constitution.toml (this file - review needed)
Follow-up TODOs:
  - TODO(PHASE2_IMPLEMENTATION): Implement adaptive_learning.py router
  - TODO(PHASE2_IMPLEMENTATION): Implement assessments.py router
  - TODO(PHASE2_IMPLEMENTATION): Create llm_usage database table
  - TODO(PHASE2_IMPLEMENTATION): Implement cost_tracker service
  - TODO(README_UPDATE): Add Phase 2 constitution reference to README.md
  - TODO(TEMPLATE_SYNC): Update command templates to reference Phase 2 constraints
-->

# Course Companion FTE Constitution

## Core Principles

### I. Zero-Backend-LLM Law (NON-NEGOTIABLE)
This is the most critical rule of Phase 1. Violation results in immediate disqualification.

**RULE ZERO**: The FastAPI backend MUST NOT make any LLM API calls.
No exceptions. No workarounds. No "just one call".

**Explicitly Forbidden in Backend**:
- Any call to OpenAI, Anthropic, Cohere, Groq, or any LLM provider
- RAG summarization pipelines
- Prompt orchestration logic
- LangChain, LlamaIndex, or any LLM framework integration
- Content generation using AI
- Agent loops or reasoning chains
- Embedding generation for semantic meaning (keyword/vector search for retrieval is allowed; LLM-based reranking is not)

**Enforcement Method**: Code review + automated grep scan for `openai.`, `anthropic.`, `langchain`, `llama_index`, `claude`, `gpt-4`, `chat.completions` in all backend files.

**The Correct Mental Model**:
```
User ↔ ChatGPT App (ALL intelligence lives here) ↔ Deterministic Backend (data only)
```

### II. Determinism Over Intelligence
Every backend endpoint MUST produce identical output for identical input. No probabilistic behavior.

**Requirements**:
- All business logic must be rule-based and deterministic
- Database queries must return consistent results for same parameters
- No random number generation in production code without explicit seeding
- Caching behavior must be predictable and documented

### III. Content Verbatim Delivery
When serving course content, serve it exactly as stored in Cloudflare R2. No paraphrasing, no summarizing, no reformatting beyond JSON wrapping.

**Requirements**:
- Content retrieved from R2 must be delivered unchanged
- Markdown formatting must be preserved
- Code blocks, lists, and images must maintain structure
- Only allowed transformation: JSON envelope wrapping

### IV. ChatGPT is the Brain
ChatGPT handles: explanation, tutoring, encouragement, tone adaptation, analogy creation, concept simplification, and all natural language generation. The backend is a dumb data store with rules.

**Backend Responsibilities**:
- Serve content verbatim from R2
- Track progress and streaks
- Grade quizzes (rule-based)
- Enforce access control
- Search content (keyword/embedding)

**ChatGPT Responsibilities**:
- Explain concepts at learner's level
- Provide analogies and examples
- Answer questions from content
- Encourage and motivate
- Adapt tone to student

### V. Progress Persistence
All student progress (chapter completions, quiz scores, streaks) MUST persist in a real database (Neon/Supabase PostgreSQL). In-memory storage is not acceptable.

**Requirements**:
- PostgreSQL database required (Neon or Supabase)
- All progress data must survive server restarts
- Session state may be in-memory, but progress must be in database
- Database schema must be versioned and migrated

### VI. Single Responsibility Per Endpoint
Each API endpoint does exactly one thing. No endpoint mixes content serving with progress tracking or quiz grading.

**Requirements**:
- Each endpoint has one clear purpose
- No side effects beyond stated purpose
- Endpoints are independently testable
- Clear separation of concerns

### VII. Freemium Enforcement at Data Layer
Access control is enforced in the backend. ChatGPT App never bypasses access control by directly constructing content. It always requests through authenticated endpoints.

**Requirements**:
- All content endpoints check access tier
- Free tier limited to chapters 1-3
- Premium/Pro features gated by database flags
- Access control logic is tested and auditable

---

## Phase 2: Hybrid Intelligence Layer

### VIII. The Hybrid Selectivity Law (ABSOLUTE - NON-NEGOTIABLE)
This is the most critical rule of Phase 2. Violation results in immediate disqualification.

**RULE ONE**: Hybrid (LLM) features are ONLY allowed for premium users.
          Free users NEVER trigger backend LLM calls. Ever.

**RULE TWO**: Hybrid features must be USER-INITIATED.
          The backend NEVER auto-triggers LLM calls on its own.

**RULE THREE**: Maximum 2 hybrid features total.
            Adding a 3rd hybrid feature = disqualification.

**RULE FOUR**: Phase 1 APIs remain unchanged.
           No existing Phase 1 endpoint may be modified to include LLM calls.
           Hybrid features live in NEW, ISOLATED API routes only.

**RULE FIVE**: Every LLM call must be cost-tracked.
           Token usage logged per user per request. No exceptions.

**Explicitly Allowed in Phase 2 Backend**:
- LLM API calls to Anthropic Claude (claude-sonnet-4-20250514) in isolated routes ONLY
- Adaptive Learning Path generation (Feature A)
- LLM-Graded Assessments (Feature B)
- Cross-chapter synthesis (optional Feature C, if not using A or B)

**Enforcement Method**: Code review + git diff on Phase 1 files (must show zero changes) + llm_usage table audit.

**The Correct Mental Model for Phase 2**:
```
User ↔ ChatGPT App ↔ Backend
                       ├─ Deterministic APIs (Phase 1 - ZERO LLM)
                       └─ Hybrid Intelligence APIs (Phase 2 - LLM calls, premium only)
```

### IX. Architectural Separation Law (Phase 2 - NON-NEGOTIABLE)
The codebase MUST clearly separate Phase 1 and Phase 2 logic:

```
backend/app/routers/
  ├── chapters.py        ← Phase 1 (NO changes allowed)
  ├── search.py          ← Phase 1 (NO changes allowed)
  ├── quizzes.py         ← Phase 1 (NO changes allowed)
  ├── progress.py        ← Phase 1 (NO changes allowed)
  ├── access.py          ← Phase 1 (NO changes allowed)
  ├── users.py           ← Phase 1 (NO changes allowed)
  │
  ├── adaptive_path.py   ← Phase 2 ONLY (new file)
  └── assessments.py     ← Phase 2 ONLY (new file)
```

**Detection Method**: Code review confirms zero modifications to Phase 1 files. Git diff on Phase 1 files must show no changes except import additions if strictly necessary.

**API Routing Standards**:
- Phase 1 endpoints: `/api/v1/...` or `/chapters`, `/quizzes`, etc.
- Phase 2 endpoints: `/api/v2/...` (clearly versioned and separated)
- Phase 2 routers must be in separate files (no mixing with Phase 1 code)

**Service Layer Separation**:
- `app/services/llm_service.py` - LLM client wrapper (Phase 2 only)
- `app/services/cost_tracker.py` - Usage tracking (Phase 2 only)
- Phase 1 services remain unchanged (r2_service, quiz_service, progress_service, access_service)

### X. Cost Control Standards (Phase 2)

**CC-01: Per-Request Cost Ceiling**

- Adaptive Learning Path: max $0.05 per request
- LLM Assessment: max $0.03 per request
- If estimated tokens exceed ceiling, truncate context, do NOT exceed

**CC-02: Per-User Monthly Cost Cap**

- Premium users: max $2.00/month in hybrid LLM costs
- If cap reached, gracefully downgrade to zero-LLM fallback for that user
- Pro tier users: max $5.00/month (included in tier price)

**CC-03: Cost Logging**

Every LLM call MUST log to `llm_usage` table:
- user_id
- feature_name
- model
- input_tokens
- output_tokens
- cost_usd
- timestamp

**CC-04: Cost Transparency**

`GET /users/me/cost-summary` endpoint must show users their current month's hybrid feature usage cost.

### XI. LLM Quality Standards (Phase 2)

**LQ-01: Grounding Required**

All LLM calls must include relevant course content as context. LLM must not rely on its own training knowledge for course-specific answers.

**LQ-02: Hallucination Guards**

Every LLM system prompt must include: "Base all recommendations and feedback strictly on the provided course content and student data. Do not invent course topics, chapters, or concepts not present in the provided context."

**LQ-03: Structured Output**

All LLM calls must request structured JSON output. Raw unstructured LLM text must never be returned directly to the ChatGPT App.

**LQ-04: Fallback on LLM Failure**

If LLM call fails (timeout, API error, rate limit), the endpoint MUST return a graceful fallback response — never a 500 error exposed to the user.

Example fallback:
```json
{
  "error": "LLM_UNAVAILABLE",
  "message": "AI analysis temporarily unavailable. Please try again in a moment.",
  "fallback": "Standard recommendations available instead."
}
```

**LQ-05: Model Version Pinned**

Always use `claude-sonnet-4-20250514`. Never use a floating model alias. Model must be configurable via environment variable with this as default.

### XII. Premium Gate Enforcement (Phase 2)

**PG-01: Tier Check First**

Every Phase 2 endpoint must check `user.tier == "premium"` or `user.tier == "pro"` BEFORE making any LLM call.

**PG-02: Clear Upgrade Message**

Free users hitting Phase 2 endpoints receive:
```json
{
  "error": "PREMIUM_REQUIRED",
  "message": "Adaptive learning paths are a premium feature. Upgrade to access.",
  "upgrade_url": "/upgrade"
}
```

**PG-03: No Partial Access**

There is no "trial" or "preview" of hybrid features for free users. It is binary: premium = full access, free = no access.

---

## Code Quality Standards

### CQ-01: Python Standards
- Python 3.12+ with full type annotations on all functions
- Pydantic v2 for all request/response models
- No `Any` type hints unless absolutely unavoidable (must be commented)
- All functions must have docstrings

### CQ-02: API Standards
- All endpoints follow RESTful conventions
- All responses are JSON with consistent envelope: `{ "data": ..., "error": null, "meta": {...} }`
- HTTP status codes must be semantically correct (200, 201, 400, 401, 403, 404, 422, 500)
- All endpoints documented via FastAPI's built-in OpenAPI

### CQ-03: Error Handling
- All endpoints must handle and return structured errors
- Never expose internal stack traces to the client
- All database errors must be caught and wrapped

### CQ-04: Security
- All student-specific endpoints require authentication (API key or JWT)
- User IDs are never accepted from the request body — always derive from auth token
- Rate limiting on all public endpoints

### CQ-05: Testing
- Unit tests required for quiz grading logic
- Unit tests required for freemium access control logic
- Unit tests required for Phase 2 premium gate logic
- Integration tests for all 6 required features (Phase 1)
- Integration tests for both hybrid features (Phase 2)
- Minimum 80% code coverage on backend business logic

---

## Educational Content Standards

### EC-01: Course Topic
All content must be about AI Agent Development covering: Claude Agent SDK, MCP (Model Context Protocol), Agent Skills, and the Agent Factory Architecture.

### EC-02: Content Structure
Each chapter must have:
- A unique ID (e.g., `ch-001`)
- A title, difficulty level, and estimated read time
- Body content in Markdown
- At least 3 quiz questions with answer keys
- Previous/next chapter navigation pointers

### EC-03: Quiz Integrity
Quiz grading is rule-based only. The backend compares submitted answers against a stored answer key. No partial credit logic that requires reasoning.

### EC-04: Freemium Gate
- **Free tier**: Chapters 1–3 only, basic quizzes
- **Premium tier**: All chapters, all quizzes, progress analytics
- **Pro tier**: Premium + Adaptive Learning Path + LLM-Graded Assessments

---

## Delivery Standards

### DS-01: README Completeness
The README must contain: project overview, local setup instructions, environment variables list, API documentation link, and architecture diagram.

### DS-02: OpenAPI Documentation
All endpoints must appear in `/docs` with request/response examples.

### DS-03: Environment Configuration
All secrets (DB URLs, R2 credentials, API keys) must be in `.env` and never committed. A `.env.example` must be committed.

### DS-04: ChatGPT App Manifest
A valid `openapi.yaml` manifest must be provided for ChatGPT App registration.

### DS-05: Phase 2 Documentation
- Cost analysis document must include Phase 2 hybrid feature costs
- Architecture diagram must show Phase 1 vs Phase 2 separation
- API documentation must clearly mark premium endpoints

---

## Project Identity

| Field | Phase 1 Value | Phase 2 Value |
|-------|---------------|---------------|
| **Project Name** | Course Companion FTE (Digital Full-Time Equivalent Tutor) | Course Companion FTE — Hybrid Intelligence Layer |
| **Phase** | Phase 1 — Zero-Backend-LLM Architecture | Phase 2 — Selective Hybrid Intelligence (Premium Only) |
| **Hackathon** | Panaversity Agent Factory Hackathon IV | Panaversity Agent Factory Hackathon IV |
| **Course Topic** | AI Agent Development (Option A) | AI Agent Development (Option A) |
| **Target Users** | Students learning AI Agent Development | Students learning AI Agent Development |
| **Primary Frontend** | ChatGPT App (OpenAI Apps SDK) | ChatGPT App (OpenAI Apps SDK) — unchanged |
| **Backend Language** | Python (FastAPI) | Python (FastAPI) — unchanged |
| **Content Storage** | Cloudflare R2 | Cloudflare R2 — unchanged |
| **New Backend** | — | FastAPI + Selective LLM API calls (Claude Sonnet) |
| **LLM Provider** | — | Anthropic Claude (claude-sonnet-4-20250514) |
| **Hybrid Features** | — | Maximum 2 (chosen from 4 allowed options) |
| **Selected Features** | — | Feature A: Adaptive Learning Path + Feature B: LLM-Graded Assessments |

---

## Constitution Enforcement Checklist

### Phase 1 Checklist (UNCHANGED)

Before advancing from Phase 1, a reviewer MUST verify:

- [ ] Zero LLM calls in backend (automated grep scan passes)
- [ ] All 6 required features implemented and tested
- [ ] Freemium gate works correctly
- [ ] Progress persists across sessions (database, not memory)
- [ ] OpenAPI docs generated and accessible
- [ ] ChatGPT App manifest valid
- [ ] All type hints present
- [ ] Tests pass with ≥80% coverage

### Phase 2 Checklist (ADDITIONAL)

Before advancing to Phase 3, a reviewer MUST verify:

- [ ] Phase 1 files unchanged (git diff confirms zero modifications)
- [ ] Exactly 2 hybrid features implemented (no more, no less)
- [ ] Both features are premium-gated (test with free user token → 403)
- [ ] Both features are user-initiated (no auto-triggers in code)
- [ ] `llm_usage` table populated after every LLM call
- [ ] Cost tracking accessible via `/users/me/cost-summary`
- [ ] LLM fallback works when API is unavailable (mock test)
- [ ] All LLM responses are structured JSON (not raw text)
- [ ] Cost justification document submitted
- [ ] Architecture diagram shows Phase 1 vs Phase 2 separation

---

## Governance

**Constitution Supremacy**: This constitution supersedes all other practices and guidelines in the project. Any artifact that violates these principles must be rejected and regenerated.

**Amendment Process**:
1. Propose amendment with rationale
2. Document impact on existing features
3. Update version according to semantic versioning
4. All team members must acknowledge change
5. Update dependent templates and documentation

**Versioning Policy**:
- **MAJOR**: Backward incompatible changes (removing principles, redefining core laws)
- **MINOR**: New principles added or existing principles expanded
- **PATCH**: Clarifications, wording improvements, typo fixes

**Compliance Review**:
- All PRs must be reviewed for constitution compliance
- Automated checks where possible (grep scans, test coverage)
- Manual review for architectural principles
- Non-compliant code must be refactored before merge

**Phase 2 Specific Governance**:
- Hybrid feature usage must be reviewed weekly for cost optimization
- LLM API costs must be tracked per user per month
- Premium gate bypass attempts must be logged and alerted
- Phase 1 constitution remains fully in force — Phase 2 ADDS constraints, does not replace

---

**Version**: 2.0.0 | **Ratified**: 2026-03-10 | **Last Amended**: 2026-03-11

**Phase 1**: Zero-Backend-LLM Architecture ✅ COMPLETE

**Phase 2**: Hybrid Intelligence Layer 🎯 IN PROGRESS
