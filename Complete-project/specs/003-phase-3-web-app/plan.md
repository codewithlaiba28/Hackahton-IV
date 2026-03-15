# Implementation Plan: Phase 3 Web Application

**Branch**: `3-phase-3-web-app` | **Date**: 2026-03-12 | **Spec**: [specs/003-phase-3-web-app/spec.md](../spec.md)
**Input**: Complete Phase 3 web application specification with 8 pages, authentication, and shared components

## Summary

Build a comprehensive Next.js 15 web application for the Course Companion FTE that provides a standalone learning platform with 8 pages (landing, dashboard, course overview, chapter reader, quiz, progress, adaptive path, settings), NextAuth.js v5 authentication, dark-first design system, and integration with Phase 1 and Phase 2 backend APIs.

## Technical Context

**Language/Version**: TypeScript 5.x (frontend), Python 3.12+ (backend - existing)
**Primary Dependencies**: Next.js 15, React 19, Tailwind CSS v4, shadcn/ui, NextAuth.js v5, TanStack Query v5, Zustand, Recharts
**Storage**: PostgreSQL (backend - existing), Cloudflare R2 (content - existing)
**Testing**: Jest, React Testing Library, Playwright (E2E)
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge - last 2 versions)
**Project Type**: Web application (frontend + existing backend)
**Performance Goals**: Lighthouse Performance ≥90, FCP <1.5s, TTI <3.0s, LCP <2.5s
**Constraints**: Dark theme mandatory, fully responsive (375px/768px/1440px), accessibility WCAG 2.1 AA
**Scale/Scope**: 1,000 concurrent users, 8 pages, 20+ components, 18 API endpoints

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase 1 Constitution Compliance
- ✅ **Zero-Backend-LLM Law**: Frontend only - no backend changes required
- ✅ **Determinism Over Intelligence**: All frontend logic is deterministic
- ✅ **Content Verbatim Delivery**: Markdown renderer preserves content exactly
- ✅ **Progress Persistence**: Uses existing Phase 1 progress APIs
- ✅ **Single Responsibility Per Endpoint**: Frontend components are modular
- ✅ **Freemium Enforcement**: Both frontend gate (UI) and backend gate (API)

### Phase 2 Constitution Compliance
- ✅ **Hybrid Selectivity Law**: Phase 2 features (adaptive path, assessments) remain premium-gated
- ✅ **Architectural Separation**: Frontend is separate codebase from backend
- ✅ **Cost Control Standards**: LLM usage displayed via existing cost-summary API
- ✅ **Premium Gate Enforcement**: Frontend shows premium gate, backend enforces

### Phase 3 Constitution Compliance
- ✅ **Phase 3 Identity Law**: Standalone web app, doesn't depend on ChatGPT
- ✅ **Frontend Architecture Laws**: App Router, Server Components, route protection, optimistic UI
- ✅ **Design System Laws**: Dark-first, design tokens, shadcn/ui, typography hierarchy
- ✅ **Performance Standards**: Lighthouse ≥90, Accessibility ≥95, FCP <1.5s

**GATE STATUS**: ✅ PASS - All constitution principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/003-phase-3-web-app/
├── plan.md              # This file
├── research.md          # Phase 0 output (generated below)
├── data-model.md        # Phase 1 output (generated below)
├── quickstart.md        # Phase 1 output (generated below)
├── contracts/           # Phase 1 output (API contracts)
└── tasks.md             # Phase 2 output (via /sp.tasks)
```

### Source Code (repository root)

```text
# Web Application Structure
frontend/
├── app/                              # Next.js App Router
│   ├── (public)/                     # Public route group (no auth)
│   │   ├── page.tsx                  # Landing page /
│   │   ├── features/page.tsx
│   │   ├── pricing/page.tsx
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   │
│   ├── (dashboard)/                  # Protected route group (auth required)
│   │   ├── layout.tsx                # Dashboard layout (sidebar + navbar)
│   │   ├── dashboard/page.tsx
│   │   ├── course/
│   │   │   ├── page.tsx              # Course overview
│   │   │   └── [chapter_id]/
│   │   │       ├── page.tsx          # Chapter reader
│   │   │       ├── quiz/page.tsx     # Quiz page
│   │   │       └── assessment/page.tsx # LLM assessment (premium)
│   │   ├── learning-path/page.tsx    # Adaptive path (premium)
│   │   ├── progress/page.tsx
│   │   └── settings/page.tsx
│   │
│   ├── api/                          # Next.js API routes
│   │   └── auth/[...nextauth]/route.ts
│   │
│   ├── layout.tsx                    # Root layout
│   ├── globals.css                   # CSS variables, base styles
│   └── not-found.tsx                 # 404 page
│
├── components/
│   ├── ui/                           # shadcn/ui components
│   ├── layout/
│   │   ├── Navbar.tsx
│   │   ├── Sidebar.tsx
│   │   └── Footer.tsx
│   ├── course/
│   │   ├── ChapterCard.tsx
│   │   ├── ChapterReader.tsx
│   │   ├── MarkdownRenderer.tsx
│   │   └── ChapterNavigation.tsx
│   ├── quiz/
│   │   ├── QuizQuestion.tsx
│   │   ├── QuizResults.tsx
│   │   └── ConfettiEffect.tsx
│   ├── progress/
│   │   ├── ProgressRing.tsx
│   │   ├── StreakCalendar.tsx
│   │   ├── QuizScoreChart.tsx
│   │   └── AchievementBadges.tsx
│   ├── premium/
│   │   ├── PremiumGate.tsx
│   │   └── UpgradeModal.tsx
│   └── shared/
│       ├── LoadingSkeleton.tsx
│       ├── StreakBadge.tsx
│       └── ErrorBoundary.tsx
│
├── lib/
│   ├── api.ts                        # Typed API client
│   ├── auth.ts                       # NextAuth config
│   └── utils.ts                      # cn(), formatters
│
├── hooks/
│   ├── useProgress.ts                # TanStack Query hooks
│   ├── useChapters.ts
│   └── useQuiz.ts
│
├── store/
│   └── useUIStore.ts                 # Zustand: UI state
│
├── types/
│   └── api.ts                        # TypeScript types
│
├── public/
│   ├── logo.svg
│   └── og-image.png
│
├── next.config.ts
├── tailwind.config.ts
├── components.json
├── .env.local.example
└── package.json

backend/                              # Existing Phase 1 + Phase 2
└── [unchanged - APIs already built]
```

**Structure Decision**: Web application with separate frontend (Next.js) and backend (FastAPI). Frontend uses App Router structure with route groups for public vs protected pages.

## Complexity Tracking

> Constitution Check passed - no violations to justify

---

## Phase 0: Research & Technology Decisions

### Decision: Next.js 15 App Router

**Rationale**: 
- Server Components reduce bundle size and improve performance
- Built-in SSR/SSG support for fast FCP (<1.5s requirement)
- App Router provides better layout patterns and route groups
- Edge runtime support for future scalability
- Official React 19 support with useOptimistic hook

**Alternatives Considered**:
- Remix: Good SSR but smaller ecosystem
- Vite + React: More config, no SSR out-of-box
- Next.js Pages Router: Legacy, no App Router benefits

### Decision: Tailwind CSS v4 + shadcn/ui

**Rationale**:
- Utility-first approach enables rapid UI development
- Design token support via CSS variables (required by constitution DS-02)
- shadcn/ui provides accessible, customizable primitives
- Dark theme support built-in
- Zero runtime CSS (all generated at build time)

**Alternatives Considered**:
- Material UI: Heavier bundle, harder to customize
- Chakra UI: Runtime CSS, slower performance
- Plain CSS Modules: Slower development, less consistency

### Decision: NextAuth.js v5

**Rationale**:
- JWT-based authentication (matches backend API key strategy)
- Built-in session management and middleware
- Easy integration with existing backend
- Callback-based customization for API key auth
- Secure cookie handling

**Alternatives Considered**:
- Auth.js: Lower-level, more config
- Clerk: Third-party hosted, less control
- Custom auth: Security risks, more maintenance

### Decision: TanStack Query v5

**Rationale**:
- Automatic caching reduces API calls
- Optimistic updates (required by constitution FA-04)
- Background refetching for fresh data
- Devtools for debugging
- Works perfectly with Server Components

**Alternatives Considered**:
- SWR: Simpler but fewer features
- Redux Query: More complex, larger bundle
- Custom hooks: More maintenance, less features

### Decision: Recharts

**Rationale**:
- React-native (declarative) API
- Responsive charts out-of-box
- Small bundle size (~50KB gzipped)
- Good TypeScript support
- Customizable styling via Tailwind

**Alternatives Considered**:
- Chart.js: Canvas-based, less React-friendly
- Victory: Larger bundle
- D3: Steep learning curve, overkill

### Decision: react-markdown + rehype-highlight

**Rationale**:
- Lightweight Markdown rendering
- Syntax highlighting via rehype-highlight (Prism)
- React component-based
- Supports custom components for extensions
- Security: Sanitizes HTML by default

**Alternatives Considered**:
- marked: Faster but no React integration
- remark: More plugins but complex
- MDX: Overkill for simple content

### Best Practice: Server Components First

**Pattern**: All pages are Server Components by default. Use "use client" only when:
- State management needed (useState, useReducer)
- Event handlers (onClick, onChange)
- Browser APIs (localStorage, window)
- Third-party components without SSR

**Rationale**: 
- Reduced bundle size (server code not shipped)
- Direct database/API access on server
- Progressive enhancement
- Better SEO

### Best Practice: Optimistic Updates

**Pattern**: For progress updates, quiz submissions:
```typescript
const mutation = useMutation({
  mutationFn: updateProgress,
  onMutate: async (newData) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: ['progress'] });
    
    // Snapshot previous value
    const previous = queryClient.getQueryData(['progress']);
    
    // Optimistically update
    queryClient.setQueryData(['progress'], newData);
    
    return { previous };
  },
  onError: (err, newData, context) => {
    // Rollback on error
    queryClient.setQueryData(['progress'], context.previous);
  },
});
```

**Rationale**: Instant UI feedback (constitution FA-04), better UX

### Best Practice: Route Protection Middleware

**Pattern**: Next.js middleware checks session on every request:
```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  const session = request.cookies.get('auth-token');
  
  if (!session && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
}
```

**Rationale**: Constitution FA-03 compliance, no unprotected routes

### Integration Pattern: Typed API Client

**Pattern**: Single source of truth for all API calls:
```typescript
// lib/api.ts
export const api = {
  chapters: {
    list: () => fetch<ChapterListResponse>('/chapters'),
    get: (id: string) => fetch<ChapterDetail>(`/chapters/${id}`),
  },
  // ... all endpoints typed
};
```

**Rationale**: Type safety, centralized error handling, easy testing

---

## Phase 1: Design & Contracts

### Data Model (Frontend Types)

**Location**: `frontend/types/api.ts`

```typescript
// User & Authentication
export interface User {
  id: string;
  email: string;
  name: string;
  tier: 'free' | 'premium' | 'pro';
  created_at: string;
}

export interface Session {
  user: User;
  token: string;
  expires_at: string;
}

// Chapters
export interface Chapter {
  id: string; // e.g., "ch-001"
  title: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  estimated_read_time: number; // minutes
  content: string; // Markdown
  sequence_order: number;
  is_locked: boolean;
  status?: 'not_started' | 'in_progress' | 'completed';
  quiz_score?: number;
}

export interface ChapterListResponse {
  data: Chapter[];
  meta: { total: number };
}

// Quizzes
export interface QuizQuestion {
  id: string;
  question_text: string;
  options: string[]; // 4 options
  correct_answer: number; // 0-3
}

export interface QuizSubmission {
  answers: Record<string, number>; // question_id -> option_index
}

export interface QuizResult {
  score: number; // e.g., 4
  total: number; // e.g., 5
  percentage: number; // e.g., 80
  correct_answers: string[]; // question_ids
  explanations: Record<string, string>; // question_id -> explanation
}

// Progress
export interface ProgressSummary {
  user_id: string;
  chapters_completed: number;
  total_chapters: number;
  overall_progress: number; // percentage 0-100
  best_quiz_score: number;
  total_study_time: number; // minutes
  current_streak: number; // days
  longest_streak: number; // days
  daily_activity: DailyActivity[];
}

export interface DailyActivity {
  date: string; // YYYY-MM-DD
  chapters_completed: number;
  quizzes_taken: number;
  study_time: number; // minutes
}

// Adaptive Learning Path (Phase 2)
export interface AdaptiveRecommendation {
  recommended_chapters: RecommendedChapter[];
  weak_areas: string[];
  strengths: string[];
  overall_assessment: string;
  suggested_daily_minutes: number;
  generated_at: string;
}

export interface RecommendedChapter {
  chapter_id: string;
  reason: string;
  priority: number; // 1-5
}

// LLM Usage (Phase 2)
export interface CostSummary {
  user_id: string;
  month: string; // YYYY-MM
  total_cost_usd: number;
  feature_breakdown: FeatureCost[];
}

export interface FeatureCost {
  feature_name: string;
  calls: number;
  cost_usd: number;
}

// API Response Envelope
export interface APIResponse<T> {
  data: T;
  error: null | { code: string; message: string };
  meta?: Record<string, any>;
}
```

### API Contracts

**Location**: `frontend/contracts/api.md`

All contracts map to existing Phase 1 + Phase 2 backend endpoints:

```markdown
# API Contracts (Frontend → Backend)

## Authentication

### POST /api/auth/signin
**Request**: { email: string, password: string }
**Response**: { user: User, token: string }
**Auth**: None
**Tier**: All

### POST /api/auth/signup
**Request**: { email: string, password: string, name: string }
**Response**: { user: User, token: string }
**Auth**: None
**Tier**: All

### POST /api/auth/signout
**Request**: {}
**Response**: { success: boolean }
**Auth**: Required
**Tier**: All

## Chapters

### GET /chapters
**Request**: {}
**Response**: ChapterListResponse
**Auth**: Required
**Tier**: All

### GET /chapters/{id}
**Request**: {}
**Response**: ChapterDetailResponse
**Auth**: Required
**Tier**: Free (1-3), Premium (4-5)

### GET /chapters/{id}/next
**Request**: {}
**Response**: ChapterMeta | null
**Auth**: Required
**Tier**: All

### GET /chapters/{id}/prev
**Request**: {}
**Response**: ChapterMeta | null
**Auth**: Required
**Tier**: All

## Quizzes

### GET /quizzes/{chapter_id}
**Request**: {}
**Response**: QuizQuestion[]
**Auth**: Required
**Tier**: All

### POST /quizzes/{chapter_id}/submit
**Request**: QuizSubmission
**Response**: QuizResult
**Auth**: Required
**Tier**: All

## Progress

### GET /progress/{user_id}
**Request**: {}
**Response**: ProgressSummary
**Auth**: Required (user_id from session)
**Tier**: All

### PUT /progress/{user_id}/chapter/{chapter_id}
**Request**: { status: 'completed', quiz_score?: number }
**Response**: { success: boolean }
**Auth**: Required (user_id from session)
**Tier**: All

## Adaptive Path (Phase 2 - Premium Only)

### POST /adaptive/learning-path
**Request**: {}
**Response**: AdaptiveRecommendation
**Auth**: Required
**Tier**: Premium/Pro only (403 for Free)

### GET /adaptive/learning-path/latest
**Request**: {}
**Response**: AdaptiveRecommendation
**Auth**: Required
**Tier**: Premium/Pro only

## Assessments (Phase 2 - Premium Only)

### GET /assessments/{chapter_id}/questions
**Request**: {}
**Response**: AssessmentQuestion[]
**Auth**: Required
**Tier**: Premium/Pro only

### POST /assessments/{chapter_id}/submit
**Request**: { answer_text: string }
**Response**: AssessmentResult
**Auth**: Required
**Tier**: Premium/Pro only

## Users

### GET /users/me
**Request**: {}
**Response**: UserProfile
**Auth**: Required
**Tier**: All

### GET /users/me/cost-summary
**Request**: {}
**Response**: CostSummary
**Auth**: Required
**Tier**: All (Free sees $0)
```

### Quickstart Guide

**Location**: `frontend/QUICKSTART.md`

```markdown
# Quickstart: Phase 3 Web Application

## Prerequisites

- Node.js 20.x or later
- npm, yarn, or pnpm
- Backend API running (Phase 1 + Phase 2)

## Installation

```bash
# Clone repository
cd Phase-III

# Install dependencies
cd frontend
npm install

# Copy environment variables
cp .env.local.example .env.local

# Edit .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_SECRET=your-secret-key-here
NEXTAUTH_URL=http://localhost:3000
```

## Development

```bash
# Start development server
npm run dev

# Open http://localhost:3000
```

## Build

```bash
# Production build
npm run build

# Start production server
npm start
```

## Testing

```bash
# Run unit tests
npm test

# Run E2E tests
npm run test:e2e
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | Yes |
| `NEXTAUTH_SECRET` | NextAuth JWT secret | Yes |
| `NEXTAUTH_URL` | App URL (for callbacks) | Yes |

## Route Map

- `/` - Landing page (public)
- `/login` - Login page (public)
- `/register` - Register page (public)
- `/dashboard` - Student dashboard (protected)
- `/course` - Course overview (protected)
- `/course/[id]` - Chapter reader (protected)
- `/course/[id]/quiz` - Quiz page (protected)
- `/learning-path` - Adaptive path (premium only)
- `/progress` - Progress analytics (protected)
- `/settings` - Settings (protected)
```

---

## Constitution Check (Post-Design)

Re-evaluating after design completion:

### Phase 1 Principles
- ✅ Zero-Backend-LLM: Frontend doesn't add backend LLM calls
- ✅ Determinism: All frontend logic is rule-based
- ✅ Content Verbatim: Markdown renderer preserves content
- ✅ Progress Persistence: Uses existing database via APIs
- ✅ Single Responsibility: Components are modular
- ✅ Freemium Enforcement: Frontend gate + backend gate

### Phase 2 Principles
- ✅ Hybrid Selectivity: Premium features remain gated
- ✅ Architectural Separation: Frontend separate from backend
- ✅ Cost Control: LLM usage displayed via API
- ✅ Premium Gate: Frontend shows gate, backend enforces

### Phase 3 Principles
- ✅ App Router Only: All pages use App Router
- ✅ Server-Side Data Fetching: Server Components fetch data
- ✅ Route Protection: Middleware protects all routes
- ✅ Optimistic UI: TanStack Query optimistic updates
- ✅ Zero Broken States: Loading, empty, error states on all pages
- ✅ Dark-First Theme: CSS variables define dark theme
- ✅ Design Token Consistency: All values via CSS variables
- ✅ Component Library: shadcn/ui base
- ✅ Typography Hierarchy: Sora + DM Sans + JetBrains Mono
- ✅ Accessibility: Keyboard navigation, alt text, contrast ≥4.5:1
- ✅ Performance: Lighthouse ≥90, FCP <1.5s, TTI <3.0s

**GATE STATUS**: ✅ PASS - All constitution principles satisfied

---

## Next Steps

1. **Run /sp.tasks**: Generate implementation task list
2. **Scaffold Next.js project**: `npx create-next-app@latest`
3. **Install dependencies**: shadcn/ui, TanStack Query, Zustand
4. **Implement components**: Follow task list
5. **Test**: Unit tests, integration tests, E2E tests
6. **Deploy**: Vercel (frontend), Fly.io (backend)

**Branch**: `3-phase-3-web-app`
**Plan Location**: `specs/003-phase-3-web-app/plan.md`
**Artifacts Generated**:
- ✅ research.md (Phase 0)
- ✅ data-model.md (Phase 1 types)
- ✅ contracts/api.md (Phase 1 API contracts)
- ✅ quickstart.md (Phase 1 setup guide)
