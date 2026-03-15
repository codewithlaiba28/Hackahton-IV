<!--
SYNC IMPACT REPORT
==================
Version change: 2.0.0 → 3.0.0
Modified principles:
  - Added Phase 3 Identity section
  - Added Web App Core Laws (5 rules)
  - Added Frontend Architecture Laws (5 laws)
  - Added Design System Laws (5 laws)
  - Added Performance Standards (Phase 3)
  - Updated Project Identity table (Phase 3 values)
  - Updated Constitution Enforcement Checklist (Phase 3 additions)
Added sections:
  - Phase 3 Identity (complete)
  - Web App Core Laws (5 rules - NON-NEGOTIABLE)
  - Frontend Architecture Laws (FA-01 through FA-05)
  - Design System Laws (DS-01 through DS-05)
  - Performance Standards (5 metrics with targets)
  - Phase 3 Constitution Checklist
Removed sections: None (all Phase 1 and Phase 2 principles preserved)
Templates requiring updates:
  - ✅ .specify/templates/plan-template.md (Constitution Check aligned with Phase 3)
  - ✅ .specify/templates/spec-template.md (Scope constraints include Phase 3)
  - ✅ .specify/templates/tasks-template.md (Task categories include Phase 3 web app tasks)
Follow-up TODOs:
  - TODO(PHASE3_IMPLEMENTATION): Scaffold Next.js 15 App Router project
  - TODO(PHASE3_IMPLEMENTATION): Implement consolidated backend API routing
  - TODO(PHASE3_IMPLEMENTATION): Create admin dashboard components
  - TODO(PHASE3_IMPLEMENTATION): Implement NextAuth.js v5 authentication
  - TODO(README_UPDATE): Add Phase 3 web app setup instructions to README.md
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

## Phase 3: Full-Stack Web Application Layer

### XIII. Phase 3 Identity Law (NON-NEGOTIABLE)
Phase 3 ADDS a standalone web application. All Phase 1 and Phase 2 principles remain fully in force.

**RULE ONE**: The web app is a STANDALONE product.
          It does NOT depend on ChatGPT. It is fully self-contained.

**RULE TWO**: All Phase 1 and Phase 2 backend APIs remain unchanged.
          The consolidated backend ADDS unified routing. It does not rewrite.

**RULE THREE**: The web frontend must be fully responsive.
            Desktop (1440px), Tablet (768px), Mobile (375px) — all must work perfectly.

**RULE FOUR**: The freemium gate is enforced on the frontend AND backend.
           Frontend shows locked UI; backend enforces access. Both layers must agree.

**RULE FIVE**: The web app must have a public-facing landing page.
           Unauthenticated visitors must see a marketing page that converts to sign-ups.

**Phase 3 Technology Stack** (MANDATORY):
- Frontend: Next.js 15 (App Router) + React 19
- Styling: Tailwind CSS v4 + shadcn/ui
- Backend: Consolidated FastAPI (Phase 1 + Phase 2 APIs unified)
- Auth: NextAuth.js v5 (JWT strategy)
- Deployment: Vercel (frontend) + Fly.io (backend)

### XIV. Frontend Architecture Laws (Phase 3 - NON-NEGOTIABLE)

**FA-01: App Router Only**
Use Next.js 15 App Router exclusively. No Pages Router. All pages are Server Components by default; use "use client" only when interactivity is required.

**FA-02: Server-Side Data Fetching**
All initial data fetching happens in Server Components (using fetch with proper caching). Client Components only for interactive state (quiz taking, real-time progress).

**FA-03: Route Protection**
All authenticated routes use Next.js middleware for protection. No route can be accessed without valid session — redirect to /login.

**FA-04: Optimistic UI**
Progress updates and quiz submissions use optimistic updates (React 19 useOptimistic). Never block the UI waiting for API responses for non-critical updates.

**FA-05: Zero Broken States**
Every page must handle: loading state, empty state, error state, and success state. No blank white screens.

### XV. Design System Laws (Phase 3 - NON-NEGOTIABLE)

**DS-01: Dark-First Theme**
The primary theme is dark (background: near-black #0A0A0A). A light mode toggle is optional bonus. Dark theme is mandatory.

**DS-02: Design Token Consistency**
All colors, spacing, typography, and border radius values must be defined as CSS variables / Tailwind config. No hardcoded values in components.

**DS-03: Component Library**
Use shadcn/ui as the base component library. All custom components extend shadcn primitives.

**DS-04: Typography Hierarchy**
Three font roles only:
- Display: dramatic heading font (e.g., Sora, Outfit, or Clash Display)
- Body: readable body font (e.g., DM Sans, Plus Jakarta Sans)
- Mono: code font (JetBrains Mono)

**DS-05: Accessibility**
All interactive elements must be keyboard-navigable. All images must have alt text. Color contrast ratio ≥ 4.5:1 for body text.

### XVI. Performance Standards (Phase 3)

| Metric | Target |
|--------|--------|
| Lighthouse Performance | ≥ 90 |
| Lighthouse Accessibility | ≥ 95 |
| First Contentful Paint | < 1.5s |
| Time to Interactive | < 3.0s |
| Core Web Vitals (LCP) | < 2.5s |

**Enforcement Method**: Lighthouse CI integration + manual audit before Phase 3 submission.

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

### DS-06: Phase 3 Documentation
- Web app README with setup instructions for Next.js frontend
- Architecture diagram must show Phase 3 web app integration
- Performance audit results (Lighthouse scores) must be documented
- Responsive design testing results (375px, 768px, 1440px)

---

## Project Identity

| Field | Phase 1 Value | Phase 2 Value | Phase 3 Value |
|-------|---------------|---------------|---------------|
| **Project Name** | Course Companion FTE (Digital Full-Time Equivalent Tutor) | Course Companion FTE — Hybrid Intelligence Layer | Course Companion FTE — Full-Stack Web Application |
| **Phase** | Phase 1 — Zero-Backend-LLM Architecture | Phase 2 — Selective Hybrid Intelligence (Premium Only) | Phase 3 — Standalone End-to-End Web App |
| **Hackathon** | Panaversity Agent Factory Hackathon IV | Panaversity Agent Factory Hackathon IV | Panaversity Agent Factory Hackathon IV |
| **Course Topic** | AI Agent Development (Option A) | AI Agent Development (Option A) | AI Agent Development (Option A) |
| **Target Users** | Students learning AI Agent Development | Students learning AI Agent Development | Students learning AI Agent Development |
| **Primary Frontend** | ChatGPT App (OpenAI Apps SDK) | ChatGPT App (OpenAI Apps SDK) — unchanged | Next.js 15 Web App (App Router) + ChatGPT App |
| **Backend Language** | Python (FastAPI) | Python (FastAPI) — unchanged | Python (FastAPI) — consolidated |
| **Content Storage** | Cloudflare R2 | Cloudflare R2 — unchanged | Cloudflare R2 — unchanged |
| **New Backend** | — | FastAPI + Selective LLM API calls (Claude Sonnet) | Consolidated FastAPI (unified routing) |
| **LLM Provider** | — | Anthropic Claude (claude-sonnet-4-20250514) | Anthropic Claude (claude-sonnet-4-20250514) |
| **Hybrid Features** | — | Maximum 2 (chosen from 4 allowed options) | Maximum 2 (unchanged from Phase 2) |
| **Selected Features** | — | Feature A: Adaptive Learning Path + Feature B: LLM-Graded Assessments | Feature A + Feature B (unchanged) |
| **Authentication** | API Key | API Key | NextAuth.js v5 (JWT) + API Key |
| **Deployment** | Fly.io (backend only) | Fly.io (backend only) | Vercel (frontend) + Fly.io (backend) |
| **Builds On** | — | Phase 1 (Zero-Backend-LLM) | Phase 1 + Phase 2 |

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

### Phase 3 Checklist (ADDITIONAL)

Before final submission, a reviewer MUST verify:

- [ ] Landing page renders correctly and converts to sign-up
- [ ] All 6 Phase 1 features accessible via web UI
- [ ] Both Phase 2 premium features accessible via web UI (with gate)
- [ ] Freemium gate works: free user sees locked content UI
- [ ] Fully responsive (test at 375px, 768px, 1440px)
- [ ] All pages have loading, empty, and error states
- [ ] Authentication works (register, login, logout, session persistence)
- [ ] Progress dashboard shows real data
- [ ] Quiz flow is complete (start → answer → submit → result)
- [ ] Phase 1 and Phase 2 backend APIs unchanged
- [ ] Lighthouse Performance score ≥ 90
- [ ] Lighthouse Accessibility score ≥ 95
- [ ] NextAuth.js middleware protects all authenticated routes
- [ ] Dark theme is default and primary

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
- **PATCH**: Clarifications, wording improvements, typo fixes, non-semantic refinements

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

**Phase 3 Specific Governance**:
- Web app must maintain Lighthouse scores throughout development
- Design token changes must be backward compatible
- Route protection middleware must be tested on every PR
- Performance regression >10% requires immediate remediation

---

**Version**: 3.0.0 | **Ratified**: 2026-03-10 | **Last Amended**: 2026-03-12

**Phase 1**: Zero-Backend-LLM Architecture ✅ COMPLETE

**Phase 2**: Hybrid Intelligence Layer ✅ COMPLETE

**Phase 3**: Full-Stack Web Application 🎯 IN PROGRESS
