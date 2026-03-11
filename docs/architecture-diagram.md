# Architecture Diagram

## Phase 1: Zero-Backend-LLM Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER (Student)                                  │
│                         Access via ChatGPT App                               │
└────────────────────────────────────┬────────────────────────────────────────┘
                                     │
                                     │ HTTPS
                                     │ User queries, quiz submissions
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ChatGPT App (OpenAI Platform)                        │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                    ALL INTELLIGENCE LIVES HERE                         │  │
│  │  • Explanation generation                                              │  │
│  │  • Tutoring conversations                                              │  │
│  │  • Encouragement & motivation                                          │  │
│  │  • Adaptation to learner level                                         │  │
│  │  • Agent Skills execution                                              │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                         System Prompt + 4 Skills                             │
│  • concept-explainer  • quiz-master  • socratic-tutor  • progress-motivator │
└────────────────────────────────────┬────────────────────────────────────────┘
                                     │
                                     │ API Calls (X-API-Key authenticated)
                                     │ GET /chapters, POST /quizzes/submit, etc.
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend (Deterministic - ZERO LLM)                │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  API Routes (app/routers/)                                            │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐  │  │
│  │  │  chapters   │ │   quizzes   │ │  progress   │ │     access      │  │  │
│  │  │  GET /      │ │ GET /{id}   │ │ GET /{uid}  │ │ GET /check      │  │  │
│  │  │  GET /{id}  │ │ POST /submit│ │ PUT /{uid}/ │ │                 │  │  │
│  │  │  GET /next  │ │ GET /best   │ │ GET /{uid}/ │ │                 │  │  │
│  │  │  GET /prev  │ │             │ │ quiz-scores │ │                 │  │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────────┘  │  │
│  │  ┌─────────────┐ ┌─────────────┐                                      │  │
│  │  │   search    │ │    users    │                                      │  │
│  │  │ GET /?q=    │ │ GET /me     │                                      │  │
│  │  └─────────────┘ └─────────────┘                                      │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Services (app/services/) - Business Logic Layer                      │  │
│  │  • r2_service.py       - Cloudflare R2 content retrieval + caching    │  │
│  │  • quiz_service.py     - Rule-based quiz grading (exact match)        │  │
│  │  • progress_service.py - Progress tracking, streak calculation        │  │
│  │  • access_service.py   - Freemium gate enforcement                    │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Authentication (app/auth.py)                                         │  │
│  │  • API Key validation via X-API-Key header                            │  │
│  │  • User lookup from PostgreSQL                                        │  │
│  │  • Returns 401 for invalid/missing keys                               │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  ⚠️  ZERO-LLM COMPLIANCE: No openai, anthropic, langchain imports          │
└────────────────────────────────────┬────────────────────────────────────────┘
                                     │
                     ┌───────────────┴───────────────┐
                     │                               │
                     ▼                               ▼
┌─────────────────────────────┐     ┌─────────────────────────────┐
│     PostgreSQL Database     │     │   Cloudflare R2 Storage     │
│  (Neon Serverless)          │     │  (Content Storage)          │
│                             │     │                             │
│  ┌───────────────────────┐  │     │  ┌───────────────────────┐  │
│  │ users                 │  │     │  │ chapters/             │  │
│  │ - id (UUID)           │  │     │  │  ch-001/content.md    │  │
│  │ - api_key (unique)    │  │     │  │  ch-002/content.md    │  │
│  │ - email (unique)      │  │     │  │  ch-003/content.md    │  │
│  │ - tier (enum)         │  │     │  │  ch-004/content.md    │  │
│  │ - created_at          │  │     │  │  ch-005/content.md    │  │
│  └───────────────────────┘  │     │  └───────────────────────┘  │
│                             │     │                             │
│  ┌───────────────────────┐  │     │  Content: Raw Markdown      │
│  │ chapters              │  │     │  - 800+ words per chapter   │
│  │ - id (PK)             │  │     │  - Code examples            │
│  │ - title               │  │     │  - Exercises                │
│  │ - difficulty          │  │     │                             │
│  │ - is_free (boolean)   │  │     │                             │
│  │ - sequence_order      │  │     │                             │
│  │ - r2_content_key      │  │     │                             │
│  │ - search_vector       │  │     │                             │
│  └───────────────────────┘  │     │                             │
│                             │     │                             │
│  ┌───────────────────────┐  │     │                             │
│  │ quiz_questions        │  │     │                             │
│  │ - id (UUID)           │  │     │                             │
│  │ - chapter_id (FK)     │  │     │                             │
│  │ - question_text       │  │     │                             │
│  │ - correct_answer      │  │     │                             │
│  │ - explanation         │  │     │                             │
│  └───────────────────────┘  │     │                             │
│                             │     │                             │
│  ┌───────────────────────┐  │     │                             │
│  │ chapter_progress      │  │     │                             │
│  │ - user_id (FK)        │  │     │                             │
│  │ - chapter_id (FK)     │  │     │                             │
│  │ - status              │  │     │                             │
│  │ - started_at          │  │     │                             │
│  │ - completed_at        │  │     │                             │
│  └───────────────────────┘  │     │                             │
│                             │     │                             │
│  ┌───────────────────────┐  │     │                             │
│  │ quiz_attempts         │  │     │                             │
│  │ - user_id (FK)        │  │     │                             │
│  │ - chapter_id (FK)     │  │     │                             │
│  │ - score               │  │     │                             │
│  │ - percentage          │  │     │                             │
│  └───────────────────────┘  │     │                             │
│                             │     │                             │
│  ┌───────────────────────┐  │     │                             │
│  │ daily_activity        │  │     │                             │
│  │ - user_id (FK)        │  │     │                             │
│  │ - activity_date       │  │     │                             │
│  └───────────────────────┘  │     │                             │
└─────────────────────────────┘     └─────────────────────────────┘
```

## Data Flow Examples

### 1. Content Delivery (Free User)

```
User → ChatGPT: "Show me chapter 1"
   │
   └─→ ChatGPT → Backend: GET /chapters/ch-001 [X-API-Key: user_key_123]
          │
          ├─→ Backend validates API key → User (tier: free)
          │
          ├─→ Backend checks: is_free = true ✓
          │
          ├─→ Backend fetches from R2: chapters/ch-001/content.md
          │
          └─→ Backend → ChatGPT: Chapter content (Markdown)
                 │
                 └─→ ChatGPT: Explains content at user's level
```

### 2. Quiz Submission

```
User → ChatGPT: "I want to take the quiz"
   │
   └─→ ChatGPT → Backend: GET /quizzes/ch-001
          │
          ├─→ Backend returns questions (WITHOUT correct_answer)
          │
          └─→ ChatGPT: Presents questions to user

User → ChatGPT: "My answers: 1-B, 2-A, 3-C..."
   │
   └─→ ChatGPT → Backend: POST /quizzes/ch-001/submit
                 {answers: [{question_id, answer}, ...]}
          │
          ├─→ Backend grades by EXACT string match
          │
          ├─→ Backend records attempt in quiz_attempts
          │
          └─→ Backend → ChatGPT: {score: 4/5, percentage: 80%, results: [...]}
                 │
                 └─→ ChatGPT: Celebrates, explains wrong answers
```

### 3. Freemium Gate (Premium Chapter)

```
User → ChatGPT: "Show me chapter 4"
   │
   └─→ ChatGPT → Backend: GET /chapters/ch-004 [X-API-Key: free_user_key]
          │
          ├─→ Backend validates: User tier = free
          │
          ├─→ Backend checks: ch-004.is_free = false ✗
          │
          └─→ Backend → ChatGPT: 403 Forbidden
                 {reason: "Chapter requires premium", upgrade_required: true}
                 │
                 └─→ ChatGPT: "Chapter 4 requires premium. Upgrade to access..."
```

## Security Boundaries

```
┌─────────────────────────────────────────────────────────────────┐
│  Trust Boundary: Internet (Untrusted)                           │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Trust Boundary: TLS/HTTPS                                 │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  Trust Boundary: API Key Authentication              │  │  │
│  │  │                                                       │  │  │
│  │  │  ┌───────────────────────────────────────────────┐   │  │  │
│  │  │  │  FastAPI Backend (Trusted)                    │   │  │  │
│  │  │  │  • All inputs validated                        │   │  │  │
│  │  │  │  • SQL injection prevented (SQLAlchemy ORM)    │   │  │  │
│  │  │  │  • User ID from auth token (never from body)   │   │  │  │
│  │  │  └───────────────────────────────────────────────┘   │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Zero-Backend-LLM Compliance

```
┌─────────────────────────────────────────────────────────────────┐
│  FORBIDDEN IMPORTS (Will cause disqualification)                │
│                                                                  │
│  ✗ import openai                                                │
│  ✗ from anthropic import ...                                    │
│  ✗ import langchain                                             │
│  ✗ from llama_index import ...                                  │
│  ✗ import cohere                                                │
│  ✗ import groq                                                  │
│                                                                  │
│  ALLOWED (Deterministic operations)                             │
│                                                                  │
│  ✓ import fastapi                                               │
│  ✓ import sqlalchemy                                            │
│  ✓ import boto3  (for R2)                                       │
│  ✓ import pydantic                                              │
│  ✓ import pytest                                                │
└─────────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Production Deployment (Fly.io)                                 │
│                                                                  │
│  ┌─────────────────┐    ┌─────────────────┐                    │
│  │  Fly.io App     │    │  Fly.io App     │                    │
│  │  (Primary)      │    │  (Replica)      │                    │
│  │                 │    │                 │                    │
│  │  FastAPI :8000  │    │  FastAPI :8000  │                    │
│  │  + PostgreSQL   │    │  (Standby)      │                    │
│  └────────┬────────┘    └────────┬────────┘                    │
│           │                      │                               │
│           └──────────┬───────────┘                               │
│                      │                                           │
│              ┌───────┴───────┐                                  │
│              │  Fly.io Proxy │                                  │
│              │  (Load Balancer)                                │
│              └───────┬───────┘                                  │
│                      │                                           │
│         ┌────────────┴────────────┐                             │
│         │                         │                             │
│         ▼                         ▼                             │
│  ┌─────────────┐           ┌─────────────┐                     │
│  │ Neon PG     │           │ Cloudflare  │                     │
│  │ (External)  │           │ R2          │                     │
│  └─────────────┘           └─────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
```

---

*Diagram Version: 1.0 | Last Updated: January 2026*
