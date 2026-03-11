---
id: 4
title: "Create Phase 1 Technical Implementation Plan"
stage: "plan"
date_iso: "2026-03-10"
surface: "agent"
model: "qwen-code"
feature: "complete-phase-1"
branch: "001-complete-phase-1"
user: "Administrator"
command: "/sp.plan Technical Implementation Plan"
labels: ["plan", "phase-1", "technical-design", "zero-backend-llm"]
links:
  spec: "specs/001-complete-phase-1/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml: |
  - specs/001-complete-phase-1/plan.md
tests_yaml: |
  - Constitution Check: All 7 principles compliant
  - Technical decisions: 8 research findings documented
  - API contracts: 13 endpoints defined
  - Data model: 6 entities with relationships
  - Validation rules: 5 architecture checks defined
prompt_text: |
  /sp.plan Technical Implementation Plan
  
  Purpose: Defines HOW the system will be built. Technology choices, architecture
  decisions, directory structure, data models, and API contracts.
  
  [Full technical plan with technology stack, project structure, database schema,
  API contracts, research findings, and constitution compliance checks]

Response_Text: |
  Created Phase 1 Technical Implementation Plan.
  
  **Technology Stack (8 decisions):**
  1. API Framework: FastAPI (Python 3.12) - async, auto OpenAPI
  2. Database: PostgreSQL via Neon (serverless) - free tier, full-text search
  3. ORM: SQLAlchemy 2.0 (async) - type-safe, Alembic migrations
  4. Content Storage: Cloudflare R2 - S3-compatible, cheap egress
  5. Authentication: API Key (X-API-Key header) - simple, ChatGPT compatible
  6. Deployment: Fly.io or Railway - easy deploy, free tier
  7. Search: PostgreSQL full-text search (tsvector) - no external dependency
  8. Dependency Management: uv - fast, modern
  
  **Project Structure:**
  - backend/app/ - FastAPI application
    - models/ - SQLAlchemy ORM models (4 entities)
    - schemas/ - Pydantic v2 schemas
    - routers/ - 6 feature routers
    - services/ - 4 deterministic services
  - chatgpt-app/ - OpenAI Apps SDK manifest + SKILL.md files
  - content/ - Course Markdown files + quiz JSON
  - alembic/ - Database migrations
  
  **Database Schema (6 tables):**
  - users (id, api_key, email, tier, created_at)
  - chapters (id, title, difficulty, is_free, sequence_order, r2_content_key, search_vector)
  - quiz_questions (id, chapter_id, question_text, options, correct_answer)
  - quiz_attempts (id, user_id, chapter_id, score, percentage)
  - chapter_progress (id, user_id, chapter_id, status)
  - daily_activity (id, user_id, activity_date)
  
  **API Contracts (13 endpoints):**
  - GET /health (no auth)
  - GET /chapters, /chapters/{id}, /chapters/{id}/next, /chapters/{id}/prev
  - GET /search
  - GET /quizzes/{chapter_id}, POST /quizzes/{chapter_id}/submit
  - GET /progress/{user_id}, PUT /progress/{user_id}/chapter/{chapter_id}
  - GET /access/check, GET /users/me
  
  **Constitution Compliance:**
  ✅ All 7 principles verified (pre and post-design)
  ✅ Zero-Backend-LLM Law enforced (no LLM imports)
  ✅ Deterministic services only
  ✅ Freemium gate in backend
  
  **Research Findings:**
  - 8 technical decisions documented with rationale
  - Alternatives considered for each decision
  - All NEEDS CLARIFICATION resolved
  
  **Validation Rules:**
  - No openai/anthropic imports
  - Services contain only deterministic logic
  - One router per feature
  - Schema matches specification

Outcome: |
  Phase 1 Technical Implementation Plan completed.
  
  **Key Deliverables:**
  ✓ Technology stack with justifications
  ✓ Project directory structure
  ✓ Database schema (6 tables with relationships)
  ✓ API endpoint contracts (13 endpoints)
  ✓ Research findings (8 technical decisions)
  ✓ Constitution Check passed (pre and post-design)
  ✓ Quickstart guide for local setup
  ✓ Architecture validation rules
  
  **Plan Quality:**
  - All constitution principles respected
  - Zero-Backend-LLM architecture enforced
  - Deterministic services only
  - Clear separation of concerns
  - Testable endpoint design
  
  **Ready for:**
  - Task breakdown (/sp.tasks)
  - Implementation phase

Evaluation: |
  **Success Criteria:**
  ✓ All technical decisions documented with rationale
  ✓ Constitution Check passed (all 7 principles)
  ✓ Database schema complete for all entities
  ✓ API contracts cover all 6 features
  ✓ Project structure supports single responsibility
  ✓ Research findings resolve all unknowns
  ✓ Quickstart guide enables local setup
  
  **Quality Indicators:**
  - Technology choices justified with alternatives
  - Zero-Backend-LLM constraint enforced in design
  - Freemium gate implemented in backend services
  - Progress persistence via PostgreSQL
  - Clear router/service separation
  - Authentication simple and ChatGPT-compatible
  
  **Ready for:**
  - Task creation (/sp.tasks)
  - Implementation kickoff
