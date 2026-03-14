# Course Companion FTE

**A Zero-Backend-LLM Educational Tutor for AI Agent Development**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 Project Overview

Course Companion FTE is a **Digital Full-Time Equivalent** educational tutor that teaches AI Agent Development. Built for the Panaversity Agent Factory Hackathon IV, it delivers course content, quizzes, progress tracking, and personalized tutoring through a ChatGPT App interface.

### Key Innovation: Zero-Backend-LLM Architecture

In Phase 1, **ALL intelligence lives in ChatGPT**. The FastAPI backend is purely deterministic:
- ✅ Serves content verbatim from Cloudflare R2
- ✅ Tracks progress in PostgreSQL
- ✅ Grades quizzes with rule-based matching
- ✅ Enforces freemium access control
- ❌ **NO LLM API calls** (openai, anthropic, langchain, etc.)

This architecture achieves **99% cost savings** compared to human tutors while maintaining educational quality through guardrails and Agent Skills.

## 🏗️ Architecture

```
┌─────────────┐
│   Student   │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│   ChatGPT App       │ ← ALL intelligence here
│   (OpenAI SDK)      │   Explanation, tutoring, encouragement
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  FastAPI Backend    │ ← ZERO LLM calls
│  (Deterministic)    │   Content, quizzes, progress, access
└──────────┬──────────┘
           │
           ▼
    ┌──────┴──────┐
    ▼             ▼
┌─────────┐  ┌──────────┐
│PostgreSQL│  │ R2 Store │
│(Neon)   │  │(Content) │
└─────────┘  └──────────┘
```

See [`docs/architecture-diagram.png`](docs/architecture-diagram.png) for detailed architecture.

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- uv package manager (`pip install uv`)
- PostgreSQL database (Neon serverless recommended)
- Cloudflare R2 bucket

### Local Setup

```bash
# Clone repository
git clone <repo-url>
cd Hackahton-IV/backend

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e .

# Copy environment variables
cp .env.example .env
# Edit .env with your database URL and R2 credentials

# Run database migrations
alembic upgrade head

# Seed course content and quizzes
python -m seed.seed_chapters
python -m seed.seed_quizzes

# Start development server
uvicorn app.main:app --reload
```

Access API docs at: http://localhost:8000/docs

## 📚 API Endpoints

| Method | Endpoint | Feature | Description |
|--------|----------|---------|-------------|
| GET | `/health` | — | Health check |
| GET | `/chapters` | F1 | List all chapters |
| GET | `/chapters/{id}` | F1 | Get chapter content |
| GET | `/chapters/{id}/next` | F2 | Get next chapter |
| GET | `/chapters/{id}/prev` | F2 | Get previous chapter |
| GET | `/search?q={query}` | F3 | Search content |
| GET | `/quizzes/{chapter_id}` | F4 | Get quiz questions |
| POST | `/quizzes/{chapter_id}/submit` | F4 | Submit quiz answers |
| GET | `/progress/{user_id}` | F5 | Get progress summary |
| PUT | `/progress/{user_id}/chapter/{id}` | F5 | Update progress |
| GET | `/access/check` | F6 | Check access |
| GET | `/users/me` | F6 | Get current user |

## 🌐 Web Frontend (Phase 3)

A professional, standalone Next.js web application implementing all features from Phases 1 and 2 with custom branding and enhanced UX.

**Location:** `frontend/`

### Features

| Feature | Description | Status |
|---------|-------------|--------|
| 📚 Chapters | Rich markdown rendering with code highlighting | ✅ |
| 📊 Progress | Dynamic dashboard with completion tracking | ✅ |
| 📝 Quiz | Interactive rule-based testing | ✅ |
| 🧠 Assessments | LLM-Graded conceptual testing (Premium/Pro) | ✅ |
| 🗺️ Adaptive Path | AI-generated study recommendations (Premium/Pro) | ✅ |
| 🔒 Freemium | Tier-based access control and upgrade flows | ✅ |

### Quick Start

```bash
cd frontend
npm install
npm run dev
# Open http://localhost:3000
```

### Configuration

Create `.env.local` in the `frontend` directory:
```bash
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

**Documentation:** See [`frontend/README.md`](frontend/README.md) for the complete developer guide.

---

## 🔐 Authentication

All endpoints (except `/health`) require API key authentication:

```bash
curl -H "X-API-Key: your_api_key" http://localhost:8000/chapters
```

API keys are stored in the `users` table and linked to subscription tiers (free/premium).

## 📦 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Pydantic settings
│   ├── database.py          # Async SQLAlchemy engine
│   ├── auth.py              # API key authentication
│   │
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── chapter.py
│   │   ├── quiz.py
│   │   └── progress.py
│   │
│   ├── schemas/             # Pydantic v2 schemas
│   │   ├── common.py        # APIResponse envelope
│   │   ├── chapter.py
│   │   ├── quiz.py
│   │   ├── progress.py
│   │   └── user.py
│   │
│   ├── routers/             # Feature routers
│   │   ├── chapters.py      # Features 1 & 2
│   │   ├── search.py        # Feature 3
│   │   ├── quizzes.py       # Feature 4
│   │   ├── progress.py      # Feature 5
│   │   ├── access.py        # Feature 6
│   │   └── users.py
│   │
│   └── services/            # Business logic (deterministic)
│       ├── r2_service.py
│       ├── quiz_service.py
│       ├── progress_service.py
│       └── access_service.py
│
├── alembic/                 # Database migrations
├── tests/                   # Test suite
├── seed/                    # Content seeding scripts
├── pyproject.toml
└── .env.example
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_chapters.py -v
```

**Coverage requirement:** ≥80% on business logic

## 🎓 Course Content

The course covers **AI Agent Development** with 5 chapters:

1. **Introduction to AI Agents** (Free)
2. **Claude Agent SDK** (Free)
3. **MCP Basics** (Free)
4. **Agent Skills** (Premium)
5. **Agent Factory Architecture** (Premium)

Each chapter includes:
- 800+ words of substantive content
- Code examples
- 5 quiz questions (MCQ and true/false)

## 💰 Cost Analysis

**Phase 1 Monthly Costs (10K users):**

| Component | Cost |
|-----------|------|
| Cloudflare R2 | ~$5 |
| PostgreSQL (Neon) | $0-25 |
| Compute (Fly.io/Railway) | ~$10 |
| **Total** | **$16-41** |
| **Cost per user** | **$0.002-0.004** |

Compare to human tutoring: **$2,000-5,000/month** → **99% cost savings**

See [`docs/cost-analysis.md`](docs/cost-analysis.md) for detailed breakdown.

## 🤖 ChatGPT App Setup

1. Create `chatgpt-app/openapi.yaml` manifest
2. Register with OpenAI Apps SDK
3. Configure system prompt in `chatgpt-app/system-prompt.md`
4. Deploy 4 Agent Skills:
   - `concept-explainer`
   - `quiz-master`
   - `socratic-tutor`
   - `progress-motivator`

## 🔒 Security

- API key authentication for all user endpoints
- User IDs derived from auth token (never from request body)
- Freemium gate enforced at service layer
- No LLM API calls in backend (Zero-Backend-LLM law)
- Rate limiting on public endpoints

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `R2_ENDPOINT_URL` | Cloudflare R2 endpoint | Yes |
| `R2_ACCESS_KEY_ID` | R2 access key | Yes |
| `R2_SECRET_ACCESS_KEY` | R2 secret key | Yes |
| `R2_BUCKET_NAME` | R2 bucket name | Yes |
| `SECRET_KEY` | JWT generation key | Yes |
| `APP_ENV` | Environment (development/production) | No |

## 🚧 Development Workflow

1. **Setup**: Install dependencies, run migrations
2. **Implement**: Follow tasks.md for ordered implementation
3. **Test**: Write tests before/during implementation (TDD)
4. **Validate**: Run Zero-LLM compliance audit
5. **Deploy**: Deploy to Fly.io/Railway

## 📋 Implementation Tasks

See [`specs/001-complete-phase-1/tasks.md`](specs/001-complete-phase-1/tasks.md) for complete task breakdown (44 tasks).

## ⚠️ Critical Compliance

**Zero-Backend-LLM Law (Phase 1):**

```python
# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.
```

**Automated Audit:**
```bash
grep -r "openai\|anthropic\|langchain\|llama_index" app/ --include="*.py"
# Expected: zero results
```

## 🏆 Hackathon Deliverables

- [x] Source code (this repository)
- [x] Architecture diagram
- [x] Specification document (`specs/001-complete-phase-1/spec.md`)
- [x] Technical plan (`specs/001-complete-phase-1/plan.md`)
- [x] Implementation tasks (`specs/001-complete-phase-1/tasks.md`)
- [x] API documentation (http://localhost:8000/docs)
- [x] ChatGPT App manifest (`chatgpt-app/openapi.yaml`)
- [x] Cost analysis (`docs/cost-analysis.md`)

## 📄 License

MIT License - see LICENSE file for details

## 👥 Team

Built for Panaversity Agent Factory Hackathon IV

## 🔗 Resources

- [Agent Factory Architecture](https://docs.google.com/document/d/15GuwZwIOQy_g1XsIJjQsFNHCTQTWoXQhWGVMhiH0swc/)
- [AI Agent Factory Textbook](https://agentfactory.panaversity.org/)

---

**Ready to build the future of education!** 🚀
