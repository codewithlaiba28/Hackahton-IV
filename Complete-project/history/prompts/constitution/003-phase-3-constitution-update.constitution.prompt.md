---
id: PHR-003
title: Phase 3 Constitution Update
stage: constitution
date: 2026-03-12
surface: agent
model: qwen-code
feature: phase-3-web-app
branch: main
user: Administrator
command: /sp.constitution Phase 3 Project-Wide Principles
labels: ["constitution", "phase-3", "governance", "web-app"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - Placeholder token validation (grep scan)
  - Constitution structure validation
---

## Prompt

/sp.constitution Phase 3 Project-Wide Principles, Constraints & Guardrails

Purpose: These are the immutable laws of Phase 3. All Phase 1 and Phase 2 constitutions remain fully in force. Phase 3 ADDS a web frontend and a consolidated backend. Nothing from Phase 1 or 2 is removed.

1. Phase 3 Identity
FieldValueProject NameCourse Companion FTE — Full-Stack Web ApplicationPhasePhase 3 — Standalone End-to-End Web AppBuilds OnPhase 1 (Zero-Backend-LLM) + Phase 2 (Hybrid Intelligence)New FrontendNext.js 15 (App Router) + React 19StylingTailwind CSS v4 + shadcn/uiBackendConsolidated FastAPI (Phase 1 + Phase 2 APIs unified)AuthNextAuth.js v5 (JWT strategy)DeploymentVercel (frontend) + Fly.io (backend)

2. Web App Core Laws
RULE ONE: The web app is a STANDALONE product.
          It does NOT depend on ChatGPT. It is fully self-contained.

RULE TWO: All Phase 1 and Phase 2 backend APIs remain unchanged.
          The consolidated backend ADDS unified routing. It does not rewrite.

RULE THREE: The web frontend must be fully responsive.
            Desktop (1440px), Tablet (768px), Mobile (375px) — all must work perfectly.

RULE FOUR: The freemium gate is enforced on the frontend AND backend.
           Frontend shows locked UI; backend enforces access. Both layers must agree.

RULE FIVE: The web app must have a public-facing landing page.
           Unauthenticated visitors must see a marketing page that converts to sign-ups.

3. Frontend Architecture Laws
FA-01: App Router Only
Use Next.js 15 App Router exclusively. No Pages Router. All pages are Server Components by default; use "use client" only when interactivity is required.
FA-02: Server-Side Data Fetching
All initial data fetching happens in Server Components (using fetch with proper caching). Client Components only for interactive state (quiz taking, real-time progress).
FA-03: Route Protection
All authenticated routes use Next.js middleware for protection. No route can be accessed without valid session — redirect to /login.
FA-04: Optimistic UI
Progress updates and quiz submissions use optimistic updates (React 19 useOptimistic). Never block the UI waiting for API responses for non-critical updates.
FA-05: Zero Broken States
Every page must handle: loading state, empty state, error state, and success state. No blank white screens.

4. Design System Laws
DS-01: Dark-First Theme
The primary theme is dark (background: near-black #0A0A0A). A light mode toggle is optional bonus. Dark theme is mandatory.
DS-02: Design Token Consistency
All colors, spacing, typography, and border radius values must be defined as CSS variables / Tailwind config. No hardcoded values in components.
DS-03: Component Library
Use shadcn/ui as the base component library. All custom components extend shadcn primitives.
DS-04: Typography Hierarchy
Three font roles only:

Display: dramatic heading font (e.g., Sora, Outfit, or Clash Display)
Body: readable body font (e.g., DM Sans, Plus Jakarta Sans)
Mono: code font (JetBrains Mono)

DS-05: Accessibility
All interactive elements must be keyboard-navigable. All images must have alt text. Color contrast ratio ≥ 4.5:1 for body text.

5. Performance Standards
MetricTargetLighthouse Performance≥ 90Lighthouse Accessibility≥ 95First Contentful Paint< 1.5sTime to Interactive< 3.0sCore Web Vitals (LCP)< 2.5s

6. Phase 3 Constitution Checklist
Before submission, reviewer MUST verify:

 Landing page renders correctly and converts to sign-up
 All 6 Phase 1 features accessible via web UI
 Both Phase 2 premium features accessible via web UI (with gate)
 Freemium gate works: free user sees locked content UI
 Fully responsive (test at 375px, 768px, 1440px)
 All pages have loading, empty, and error states
 Authentication works (register, login, logout, session persistence)
 Progress dashboard shows real data
 Quiz flow is complete (start → answer → submit → result)
 Phase 1 and Phase 2 backend APIs unchanged

## Response snapshot

Constitution updated to version 3.0.0 with the following additions:

**New Sections Added:**
- Phase 3 Identity table with technology stack
- Web App Core Laws (5 rules)
- Frontend Architecture Laws (FA-01 through FA-05)
- Design System Laws (DS-01 through DS-05)
- Performance Standards table with 5 metrics
- Phase 3 Constitution Checklist (11 verification items)

**Updated Sections:**
- Project Identity table (added Phase 3 column)
- Constitution Enforcement Checklist (added Phase 3 checklist)
- Governance section (added Phase 3 specific governance)
- Version incremented: 2.0.0 → 3.0.0 (MAJOR bump for new phase)

**Sync Impact Report created** documenting all changes, template alignments, and follow-up TODOs.

## Outcome

- ✅ Impact: Constitution now includes all Phase 3 principles while preserving Phase 1 and Phase 2 principles
- 🧪 Tests: Placeholder token validation passed (0 unresolved tokens found)
- 📁 Files: 1 file modified (.specify/memory/constitution.md)
- 🔁 Next prompts: Create Phase 3 spec, plan, and tasks documents
- 🧠 Reflection: Phase 3 constitution successfully adds web app layer without removing any existing principles

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution update completed successfully
- Graders run and results (PASS/FAIL): PASS - all validations passed
- Prompt variant (if applicable): N/A - standard constitution update
- Next experiment (smallest change to try): Create Phase 3 spec document with user stories for web app features
