---
id: 2
title: "Create Project Constitution for Course Companion FTE"
stage: "constitution"
date_iso: "2026-03-10"
surface: "agent"
model: "qwen-code"
feature: "course-companion-fte"
branch: "main"
user: "Administrator"
command: "/sp.constitution Project-Wide Principles, Constraints & Guardrails"
labels: ["constitution", "governance", "phase-1", "zero-backend-llm"]
links:
  spec: "Hackahton.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml: |
  - .specify/memory/constitution.md
tests_yaml: |
  - Automated grep scan: No LLM calls in backend code
  - Manual review: All principles are declarative and testable
  - Template sync: plan-template.md, spec-template.md, tasks-template.md verified aligned
prompt_text: |
  /sp.constitution Project-Wide Principles, Constraints & Guardrails
  
  Purpose: These are the immutable laws of this project. Every specification, plan,
  task, and line of code must conform to this constitution. If any generated artifact
  violates a rule here, it must be rejected and regenerated. This is the supreme source
  of truth.
  
  [Full constitution content with 7 core principles, code quality standards,
  educational content standards, delivery standards, and enforcement checklist]

Response_Text: |
  Created project constitution for Course Companion FTE at version 1.0.0.
  
  **Constitution Structure:**
  
  **7 Core Principles:**
  1. Zero-Backend-LLM Law (NON-NEGOTIABLE) - Most critical Phase 1 rule
  2. Determinism Over Intelligence - Backend must be fully deterministic
  3. Content Verbatim Delivery - No modification of course content
  4. ChatGPT is the Brain - All intelligence in ChatGPT, backend is data-only
  5. Progress Persistence - PostgreSQL database required
  6. Single Responsibility Per Endpoint - One thing per endpoint
  7. Freemium Enforcement at Data Layer - Access control in backend
  
  **Code Quality Standards (5):**
  - CQ-01: Python 3.12+ with full type annotations
  - CQ-02: RESTful API with JSON envelope
  - CQ-03: Structured error handling
  - CQ-04: Security (auth, rate limiting)
  - CQ-05: Testing (80% coverage minimum)
  
  **Educational Content Standards (4):**
  - EC-01: AI Agent Development topic
  - EC-02: Chapter structure requirements
  - EC-03: Rule-based quiz grading only
  - EC-04: Freemium gate definition
  
  **Delivery Standards (4):**
  - DS-01: README completeness
  - DS-02: OpenAPI documentation
  - DS-03: Environment configuration
  - DS-04: ChatGPT App manifest
  
  **Enforcement:**
  - Constitution Enforcement Checklist with 8 verification items
  - Governance section with amendment process and versioning policy
  - Sync Impact Report in HTML comment at top of file
  
  **Template Verification:**
  - ✅ plan-template.md - Constitution Check section already present
  - ✅ spec-template.md - User story format compatible
  - ✅ tasks-template.md - Phase-based structure aligned
  - ⚠ sp.constitution.toml - May need review for Phase 1 specifics

Outcome: |
  Constitution version 1.0.0 ratified and saved to `.specify/memory/constitution.md`.
  
  **Key Achievements:**
  ✓ All placeholder tokens replaced with concrete values
  ✓ Zero-Backend-LLM Law prominently featured as Principle I
  ✓ 7 core principles defined (template had 6, adjusted to match project needs)
  ✓ Code quality, educational content, and delivery standards documented
  ✓ Enforcement checklist with automated and manual verification methods
  ✓ Governance section with versioning policy and amendment process
  ✓ Sync Impact Report included with template alignment status
  ✓ Project Identity table completed
  
  **Version:** 1.0.0 (initial ratification)
  **Ratified:** 2026-03-10
  **Last Amended:** 2026-03-10

Evaluation: |
  **Success Criteria:**
  ✓ No remaining unexplained bracket tokens (except intentionally retained template slots)
  ✓ Version line matches report (1.0.0)
  ✓ Dates in ISO format (YYYY-MM-DD)
  ✓ Principles are declarative, testable, and free of vague language
  ✓ "should" replaced with MUST/SHOULD where appropriate
  ✓ Zero-Backend-LLM Law prominently featured and enforced
  ✓ All 6 required Phase 1 features referenced in enforcement checklist
  ✓ Template alignment verified
  
  **Quality Indicators:**
  - Constitution is actionable and enforceable
  - Principles are independent and testable
  - Governance process is clear
  - Enforcement checklist is automated where possible
  - Sync Impact Report provides transparency
  
  **Ready for:**
  - Phase 1 implementation with clear guardrails
  - Specification creation (/sp.spec)
  - Planning (/sp.plan)
  - Task generation (/sp.tasks)
