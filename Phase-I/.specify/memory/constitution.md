<!--
SYNC IMPACT REPORT
==================
Version change: [TEMPLATE] → 1.0.0
Modified principles: All (template → concrete values)
Added sections:
  - Project Identity (complete)
  - Zero-Backend-LLM Law (Phase 1 critical)
  - Architectural Principles (7 principles)
  - Code Quality Standards (5 standards)
  - Educational Content Standards (4 standards)
  - Delivery Standards (4 standards)
  - Constitution Enforcement Checklist
Templates requiring updates:
  - ✅ .specify/templates/plan-template.md (Constitution Check aligned)
  - ✅ .specify/templates/spec-template.md (Scope constraints aligned)
  - ✅ .specify/templates/tasks-template.md (Task categories aligned)
  - ⚠ .specify/templates/commands/sp.constitution.toml (this file - review needed)
Follow-up TODOs:
  - TODO(TEMPLATE_SYNC): Update command templates to reference Phase 1 constraints
  - TODO(README_UPDATE): Add constitution reference to README.md
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
- Integration tests for all 6 required features
- Minimum 80% code coverage on backend business logic

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

## Delivery Standards

### DS-01: README Completeness
The README must contain: project overview, local setup instructions, environment variables list, API documentation link, and architecture diagram.

### DS-02: OpenAPI Documentation
All endpoints must appear in `/docs` with request/response examples.

### DS-03: Environment Configuration
All secrets (DB URLs, R2 credentials, API keys) must be in `.env` and never committed. A `.env.example` must be committed.

### DS-04: ChatGPT App Manifest
A valid `openapi.yaml` manifest must be provided for ChatGPT App registration.

## Project Identity

| Field | Value |
|-------|-------|
| **Project Name** | Course Companion FTE (Digital Full-Time Equivalent Tutor) |
| **Phase** | Phase 1 — Zero-Backend-LLM Architecture |
| **Hackathon** | Panaversity Agent Factory Hackathon IV |
| **Course Topic** | AI Agent Development (Option A) |
| **Target Users** | Students learning AI Agent Development |
| **Primary Frontend** | ChatGPT App (OpenAI Apps SDK) |
| **Backend Language** | Python (FastAPI) |
| **Content Storage** | Cloudflare R2 |

## Constitution Enforcement Checklist

Before advancing from Phase 1, a reviewer MUST verify:

- [ ] Zero LLM calls in backend (automated grep scan passes)
- [ ] All 6 required features implemented and tested
- [ ] Freemium gate works correctly
- [ ] Progress persists across sessions (database, not memory)
- [ ] OpenAPI docs generated and accessible
- [ ] ChatGPT App manifest valid
- [ ] All type hints present
- [ ] Tests pass with ≥80% coverage

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

**Version**: 1.0.0 | **Ratified**: 2026-03-10 | **Last Amended**: 2026-03-10
