# Tasks: Phase 3 Web Application

**Input**: Design documents from `/specs/003-phase-3-web-app/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Tests are OPTIONAL - this task list focuses on implementation. Add tests as needed during development.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/` for Next.js code, `backend/` for existing FastAPI
- All paths are relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize Next.js 15 project with TypeScript, Tailwind CSS, ESLint
- [x] T002 [P] Install core dependencies: next-auth@beta, @tanstack/react-query, zustand, framer-motion, lucide-react
- [x] T003 [P] Install content dependencies: react-markdown, rehype-highlight, recharts
- [x] T004 [P] Initialize shadcn/ui: `npx shadcn@latest init`
- [x] T005 Configure Tailwind with design tokens (colors, fonts, spacing)
- [x] T006 [P] Configure next.config.ts with font optimization (Sora, DM Sans, JetBrains Mono)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 [P] Create global CSS variables in `frontend/app/globals.css` (dark theme, all design tokens)
- [ ] T008 [P] Create TypeScript types in `frontend/types/api.ts` (User, Chapter, Quiz, Progress, Adaptive, Assessment, CostSummary)
- [ ] T009 [P] Implement API client in `frontend/lib/api.ts` (typed fetch wrapper for all 18 endpoints)
- [ ] T010 [P] Configure NextAuth.js in `frontend/lib/auth.ts` (Credentials provider, JWT strategy)
- [ ] T011 Create NextAuth route handler in `frontend/app/api/auth/[...nextauth]/route.ts`
- [ ] T012 [P] Create middleware.ts for route protection (protect all /(dashboard)/ routes)
- [ ] T013 [P] Create Zustand UI store in `frontend/store/useUIStore.ts` (sidebar state, modal state)
- [ ] T014 Configure TanStack Query client in `frontend/lib/queryClient.ts`
- [ ] T015 [P] Create backend auth endpoints in `backend/app/routers/auth.py`:
  - POST /auth/register (email, password, name → user_id, api_key, tier)
  - POST /auth/login (email, password → user_id, api_key, tier, name)
- [ ] T016 Setup environment configuration in `frontend/.env.local.example`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Landing Page Experience (Priority: P1) 🎯 MVP

**Goal**: Convert visitors to registered users with compelling value proposition

**Independent Test**: Visitor can land on page, see all sections, click CTA, and register successfully.

### Implementation for User Story 1

- [x] T017 [P] [US1] Create public route group directory: `frontend/app/(public)/`
- [x] T018 [P] [US1] Create landing page in `frontend/app/(public)/page.tsx`
- [x] T019 [P] [US1] Create Hero component in `frontend/components/landing/Hero.tsx` (headline, subheadline, CTA buttons, animated gradient)
- [x] T020 [P] [US1] Create StatsBar component in `frontend/components/landing/StatsBar.tsx` (4 metrics: 168 hrs/week, 99%+ consistency, 50+ languages, $0.25/session)
- [x] T021 [P] [US1] Create FeaturesGrid component in `frontend/components/landing/FeaturesGrid.tsx` (6 cards: Content Delivery, Navigation, Grounded Q&A, Quizzes, Progress Tracking, Freemium Gate)
- [ ] T022 [US1] Create HowItWorks component in `frontend/components/landing/HowItWorks.tsx` (3 steps with connecting lines)
- [ ] T023 [US1] Create PricingPreview component in `frontend/components/landing/PricingPreview.tsx` (Free $0 vs Premium $9.99/mo cards)
- [ ] T024 [US1] Create Testimonials component in `frontend/components/landing/Testimonials.tsx` (3 placeholder testimonials)
- [x] T025 [P] [US1] Create Footer component in `frontend/components/layout/Footer.tsx` (logo, nav links, copyright)
- [ ] T026 [US1] Implement smooth scroll between sections
- [ ] T027 [US1] Add mobile responsive styles (stacked layout at 375px)
- [x] T028 [P] [US1] Create login page in `frontend/app/(public)/login/page.tsx`
- [x] T029 [P] [US1] Create register page in `frontend/app/(public)/register/page.tsx`
- [x] T030 [US1] Create LoginForm component in `frontend/components/auth/LoginForm.tsx` (email, password, submit to NextAuth)
- [x] T031 [US1] Create RegisterForm component in `frontend/components/auth/RegisterForm.tsx` (email, password, name, submit to backend)
- [x] T032 [US1] Add form validation and error messages to both forms
- [x] T033 [US1] Implement redirect to /dashboard after successful auth

**Checkpoint**: Landing page renders, auth flow works end-to-end, Lighthouse Performance ≥ 90

---

## Phase 4: User Story 2 - Student Dashboard (Priority: P1) 🎯 MVP

**Goal**: First page after login showing progress overview and next action

**Independent Test**: Logged-in user sees accurate progress data, streak, and can navigate to next chapter.

### Implementation for User Story 2

- [x] T034 [P] [US2] Create dashboard layout in `frontend/app/(dashboard)/layout.tsx` (protected layout wrapper)
- [x] T035 [P] [US2] Create Navbar component in `frontend/components/layout/Navbar.tsx` (user greeting, streak badge, tier badge, logout)
- [x] T036 [P] [US2] Create Sidebar component in `frontend/components/layout/Sidebar.tsx` (nav items: Dashboard, Course, Progress, Learning Path, Settings)
- [x] T037 [US2] Create dashboard page in `frontend/app/(dashboard)/dashboard/page.tsx`
- [x] T038 [P] [US2] Create ProgressRing component in `frontend/components/progress/ProgressRing.tsx` (percentage ring chart)
- [x] T039 [P] [US2] Create StreakBadge component in `frontend/components/shared/StreakBadge.tsx` (flame icon + streak count)
- [x] T040 [US2] Create stat cards for dashboard (Chapters Completed, Overall Progress, Best Quiz Score, Total Study Time)
- [x] T041 [US2] Create ContinueLearningCard component (shows next recommended chapter, "Continue" button)
- [ ] T042 [US2] Create RecentActivityFeed component (last 5 actions with timestamps)
- [ ] T043 [US2] Create QuickStats component for premium users (adaptive path summary, "Generate My Learning Path" CTA)
- [x] T044 [US2] Implement data fetching from GET /progress/{userId} and GET /chapters
- [x] T045 [US2] Add loading skeleton during data fetch
- [x] T046 [US2] Add empty state: "Start your first chapter" with CTA if no progress
- [x] T047 [US2] Display streak correctly (0 if no activity)

**Checkpoint**: Dashboard shows real data, loading states work, empty state present

---

## Phase 5: User Story 3 - Course Overview (Priority: P1) 🎯 MVP

**Goal**: Display all chapters with status indicators and access control

**Independent Test**: Free user sees chapters 1-3 unlocked, 4-5 locked. Premium user sees all unlocked.

### Implementation for User Story 3

- [ ] T048 [P] [US3] Create course overview page in `frontend/app/(dashboard)/course/page.tsx`
- [ ] T049 [P] [US3] Create ChapterCard component in `frontend/components/course/ChapterCard.tsx`
- [ ] T050 [US3] Implement chapter card states:
  - Unlocked + Not Started: Normal card with "Start" button
  - Unlocked + In Progress: Card with progress indicator, "Continue" button
  - Unlocked + Completed: Card with green checkmark, "Review" button
  - Locked (Free User): Grayed out card with lock icon, "Upgrade" tooltip
- [ ] T051 [US3] Add chapter metadata display (number, title, difficulty badge, estimated read time)
- [ ] T052 [US3] Add completion status and quiz score display (if taken)
- [ ] T053 [US3] Implement data fetching from GET /chapters (with is_locked field)
- [ ] T054 [US3] Create grid layout (2 cols desktop, 1 col mobile)
- [ ] T055 [US3] Implement upgrade modal trigger on locked chapter click
- [ ] T056 [US3] Add freemium gate logic (free user sees ch-001 to ch-003 unlocked, ch-004+ locked)

**Checkpoint**: Freemium gate works correctly, upgrade modal appears on locked chapter click

---

## Phase 6: User Story 4 - Chapter Reading Experience (Priority: P1) 🎯 MVP

**Goal**: Display chapter content with navigation and reading experience

**Independent Test**: Student can read chapter, mark as complete, navigate prev/next, see progress update.

### Implementation for User Story 4

- [ ] T057 [P] [US4] Create chapter reader page in `frontend/app/(dashboard)/course/[chapter_id]/page.tsx`
- [ ] T058 [P] [US4] Create ChapterReader component in `frontend/components/course/ChapterReader.tsx`
- [ ] T059 [P] [US4] Create MarkdownRenderer component in `frontend/components/course/MarkdownRenderer.tsx` (react-markdown + rehype-highlight)
- [ ] T060 [P] [US4] Create NavigationBar component in `frontend/components/course/NavigationBar.tsx` (prev/next buttons)
- [ ] T061 [US4] Implement left sidebar with table of contents (anchored headings)
- [ ] T062 [US4] Implement right sidebar (desktop) with progress actions + quiz CTA
- [ ] T063 [US4] Add syntax highlighting for code blocks (Prism.js or Shiki)
- [ ] T064 [US4] Create "Mark as Complete" button → calls PUT /progress/{user_id}/chapter/{chapter_id}
- [ ] T065 [US4] Implement optimistic UI update on mark complete
- [ ] T066 [US4] Add "Take Quiz" button → navigates to /course/[chapter_id]/quiz
- [ ] T067 [US4] Implement prev/next chapter navigation at bottom (respects freemium gate)
- [ ] T068 [US4] Add reading progress bar at top (scroll-based)
- [ ] T069 [US4] Implement data fetching from GET /chapters/{id}, GET /chapters/{id}/next, GET /chapters/{id}/prev
- [ ] T070 [US4] Add proper typography styles (prose styles for markdown content)

**Checkpoint**: Chapter renders with syntax highlighting, mark complete works with optimistic update, navigation respects freemium

---

## Phase 7: User Story 5 - Quiz Taking Experience (Priority: P1) 🎯 MVP

**Goal**: Interactive quiz experience with immediate feedback

**Independent Test**: Student can start quiz, answer questions, submit, see results with explanations, and retake.

### Implementation for User Story 5

- [ ] T071 [P] [US5] Create quiz page in `frontend/app/(dashboard)/course/[chapter_id]/quiz/page.tsx`
- [ ] T072 [P] [US5] Create QuizQuestion component in `frontend/components/quiz/QuizQuestion.tsx` (one question at a time, 4 MCQ options)
- [ ] T073 [P] [US5] Create QuizResults component in `frontend/components/quiz/QuizResults.tsx` (score, percentage, per-question breakdown)
- [ ] T074 [P] [US5] Create ConfettiEffect component in `frontend/components/quiz/ConfettiEffect.tsx` (celebration on score ≥ 80%)
- [ ] T075 [US5] Implement quiz flow: Start Screen → Question Screen → Review Screen → Results Screen
- [ ] T076 [US5] Add question counter (e.g., "3/5")
- [ ] T077 [US5] Implement progress bar showing question progress
- [ ] T078 [US5] Add selected answer highlighting (blue)
- [ ] T079 [US5] Implement answer submission to POST /quizzes/{chapter_id}/submit
- [ ] T080 [US5] Display results using API response (correct answers turn green, wrong turn red with correct answer shown)
- [ ] T081 [US5] Add per-question explanations from API
- [ ] T082 [US5] Implement confetti animation on score ≥ 80%
- [ ] T083 [US5] Add "Retake Quiz" button on results screen
- [ ] T084 [US5] Add "Back to Chapter" button on results screen
- [ ] T085 [US5] Implement data fetching from GET /quizzes/{chapter_id}
- [ ] T086 [US5] Add upgrade prompt for locked chapters instead of quiz

**Checkpoint**: Full quiz flow works, results display correctly, confetti on high scores, retake available

---

## Phase 8: User Story 6 - Progress Analytics (Priority: P2)

**Goal**: Detailed learning analytics for the student

**Independent Test**: Student sees accurate streak calendar, chapter progress table, quiz score chart, and earned badges.

### Implementation for User Story 6

- [ ] T087 [P] [US6] Create progress page in `frontend/app/(dashboard)/progress/page.tsx`
- [ ] T088 [P] [US6] Create StreakCalendar component in `frontend/components/progress/StreakCalendar.tsx` (GitHub-style contribution graph)
- [ ] T089 [P] [US6] Create QuizScoreChart component in `frontend/components/progress/QuizScoreChart.tsx` (bar chart with Recharts)
- [ ] T090 [P] [US6] Create AchievementBadges component in `frontend/components/progress/AchievementBadges.tsx`
- [ ] T091 [US6] Implement chapter progress table (all chapters, status, completion date, best quiz score)
- [ ] T092 [US6] Create 4 achievement badges:
  - First Quiz
  - 7-Day Streak
  - First Chapter
  - First Assessment
- [ ] T093 [US6] Implement data fetching from GET /progress/{user_id}
- [ ] T094 [US6] Ensure calendar accurately reflects daily_activity table data
- [ ] T095 [US6] Add empty state: "Complete your first chapter to see progress"
- [ ] T096 [US6] Add loading states during data fetch

**Checkpoint**: All progress data displays accurately, calendar shows daily activity, badges render

---

## Phase 9: User Story 7 - Adaptive Learning Path (Priority: P2) - Premium Only

**Goal**: Display and generate personalized study recommendations for premium users

**Independent Test**: Premium user can generate learning path, see recommendations. Free user sees premium gate.

### Implementation for User Story 7

- [ ] T097 [P] [US7] Create adaptive path page in `frontend/app/(dashboard)/learning-path/page.tsx`
- [ ] T098 [P] [US7] Create PremiumGate component in `frontend/components/premium/PremiumGate.tsx` (banner with upgrade CTA)
- [ ] T099 [P] [US7] Create UpgradeModal component in `frontend/components/premium/UpgradeModal.tsx`
- [ ] T100 [US7] Create LearningPathResult component in `frontend/components/premium/LearningPathResult.tsx`
- [ ] T101 [US7] Implement premium gate banner for free users (with upgrade CTA)
- [ ] T102 [US7] Create "Generate My Learning Path" button for premium users
- [ ] T103 [US7] Implement loading state during LLM call (animated skeleton, ~8s estimated wait)
- [ ] T104 [US7] Implement API call to POST /adaptive/learning-path
- [ ] T105 [US7] Display results: recommended chapters (ordered list with reasons), weak areas, strengths, daily goal
- [ ] T106 [US7] Add "Refresh Recommendations" button (re-calls API)
- [ ] T107 [US7] Display last generated timestamp
- [ ] T108 [US7] Implement data fetching from GET /adaptive/learning-path/latest (cached recommendations)
- [ ] T109 [US7] Ensure each recommended chapter links to /course/[chapter_id]

**Checkpoint**: Free users see premium gate, premium users can generate and view recommendations, loading state works

---

## Phase 10: User Story 8 - Settings (Priority: P2)

**Goal**: Profile management and subscription overview

**Independent Test**: User can view profile, see subscription tier, premium users see LLM usage cost summary.

### Implementation for User Story 8

- [ ] T110 [P] [US8] Create settings page in `frontend/app/(dashboard)/settings/page.tsx`
- [ ] T111 [P] [US8] Create Profile section (name, email read-only, account creation date)
- [ ] T112 [US8] Create Subscription section (current tier badge, upgrade/downgrade CTA, billing info placeholder)
- [ ] T113 [US8] Create LLM Usage section for premium users (monthly cost summary from GET /users/me/cost-summary)
- [ ] T114 [US8] Create Danger Zone section (delete account with confirmation modal)
- [ ] T115 [US8] Implement data fetching from GET /users/me and GET /users/me/cost-summary
- [ ] T116 [US8] Ensure LLM usage section only visible for premium users
- [ ] T117 [US8] Add confirmation modal for delete account action
- [ ] T118 [US8] Display cost summary fetched from API (not hardcoded)

**Checkpoint**: Profile displays correctly, subscription tier shown, premium users see LLM usage, delete account has confirmation

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories, quality assurance, deployment readiness

- [ ] T119 [P] Responsive testing at 375px (mobile), 768px (tablet), 1440px (desktop)
- [ ] T120 [P] Fix all responsive issues found during testing
- [ ] T121 [P] Add loading.tsx skeleton to all data-fetching pages
- [ ] T122 [P] Add error boundaries to all pages
- [ ] T123 Add empty states with actionable CTAs to all list/data sections
- [ ] T124 [P] Optimize images with next/image
- [ ] T125 [P] Implement code splitting with dynamic imports for heavy components (Recharts, MarkdownRenderer, ConfettiEffect)
- [ ] T126 Remove unused Tailwind classes (purge configured)
- [ ] T127 [P] Run Lighthouse audit and fix issues
- [ ] T128 Achieve Lighthouse Performance ≥ 90
- [ ] T129 Achieve Lighthouse Accessibility ≥ 95
- [ ] T130 [P] Update README.md with Phase 3 frontend setup instructions
- [ ] T131 [P] Update docs/architecture-diagram.png to show web frontend
- [ ] T132 Create docs/phase3-deployment.md (Vercel + Fly.io deployment guide)
- [ ] T133 Code cleanup and refactoring
- [ ] T134 Security hardening (XSS prevention, CSRF protection, input sanitization)
- [ ] T135 [P] Run quickstart.md validation (developer can run frontend locally from README alone)

---

## Phase 12: Backend Auth Endpoints (Phase 3 Addition)

**Purpose**: Add required backend endpoints for NextAuth integration

**Note**: These are the ONLY new backend endpoints in Phase 3. All existing Phase 1 and Phase 2 endpoints remain unchanged.

- [ ] T136 [P] Create `backend/app/routers/auth.py` with password hashing (bcrypt)
- [ ] T137 Implement POST /auth/register:
  - Body: { email, name, password }
  - Hash password with bcrypt
  - Generate API key as secrets.token_hex(32)
  - Create user with tier='free'
  - Return: { user_id, api_key, tier, name }
- [ ] T138 Implement POST /auth/login:
  - Body: { email, password }
  - Validate credentials (check hashed password)
  - Return: { user_id, api_key, tier, name }
  - Return 401 for invalid credentials
- [ ] T139 Register auth router in backend/app/main.py
- [ ] T140 Test both endpoints with Postman/curl
- [ ] T141 Add auth endpoints to OpenAPI documentation

---

## Checkpoints

### CHECKPOINT P3-A: Frontend Infrastructure Review
**After Phase 2 (T007-T016)**
- [ ] Auth works (login → redirect to dashboard)
- [ ] API client connects to backend
- [ ] Design tokens applied globally
- [ ] All CSS variables defined and working

### CHECKPOINT P3-B: Public Pages Review
**After Phase 3 (T017-T033)**
- [ ] Landing page renders beautifully
- [ ] Auth flow works end-to-end
- [ ] Lighthouse Performance ≥ 90

### CHECKPOINT P3-C: Core Course Features Review
**After Phase 7 (T057-T086)**
- [ ] Chapter reading works end-to-end
- [ ] Quiz taking works end-to-end
- [ ] Progress updating works (mark complete, optimistic UI)

### CHECKPOINT P3-FINAL: Pre-Submission Complete
**After all phases**
- [ ] All three phase checklists passed
- [ ] Lighthouse audit complete (Performance ≥ 90, Accessibility ≥ 95)
- [ ] Demo video recorded
- [ ] All responsive breakpoints tested (375px, 768px, 1440px)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 completion - **BLOCKS all user stories**
- **Phase 3-10 (User Stories)**: All depend on Phase 2 completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Phase 11 (Polish)**: Depends on all user stories being complete
- **Phase 12 (Backend Auth)**: Can run in parallel with Phase 2

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2 - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Phase 2 - Independent
- **User Story 3 (P1)**: Can start after Phase 2 - Independent
- **User Story 4 (P1)**: Can start after Phase 2 - Independent
- **User Story 5 (P1)**: Can start after Phase 2 - Independent
- **User Story 6 (P2)**: Can start after Phase 2 - Independent
- **User Story 7 (P2)**: Can start after Phase 2 - Depends on PremiumGate from US7
- **User Story 8 (P2)**: Can start after Phase 2 - Independent

### Within Each User Story

- Models/types before components
- Components before page integration
- Core implementation before polish
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1**: All tasks [P] can run in parallel
- **Phase 2**: All tasks [P] can run in parallel
- **After Phase 2**: All user stories can start in parallel (if team capacity allows)
- **Within User Stories**: All [P] tasks can run in parallel
- **Phase 11**: All [P] tasks can run in parallel

---

## Parallel Example: User Story 1 (Landing Page)

```bash
# Launch all component creation together:
Task: "Create Hero component in frontend/components/landing/Hero.tsx"
Task: "Create StatsBar component in frontend/components/landing/StatsBar.tsx"
Task: "Create FeaturesGrid component in frontend/components/landing/FeaturesGrid.tsx"
Task: "Create Footer component in frontend/components/layout/Footer.tsx"

# Launch auth pages together:
Task: "Create login page in frontend/app/(public)/login/page.tsx"
Task: "Create register page in frontend/app/(public)/register/page.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Landing Page + Auth)
4. **STOP and VALIDATE**: Test landing page, registration flow
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Landing + Auth) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (Dashboard) → Test independently → Deploy/Demo
4. Add User Story 3 (Course Overview) → Test independently → Deploy/Demo
5. Add User Story 4 (Chapter Reader) → Test independently → Deploy/Demo
6. Add User Story 5 (Quiz) → Test independently → Deploy/Demo
7. Add User Story 6-8 (P2 features) → Test independently → Deploy/Demo
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Landing + Auth)
   - Developer B: User Story 2 (Dashboard) + User Story 3 (Course)
   - Developer C: User Story 4 (Chapter) + User Story 5 (Quiz)
3. After P1 stories complete:
   - Developer A: User Story 6 (Progress)
   - Developer B: User Story 7 (Adaptive Path)
   - Developer C: User Story 8 (Settings)
4. All complete Phase 11 (Polish) together

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability (e.g., [US1], [US2])
- Each user story should be independently completable and testable
- Commit after each task or logical group of tasks
- Stop at checkpoints to validate independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

**Total Tasks**: 141

**By Phase**:
- Phase 1 (Setup): 6 tasks
- Phase 2 (Foundational): 10 tasks
- Phase 3 (US1 - Landing): 17 tasks
- Phase 4 (US2 - Dashboard): 14 tasks
- Phase 5 (US3 - Course): 9 tasks
- Phase 6 (US4 - Chapter): 14 tasks
- Phase 7 (US5 - Quiz): 16 tasks
- Phase 8 (US6 - Progress): 10 tasks
- Phase 9 (US7 - Adaptive): 13 tasks
- Phase 10 (US8 - Settings): 9 tasks
- Phase 11 (Polish): 17 tasks
- Phase 12 (Backend Auth): 6 tasks

**Parallel Opportunities**:
- Phase 1: 4/6 tasks can run in parallel
- Phase 2: 7/10 tasks can run in parallel
- User Stories: All P1 stories (US1-US5) can run in parallel after Phase 2
- Polish: 8/17 tasks can run in parallel

**MVP Scope**: Phases 1-3 (Landing Page + Auth) - 33 tasks

---

**Ready to Implement!** 🚀

Start with Phase 1, proceed through Phase 2 (foundational), then tackle user stories in priority order.
