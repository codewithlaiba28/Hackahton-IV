# Research & Technology Decisions: Phase 3 Web Application

**Created**: 2026-03-12
**Feature**: Phase 3 Web Application
**Spec**: [spec.md](./spec.md)

---

## Technology Decisions

### 1. Framework: Next.js 15 (App Router)

**Decision**: Next.js 15 with App Router

**Rationale**:
- Server Components reduce bundle size by 40-50% vs client-side only
- Built-in SSR ensures FCP <1.5s (constitution requirement)
- Route groups enable clean public/protected separation
- Edge runtime ready for future scaling
- Official React 19 support (useOptimistic, useTransition)

**Alternatives Considered**:
| Framework | Pros | Cons | Why Rejected |
|-----------|------|------|--------------|
| Remix | Good SSR, loaders | Smaller ecosystem, less mature | Next.js has larger community |
| Vite + React | Fast HMR, simple | No SSR out-of-box, more config | Would need custom SSR setup |
| Next.js Pages | Stable, familiar | Legacy, no App Router benefits | App Router is future-proof |

**References**:
- [Next.js 15 Documentation](https://nextjs.org/docs)
- [App Router vs Pages Router](https://nextjs.org/docs/app)

---

### 2. Styling: Tailwind CSS v4 + shadcn/ui

**Decision**: Tailwind CSS v4 with shadcn/ui component library

**Rationale**:
- Utility-first enables rapid development
- Design tokens via CSS variables (constitution DS-02)
- shadcn/ui provides accessible primitives (constitution DS-03)
- Dark theme support built-in
- Zero runtime CSS (all build-time generated)
- shadcn components are copy-paste, not npm dependencies

**Alternatives Considered**:
| Library | Pros | Cons | Why Rejected |
|---------|------|------|--------------|
| Material UI | Complete, polished | Heavy bundle (200KB+), hard to customize | Bundle size, customization limits |
| Chakra UI | Easy to use, accessible | Runtime CSS, slower performance | Performance concerns |
| Plain CSS Modules | Full control, no deps | Slower development, less consistency | Development speed |

**References**:
- [Tailwind CSS v4](https://tailwindcss.com/)
- [shadcn/ui](https://ui.shadcn.com/)

---

### 3. Authentication: NextAuth.js v5

**Decision**: NextAuth.js v5 with JWT strategy

**Rationale**:
- JWT-based (matches backend API key strategy)
- Built-in session management
- Middleware for route protection (constitution FA-03)
- Callback-based customization for API key auth
- Secure cookie handling (HttpOnly, Secure flags)

**Alternatives Considered**:
| Solution | Pros | Cons | Why Rejected |
|----------|------|------|--------------|
| Auth.js | Lower-level, flexible | More configuration | NextAuth is higher-level |
| Clerk | Hosted, easy | Third-party dependency, cost | Want full control |
| Custom JWT | Full control | Security risks, maintenance | Security concerns |

**References**:
- [NextAuth.js v5](https://authjs.dev/)

---

### 4. Data Fetching: TanStack Query v5

**Decision**: TanStack Query (React Query) v5

**Rationale**:
- Automatic caching reduces API calls
- Optimistic updates (constitution FA-04)
- Background refetching keeps data fresh
- Devtools for debugging
- Works with Server Components (client-side state)

**Alternatives Considered**:
| Library | Pros | Cons | Why Rejected |
|---------|------|------|--------------|
| SWR | Simpler, lighter | Fewer features, no optimistic updates | Need optimistic UI |
| Redux Query | Powerful | Complex setup, larger bundle | Overkill for this use case |
| Custom hooks | Full control | More maintenance, less features | TanStack Query is standard |

**References**:
- [TanStack Query v5](https://tanstack.com/query/v5)

---

### 5. State Management: Zustand

**Decision**: Zustand for client-side state

**Rationale**:
- Lightweight (1KB gzipped)
- Simple API (no providers needed)
- TypeScript support
- Perfect for UI state (sidebar, modals)
- TanStack Query handles server state

**Alternatives Considered**:
| Library | Pros | Cons | Why Rejected |
|---------|------|------|--------------|
| Redux Toolkit | Powerful, devtools | Boilerplate, overkill | Too complex for UI state |
| Context API | Built-in, simple | Re-renders, no persistence | Zustand is simpler |
| Jotai | Atomic, reactive | Newer, smaller community | Zustand is more mature |

**References**:
- [Zustand](https://github.com/pmndrs/zustand)

---

### 6. Charts: Recharts

**Decision**: Recharts v2

**Rationale**:
- React-native (declarative) API
- Responsive out-of-box
- Small bundle (~50KB gzipped)
- Good TypeScript support
- Customizable via Tailwind

**Alternatives Considered**:
| Library | Pros | Cons | Why Rejected |
|---------|------|------|--------------|
| Chart.js | Popular, canvas-based | Less React-friendly | Prefer SVG-based |
| Victory | React-native | Larger bundle | Recharts is lighter |
| D3 | Powerful, flexible | Steep learning curve | Overkill for simple charts |

**References**:
- [Recharts](https://recharts.org/)

---

### 7. Markdown Rendering: react-markmark + rehype-highlight

**Decision**: react-markdown with rehype-highlight for syntax highlighting

**Rationale**:
- Lightweight rendering
- Syntax highlighting via rehype-highlight (Prism)
- React component-based
- Supports custom components
- Security: Sanitizes HTML by default

**Alternatives Considered**:
| Library | Pros | Cons | Why Rejected |
|---------|------|------|--------------|
| marked | Faster | No React integration | Need React components |
| remark | More plugins | Complex setup | react-markdown is simpler |
| MDX | Custom components | Overkill for simple content | Don't need MDX features |

**References**:
- [react-markdown](https://github.com/remarkjs/react-markdown)
- [rehype-highlight](https://github.com/rehypejs/rehype-highlight)

---

## Architecture Patterns

### Pattern 1: Server Components First

**Rule**: All pages are Server Components by default. Use "use client" only when:
- State management needed (useState, useReducer)
- Event handlers (onClick, onChange)
- Browser APIs (localStorage, window)
- Third-party components without SSR

**Example**:
```tsx
// ✅ Server Component (default)
export default async function ChapterPage({ params }) {
  const chapter = await fetchChapter(params.id);
  return <ChapterReader chapter={chapter} />;
}

// ❌ Client Component (only when needed)
'use client';
export function QuizTaker({ questions }) {
  const [answers, setAnswers] = useState({});
  return <Quiz questions={questions} answers={answers} />;
}
```

**Benefits**:
- Reduced bundle size (server code not shipped)
- Direct API access on server
- Progressive enhancement
- Better SEO

---

### Pattern 2: Optimistic Updates

**Rule**: For progress updates, quiz submissions, use optimistic UI.

**Example**:
```typescript
const mutation = useMutation({
  mutationFn: updateProgress,
  onMutate: async (newData) => {
    await queryClient.cancelQueries({ queryKey: ['progress'] });
    const previous = queryClient.getQueryData(['progress']);
    queryClient.setQueryData(['progress'], newData);
    return { previous };
  },
  onError: (err, newData, context) => {
    queryClient.setQueryData(['progress'], context.previous);
  },
});
```

**Benefits**:
- Instant UI feedback (constitution FA-04)
- Better UX (no loading spinners)
- Automatic rollback on error

---

### Pattern 3: Route Protection Middleware

**Rule**: All protected routes use Next.js middleware.

**Example**:
```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  const session = request.cookies.get('auth-token');
  
  if (!session && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
}
```

**Benefits**:
- Constitution FA-03 compliance
- No unprotected routes
- Centralized auth logic

---

### Pattern 4: Typed API Client

**Rule**: Single source of truth for all API calls.

**Example**:
```typescript
// lib/api.ts
export const api = {
  chapters: {
    list: () => fetch<ChapterListResponse>('/chapters'),
    get: (id: string) => fetch<ChapterDetail>(`/chapters/${id}`),
  },
  quizzes: {
    get: (chapterId: string) => fetch<QuizQuestion[]>(`/quizzes/${chapterId}`),
    submit: (chapterId: string, answers: QuizSubmission) =>
      post<QuizResult>(`/quizzes/${chapterId}/submit`, answers),
  },
};
```

**Benefits**:
- Type safety
- Centralized error handling
- Easy testing

---

## Performance Best Practices

### 1. Image Optimization

```tsx
import Image from 'next/image';

// ✅ Automatic optimization
<Image src="/hero.png" alt="Hero" width={800} height={600} priority />
```

### 2. Font Optimization

```tsx
import { Sora, DM_Sans, JetBrains_Mono } from 'next/font/google';

const sora = Sora({ subsets: ['latin'], variable: '--font-sora' });
const dmSans = DM_Sans({ subsets: ['latin'], variable: '--font-dm-sans' });
const jetbrainsMono = JetBrains_Mono({ subsets: ['latin'], variable: '--font-mono' });
```

### 3. Code Splitting

```tsx
// ✅ Dynamic imports for heavy components
const ConfettiEffect = dynamic(() => import('@/components/quiz/ConfettiEffect'), {
  ssr: false, // Only on client
  loading: () => <div>Loading...</div>,
});
```

### 4. Caching Strategy

```typescript
// TanStack Query configuration
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000, // 10 minutes
      retry: 1,
    },
  },
});
```

---

## Accessibility Checklist

- [ ] All interactive elements keyboard-navigable
- [ ] All images have alt text
- [ ] Color contrast ratio ≥ 4.5:1 for body text
- [ ] Focus indicators visible
- [ ] ARIA labels for icon buttons
- [ ] Semantic HTML (h1-h6, nav, main, footer)
- [ ] Skip to content link
- [ ] Form labels associated with inputs

---

## Testing Strategy

### Unit Tests (Jest + React Testing Library)

```typescript
// components/quiz/QuizQuestion.test.tsx
test('selects answer when option clicked', () => {
  render(<QuizQuestion question={mockQuestion} />);
  fireEvent.click(screen.getByText('Option A'));
  expect(screen.getByText('Option A')).toHaveClass('selected');
});
```

### Integration Tests (React Testing Library)

```typescript
// pages/dashboard.test.tsx
test('shows loading state while fetching', async () => {
  render(<DashboardPage />);
  expect(screen.getByTestId('loading-skeleton')).toBeInTheDocument();
  
  await waitFor(() => {
    expect(screen.getByText('Good morning')).toBeInTheDocument();
  });
});
```

### E2E Tests (Playwright)

```typescript
// tests/e2e/quiz-flow.spec.ts
test('complete quiz flow', async ({ page }) => {
  await page.goto('/course/ch-001/quiz');
  await page.click('[data-option="0"]');
  await page.click('button:has-text("Submit")');
  await expect(page.locator('[data-score]')).toBeVisible();
});
```

---

## Deployment Strategy

### Frontend: Vercel

```bash
# Connect GitHub repo to Vercel
# Automatic deployments on push to main
# Preview deployments on PRs
```

### Backend: Fly.io (existing)

```bash
# Already deployed from Phase 1
# Frontend uses NEXT_PUBLIC_API_URL to connect
```

### Environment Variables

**Production**:
```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXTAUTH_SECRET=<secure-random-string>
NEXTAUTH_URL=https://yourdomain.com
```

---

## References

- [Next.js Documentation](https://nextjs.org/docs)
- [React 19 Documentation](https://react.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com/)
- [TanStack Query Documentation](https://tanstack.com/query/latest)
- [NextAuth.js Documentation](https://authjs.dev/)
