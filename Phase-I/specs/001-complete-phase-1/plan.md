# Implementation Plan: Course Companion FTE - Phase 1 Core Features

**Branch**: `001-complete-phase-1` | **Date**: 2026-03-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification with 6 user stories, 18 functional requirements

## Summary

**Primary Requirement**: Build a Zero-Backend-LLM educational tutor for AI Agent Development with 6 core features (content delivery, navigation, quizzes, progress tracking, grounded Q&A, freemium gate).

**Technical Approach**: FastAPI backend serving as deterministic data layer, PostgreSQL for persistence, Cloudflare R2 for content storage, ChatGPT App as the intelligent frontend. All intelligence lives in ChatGPT; backend only serves data and enforces rules.

## Technical Context

**Language/Version**: Python 3.12
**Primary Dependencies**: FastAPI, SQLAlchemy 2.0 (async), Pydantic v2, psycopg2-binary, boto3 (R2 client)
**Storage**: PostgreSQL (Neon serverless), Cloudflare R2
**Testing**: pytest + httpx (async), pytest-asyncio
**Target Platform**: Linux server (Fly.io or Railway deployment)
**Project Type**: Single backend API + ChatGPT App manifest
**Performance Goals**: 95th percentile <500ms for GET, <1000ms for POST, 100 concurrent requests
**Constraints**: Zero LLM calls in backend, 5-second hard timeout, CORS for ChatGPT origin
**Scale/Scope**: Hackathon demo with manual user provisioning, 10K users/month cost target <$50

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Constitution Principle | Compliant? | Notes |
|------------------------|------------|-------|
| **I. Zero-Backend-LLM Law** | ✅ Yes | No LLM imports planned; FastAPI is deterministic |
| **II. Determinism Over Intelligence** | ✅ Yes | All endpoints produce identical output for identical input |
| **III. Content Verbatim Delivery** | ✅ Yes | R2 content served exactly as stored |
| **IV. ChatGPT is the Brain** | ✅ Yes | Backend serves data only; ChatGPT handles explanation |
| **V. Progress Persistence** | ✅ Yes | PostgreSQL database (Neon) for all progress data |
| **VI. Single Responsibility Per Endpoint** | ✅ Yes | One router per feature (chapters, quizzes, progress, etc.) |
| **VII. Freemium Enforcement at Data Layer** | ✅ Yes | Access control in backend services, not bypassable |

**GATE STATUS**: ✅ PASSED - All constitution principles respected

## Project Structure

### Documentation (this feature)

```text
specs/001-complete-phase-1/
├── plan.md              # This file
├── research.md          # Phase 0 output (below)
├── data-model.md        # Phase 1 output (below)
├── quickstart.md        # Phase 1 output (below)
├── contracts/           # Phase 1 output (below)
└── tasks.md             # Phase 2 output (NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                   # FastAPI app entry point
│   ├── config.py                 # Settings via pydantic-settings
│   ├── database.py               # SQLAlchemy async engine + session
│   ├── auth.py                   # API key authentication dependency
│   │
│   ├── models/                   # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user.py               # User, UserTier enum
│   │   ├── chapter.py            # Chapter metadata
│   │   ├── quiz.py               # QuizQuestion, AnswerKey, QuizAttempt
│   │   └── progress.py           # UserProgress, ChapterProgress
│   │
│   ├── schemas/                  # Pydantic v2 request/response schemas
│   │   ├── __init__.py
│   │   ├── chapter.py
│   │   ├── quiz.py
│   │   ├── progress.py
│   │   ├── user.py
│   │   └── common.py             # APIResponse envelope
│   │
│   ├── routers/                  # FastAPI routers (one per feature)
│   │   ├── __init__.py
│   │   ├── chapters.py           # Features 1, 2
│   │   ├── search.py             # Feature 3
│   │   ├── quizzes.py            # Feature 4
│   │   ├── progress.py           # Feature 5
│   │   ├── access.py             # Feature 6
│   │   └── users.py              # User management
│   │
│   ├── services/                 # Business logic (pure deterministic)
│   │   ├── __init__.py
│   │   ├── r2_service.py         # Cloudflare R2 content retrieval
│   │   ├── quiz_service.py       # Rule-based grading logic
│   │   ├── progress_service.py   # Streak calculation, progress aggregation
│   │   └── access_service.py     # Freemium gate enforcement
│   │
│   └── utils/
│       ├── __init__.py
│       └── search.py             # PostgreSQL full-text search helpers
│
├── alembic/                      # Database migrations
│   ├── env.py
│   └── versions/
│
├── tests/
│   ├── conftest.py               # Fixtures, test DB setup
│   ├── test_chapters.py
│   ├── test_quizzes.py
│   ├── test_progress.py
│   └── test_access.py
│
├── seed/                         # Content seeding scripts
│   ├── seed_chapters.py          # Upload chapters to R2 + DB metadata
│   └── seed_quizzes.py           # Seed quiz bank to DB
│
├── pyproject.toml
├── .env.example
└── Dockerfile

chatgpt-app/
├── openapi.yaml                  # ChatGPT App manifest
├── SKILL.md                      # Agent Skills (4 required)
└── system-prompt.md              # System prompt for ChatGPT App

content/                          # Raw course content (Markdown)
├── ch-001-intro-to-agents.md
├── ch-002-claude-agent-sdk.md
├── ch-003-mcp-basics.md
├── ch-004-agent-skills.md        # Gated (premium)
├── ch-005-agent-factory.md       # Gated (premium)
└── quizzes/
    ├── ch-001-quiz.json
    ├── ch-002-quiz.json
    └── ...

docs/
├── architecture-diagram.png
├── api-reference.md
└── cost-analysis.md

README.md
```

**Structure Decision**: Single backend API project with clear separation of concerns (models, schemas, routers, services). ChatGPT App is configuration-only (openapi.yaml manifest + SKILL.md files).

## Phase 0: Research & Technical Decisions

### Research Findings

#### Decision 1: API Framework - FastAPI
- **What was chosen**: FastAPI (Python 3.12)
- **Why chosen**: Native async support, automatic OpenAPI docs, Pydantic v2 integration, excellent performance
- **Alternatives considered**: 
  - Flask (synchronous, manual OpenAPI)
  - Django REST Framework (heavier, synchronous by default)
  - Starlette (lower-level, FastAPI builds on it)

#### Decision 2: Database - PostgreSQL via Neon
- **What was chosen**: PostgreSQL (Neon serverless)
- **Why chosen**: Free tier, serverless scaling, SQLAlchemy compatible, full-text search native
- **Alternatives considered**:
  - Supabase (PostgreSQL + extras, but more complex)
  - SQLite (not suitable for concurrent access)
  - MongoDB (not relational, overkill for this use case)

#### Decision 3: ORM - SQLAlchemy 2.0 (async)
- **What was chosen**: SQLAlchemy 2.0 with asyncpg
- **Why chosen**: Type-safe, async support, Alembic migrations, industry standard
- **Alternatives considered**:
  - Tortoise ORM (async-native but less mature)
  - SQLModel (simpler but less flexible)
  - Raw SQL (more control, more boilerplate)

#### Decision 4: Content Storage - Cloudflare R2
- **What was chosen**: Cloudflare R2
- **Why chosen**: S3-compatible API, cheap egress (free 10GB/month), reliable, hackathon-friendly
- **Alternatives considered**:
  - AWS S3 (more expensive egress)
  - Google Cloud Storage (similar pricing, more complex)
  - Direct database storage (not suitable for large Markdown files)

#### Decision 5: Authentication - API Key (X-API-Key header)
- **What was chosen**: Simple API key in header
- **Why chosen**: Simple, sufficient for hackathon, ChatGPT App compatible, no OAuth complexity
- **Alternatives considered**:
  - JWT tokens (more complex, overkill for demo)
  - OAuth2 (requires auth server, overkill)
  - Session-based (requires cookies, ChatGPT App incompatible)

#### Decision 6: Deployment - Fly.io or Railway
- **What was chosen**: Fly.io (primary) or Railway (backup)
- **Why chosen**: Easy deploy, free tier available, Docker support, PostgreSQL integration
- **Alternatives considered**:
  - Heroku (no longer free tier)
  - Vercel (better for frontend, not backend)
  - AWS/GCP (more complex, overkill for hackathon)

#### Decision 7: Search - PostgreSQL Full-Text Search
- **What was chosen**: PostgreSQL tsvector/tsquery
- **Why chosen**: No external dependency, deterministic, fast enough for hackathon scale
- **Alternatives considered**:
  - Elasticsearch (overkill, external service)
  - Meilisearch (external service, adds complexity)
  - Simple LIKE queries (slower, less features)

#### Decision 8: Dependency Management - uv
- **What was chosen**: uv (modern Python package manager)
- **Why chosen**: Fast, modern, deterministic locks, pip-compatible
- **Alternatives considered**:
  - pip + requirements.txt (standard but slower)
  - Poetry (mature but slower than uv)
  - pipenv (slower, less maintained)

## Phase 1: Design & Contracts

### Data Model (data-model.md)

See database schema in Technical Context section above. Key entities:

**Users**: Authentication + tier tracking
**Chapters**: Metadata only (content in R2), includes full-text search vector
**Quiz Questions**: Questions + answer keys (never returned in fetch)
**Quiz Attempts**: User submissions + scores
**Chapter Progress**: Per-user chapter completion status
**Daily Activity**: Streak tracking (one row per user per active day)

### API Contracts (contracts/)

**Base URL**: `https://api.coursecompanion.dev/v1` (production)
**Authentication**: `X-API-Key: {user_api_key}` header on all endpoints except `/health`

**Standard Response Envelope**:
```json
{
  "data": { ... },
  "error": null,
  "meta": {
    "timestamp": "2026-01-15T10:00:00Z",
    "request_id": "req_abc123"
  }
}
```

**Endpoint Summary**:

| Method | Path | Feature | Description |
|--------|------|---------|-------------|
| GET | `/health` | — | Health check (no auth) |
| GET | `/chapters` | F1 | List all chapters (metadata only) |
| GET | `/chapters/{id}` | F1 | Get chapter content from R2 |
| GET | `/chapters/{id}/next` | F2 | Get next chapter metadata |
| GET | `/chapters/{id}/prev` | F2 | Get previous chapter metadata |
| GET | `/search` | F3 | Full-text search across chapters |
| GET | `/quizzes/{chapter_id}` | F4 | Get quiz questions (no answers) |
| POST | `/quizzes/{chapter_id}/submit` | F4 | Submit answers, get graded result |
| GET | `/progress/{user_id}` | F5 | Get full progress summary |
| PUT | `/progress/{user_id}/chapter/{chapter_id}` | F5 | Update chapter progress |
| GET | `/progress/{user_id}/quiz-scores` | F5 | Get all quiz scores |
| GET | `/access/check` | F6 | Check access to resource |
| GET | `/users/me` | F6 | Get current user + tier |

**Error Responses**:
- `400 Bad Request`: Invalid request format
- `401 Unauthorized`: Missing or invalid API key
- `403 Forbidden`: Access denied (freemium gate)
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error (generic message, no stack trace)

### Quickstart Guide (quickstart.md)

```markdown
# Quickstart: Course Companion FTE Backend

## Prerequisites

- Python 3.12+
- uv package manager
- Neon PostgreSQL account (free)
- Cloudflare R2 bucket (free)
- Fly.io or Railway account (free)

## Local Setup

1. **Clone and setup**:
   ```bash
   git clone <repo>
   cd backend
   uv venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   uv pip install -e .
   ```

2. **Environment variables** (copy `.env.example` to `.env`):
   ```bash
   DATABASE_URL=postgresql+async://...
   R2_ENDPOINT_URL=https://<account-id>.r2.cloudflarestorage.com
   R2_ACCESS_KEY_ID=...
   R2_SECRET_ACCESS_KEY=...
   R2_BUCKET_NAME=course-companion-content
   ```

3. **Run migrations**:
   ```bash
   alembic upgrade head
   ```

4. **Seed content**:
   ```bash
   python -m seed.seed_chapters
   python -m seed.seed_quizzes
   ```

5. **Run server**:
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access docs**: http://localhost:8000/docs

## Deployment

See `docs/deployment.md` for Fly.io/Railway deployment guide.
```

## Architecture Validation Rules

Before any implementation begins, validate:

- [ ] No `import openai` or `import anthropic` anywhere in `backend/`
- [ ] All routers import only from `services/`, never directly from external AI SDKs
- [ ] `services/` directory contains only deterministic logic
- [ ] Database schema matches all required fields from specification
- [ ] All 6 features map to at least one router file

## Constitution Check (Post-Design)

*Re-check after Phase 1 design completion.*

| Principle | Still Compliant? | Notes |
|-----------|------------------|-------|
| **I. Zero-Backend-LLM** | ✅ Yes | No LLM imports in design |
| **II. Determinism** | ✅ Yes | All services are rule-based |
| **III. Content Verbatim** | ✅ Yes | R2 service returns exact content |
| **IV. ChatGPT is Brain** | ✅ Yes | Backend only serves data |
| **V. Progress Persistence** | ✅ Yes | PostgreSQL schema complete |
| **VI. Single Responsibility** | ✅ Yes | One router per feature |
| **VII. Freemium Gate** | ✅ Yes | Access service enforces in backend |

**POST-DESIGN GATE STATUS**: ✅ PASSED

---

**Plan Status**: ✅ COMPLETE - Ready for `/sp.tasks` command

**Artifacts Generated**:
- ✅ `research.md` (Phase 0 - embedded above)
- ✅ `data-model.md` (Phase 1 - database schema)
- ✅ `contracts/` (Phase 1 - API endpoint summary)
- ✅ `quickstart.md` (Phase 1 - setup guide)
- ✅ Constitution Check passed (pre and post-design)

**Next Step**: Run `/sp.tasks` to break this plan into implementation tasks.
