# Quickstart: Phase 3 Web Application

**Created**: 2026-03-12
**Feature**: Phase 3 Web Application
**Spec**: [spec.md](./spec.md)

---

## Prerequisites

- **Node.js**: 20.x or later
- **Package Manager**: npm, yarn, or pnpm
- **Backend API**: Phase 1 + Phase 2 backend running on `http://localhost:8000`
- **Database**: PostgreSQL (backend dependency, already set up)

---

## Installation

### 1. Clone Repository

```bash
cd C:\Code-journy\Quator-4\Hackahton-IV\Phase-III
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 3. Configure Environment Variables

```bash
# Copy example env file
cp .env.local.example .env.local

# Edit .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_SECRET=your-secret-key-here
NEXTAUTH_URL=http://localhost:3000
```

**Generate NEXTAUTH_SECRET**:
```bash
# OpenSSL (Linux/Mac)
openssl rand -base64 32

# Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

### 4. Verify Backend is Running

```bash
# Test backend health
curl http://localhost:8000/health

# Expected: {"status": "healthy"}
```

---

## Development

### Start Development Server

```bash
cd frontend
npm run dev
```

**Access**: http://localhost:3000

**Features**:
- Hot Module Replacement (HMR)
- React DevTools
- TanStack Query DevTools (http://localhost:3000 → bottom-right icon)

---

## Build for Production

### Create Production Build

```bash
cd frontend
npm run build
```

### Start Production Server

```bash
npm start
```

**Access**: http://localhost:3000

---

## Testing

### Run Unit Tests

```bash
npm test
```

**Options**:
```bash
# Watch mode
npm run test:watch

# With coverage
npm run test:coverage

# Run specific test file
npm test -- ChapterCard.test.tsx
```

### Run E2E Tests

```bash
# Install Playwright browsers
npx playwright install

# Run E2E tests
npm run test:e2e
```

**Options**:
```bash
# With UI
npm run test:e2e -- --ui

# Specific test file
npm run test:e2e -- quiz-flow.spec.ts
```

---

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── (public)/          # Public pages (landing, login, register)
│   ├── (dashboard)/       # Protected pages (dashboard, course, progress)
│   ├── api/               # API routes (NextAuth)
│   ├── layout.tsx         # Root layout
│   └── globals.css        # Global styles
│
├── components/            # React components
│   ├── ui/               # shadcn/ui primitives
│   ├── layout/           # Navbar, Sidebar, Footer
│   ├── course/           # ChapterCard, ChapterReader, MarkdownRenderer
│   ├── quiz/             # QuizQuestion, QuizResults, ConfettiEffect
│   ├── progress/         # ProgressRing, StreakCalendar, Badges
│   └── premium/          # PremiumGate, UpgradeModal
│
├── lib/                   # Utilities
│   ├── api.ts            # Typed API client
│   ├── auth.ts           # NextAuth configuration
│   └── utils.ts          # cn(), formatters
│
├── hooks/                 # Custom hooks
│   ├── useProgress.ts    # TanStack Query hooks
│   ├── useChapters.ts
│   └── useQuiz.ts
│
├── store/                 # Zustand state
│   └── useUIStore.ts     # UI state (sidebar, modals)
│
├── types/                 # TypeScript types
│   └── api.ts            # API type definitions
│
└── Configuration files
    ├── next.config.ts
    ├── tailwind.config.ts
    ├── components.json
    └── .env.local.example
```

---

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server (port 3000) |
| `npm run build` | Build for production |
| `npm start` | Start production server |
| `npm test` | Run unit tests |
| `npm run test:watch` | Run tests in watch mode |
| `npm run test:coverage` | Run tests with coverage report |
| `npm run test:e2e` | Run E2E tests with Playwright |
| `npm run lint` | Run ESLint |
| `npm run lint:fix` | Fix ESLint errors |
| `npm run type-check` | Run TypeScript type checking |

---

## Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | Yes | `http://localhost:8000` |
| `NEXTAUTH_SECRET` | NextAuth JWT secret | Yes | `random-base64-string` |
| `NEXTAUTH_URL` | Application URL | Yes | `http://localhost:3000` |

**Production Environment**:
```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXTAUTH_SECRET=<secure-random-string>
NEXTAUTH_URL=https://yourdomain.com
```

---

## Route Map

### Public Routes (No Auth)

| Route | Page | Description |
|-------|------|-------------|
| `/` | Landing Page | Marketing page with CTA |
| `/features` | Features Page | Feature breakdown |
| `/pricing` | Pricing Page | Free vs Premium comparison |
| `/login` | Login Page | Email + password auth |
| `/register` | Register Page | New account creation |

### Protected Routes (Auth Required)

| Route | Page | Description | Tier |
|-------|------|-------------|------|
| `/dashboard` | Dashboard | Progress overview, next chapter | All |
| `/course` | Course Overview | All chapters with status | All |
| `/course/[id]` | Chapter Reader | Chapter content + navigation | All |
| `/course/[id]/quiz` | Quiz Page | MCQ quiz with timer | All |
| `/course/[id]/assessment` | Assessment Page | LLM-graded (premium) | Premium/Pro |
| `/learning-path` | Adaptive Path | Personalized study plan | Premium/Pro |
| `/progress` | Progress Page | Detailed analytics | All |
| `/settings` | Settings | Profile, subscription, usage | All |

---

## Common Issues & Solutions

### Issue: Backend Connection Error

**Error**: `Failed to fetch` or `ECONNREFUSED`

**Solution**:
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check NEXT_PUBLIC_API_URL in .env.local
echo $NEXT_PUBLIC_API_URL
```

### Issue: Authentication Not Working

**Error**: `UNAUTHORIZED` on protected routes

**Solution**:
```bash
# Verify NEXTAUTH_SECRET is set
echo $NEXTAUTH_SECRET

# Ensure it's at least 32 characters
echo -n $NEXTAUTH_SECRET | wc -c
```

### Issue: Build Fails with TypeScript Errors

**Error**: `Type error: Property 'X' does not exist on type 'Y'`

**Solution**:
```bash
# Run type check to see all errors
npm run type-check

# Check types/api.ts matches backend schemas
# Update types if backend changed
```

### Issue: Styles Not Loading

**Error**: Page renders without styling

**Solution**:
```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules
npm install

# Restart dev server
npm run dev
```

---

## Deployment

### Frontend: Vercel

1. **Connect GitHub Repository** to Vercel
2. **Set Environment Variables** in Vercel dashboard
3. **Deploy**: Automatic on push to `main` branch

```bash
# Install Vercel CLI (optional)
npm i -g vercel

# Deploy manually
vercel --prod
```

### Backend: Fly.io (Existing)

Backend already deployed from Phase 1/2. Update `NEXT_PUBLIC_API_URL` to production URL.

---

## Next Steps

1. **Run /sp.tasks**: Generate implementation task list
2. **Scaffold Next.js project**: `npx create-next-app@latest frontend`
3. **Install shadcn/ui**: `npx shadcn-ui@latest init`
4. **Install dependencies**: TanStack Query, Zustand, Recharts
5. **Implement components**: Follow task list
6. **Test**: Unit, integration, E2E tests
7. **Deploy**: Vercel (frontend), Fly.io (backend)

---

## References

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui](https://ui.shadcn.com/)
- [TanStack Query](https://tanstack.com/query/latest)
- [NextAuth.js](https://authjs.dev/)
- [Zustand](https://github.com/pmndrs/zustand)
- [Recharts](https://recharts.org/)
