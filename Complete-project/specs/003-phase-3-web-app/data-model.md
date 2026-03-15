# Data Model: Phase 3 Web Application

**Created**: 2026-03-12
**Feature**: Phase 3 Web Application
**Spec**: [spec.md](./spec.md)

---

## Frontend TypeScript Types

All types match existing Phase 1 + Phase 2 backend schemas.

### Authentication & Users

```typescript
// User profile
export interface User {
  id: string;
  email: string;
  name: string;
  tier: 'free' | 'premium' | 'pro';
  created_at: string; // ISO 8601
}

// Authentication session
export interface Session {
  user: User;
  token: string;
  expires_at: string; // ISO 8601
}

// User profile with stats
export interface UserProfile extends User {
  chapters_completed: number;
  total_study_time: number; // minutes
  account_created: string;
}
```

### Chapters

```typescript
// Chapter metadata
export interface ChapterMeta {
  id: string; // e.g., "ch-001"
  title: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  estimated_read_time: number; // minutes
  sequence_order: number;
  is_locked: boolean;
}

// Chapter with status (for course overview)
export interface Chapter extends ChapterMeta {
  status?: 'not_started' | 'in_progress' | 'completed';
  quiz_score?: number; // 0-100
}

// Full chapter detail (for reader)
export interface ChapterDetail extends Chapter {
  content: string; // Markdown
  previous_chapter?: ChapterMeta;
  next_chapter?: ChapterMeta;
}

// API response: list of chapters
export interface ChapterListResponse {
  data: Chapter[];
  meta: {
    total: number;
    free_chapters: number;
    premium_chapters: number;
  };
}

// API response: single chapter
export interface ChapterDetailResponse {
  data: ChapterDetail;
  error: null | { code: string; message: string };
}
```

### Quizzes

```typescript
// Quiz question (MCQ)
export interface QuizQuestion {
  id: string;
  question_text: string;
  options: string[]; // 4 options [A, B, C, D]
  correct_answer: number; // 0-3 (index of correct option)
}

// Quiz submission (user's answers)
export interface QuizSubmission {
  answers: Record<string, number>; // question_id -> option_index (0-3)
}

// Quiz results
export interface QuizResult {
  score: number; // e.g., 4
  total: number; // e.g., 5
  percentage: number; // e.g., 80
  correct_answers: string[]; // question_ids
  explanations: Record<string, string>; // question_id -> explanation
  passed: boolean; // true if percentage >= 80
}

// API response: quiz questions
export interface QuizQuestionsResponse {
  data: QuizQuestion[];
  meta: {
    chapter_id: string;
    total_questions: number;
  };
}
```

### Progress

```typescript
// Daily activity (for streak calendar)
export interface DailyActivity {
  date: string; // YYYY-MM-DD
  chapters_completed: number;
  quizzes_taken: number;
  study_time: number; // minutes
}

// Progress summary (for dashboard)
export interface ProgressSummary {
  user_id: string;
  chapters_completed: number;
  total_chapters: number;
  overall_progress: number; // percentage 0-100
  best_quiz_score: number; // highest score across all quizzes
  total_study_time: number; // minutes
  current_streak: number; // days
  longest_streak: number; // days
  daily_activity: DailyActivity[];
}

// Chapter progress update
export interface ProgressUpdate {
  status: 'not_started' | 'in_progress' | 'completed';
  quiz_score?: number; // 0-100
  completed_at?: string; // ISO 8601
}

// API response: progress summary
export interface ProgressResponse {
  data: ProgressSummary;
  meta: {
    last_updated: string;
  };
}
```

### Adaptive Learning Path (Phase 2 - Premium Only)

```typescript
// Recommended chapter in learning path
export interface RecommendedChapter {
  chapter_id: string;
  title: string;
  reason: string; // Why this chapter is recommended
  priority: number; // 1-5 (5 = highest priority)
  estimated_time: number; // minutes
}

// Adaptive learning path recommendation
export interface AdaptiveRecommendation {
  recommended_chapters: RecommendedChapter[];
  weak_areas: string[]; // Concepts needing improvement
  strengths: string[]; // Concepts mastered
  overall_assessment: string; // Summary of performance
  suggested_daily_minutes: number; // Recommended daily study time
  generated_at: string; // ISO 8601
}

// API response: adaptive recommendation
export interface AdaptiveRecommendationResponse {
  data: AdaptiveRecommendation;
  meta: {
    is_cached: boolean; // true if from cache, false if newly generated
    generated_at: string;
  };
  error?: {
    code: 'PREMIUM_REQUIRED' | 'LLM_UNAVAILABLE';
    message: string;
  };
}
```

### Assessments (Phase 2 - Premium Only)

```typescript
// Open-ended assessment question
export interface AssessmentQuestion {
  id: string;
  chapter_id: string;
  question_text: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  word_count_min: number; // e.g., 20
  word_count_max: number; // e.g., 500
}

// Assessment submission
export interface AssessmentSubmission {
  answer_text: string;
  word_count: number;
}

// Assessment grading result
export interface AssessmentResult {
  question_id: string;
  score: number; // 0-100
  grade: 'A' | 'B' | 'C' | 'D' | 'F';
  correct_concepts: string[]; // Concepts student understood
  missing_concepts: string[]; // Concepts student missed
  feedback: string; // Detailed feedback
  improvement_suggestions: string[]; // Actionable suggestions
}

// API response: assessment questions
export interface AssessmentQuestionsResponse {
  data: AssessmentQuestion[];
  meta: {
    chapter_id: string;
    total_questions: number;
  };
}
```

### LLM Usage (Phase 2 - Cost Transparency)

```typescript
// Cost breakdown by feature
export interface FeatureCost {
  feature_name: string; // e.g., "Adaptive Learning Path"
  calls: number; // number of API calls this month
  cost_usd: number; // total cost for this feature
}

// Monthly cost summary
export interface CostSummary {
  user_id: string;
  month: string; // YYYY-MM
  total_cost_usd: number;
  feature_breakdown: FeatureCost[];
  monthly_cap: number; // e.g., $2.00 for premium
  remaining_budget: number; // monthly_cap - total_cost_usd
}

// API response: cost summary
export interface CostSummaryResponse {
  data: CostSummary;
  meta: {
    last_updated: string;
  };
}
```

### API Response Envelope

```typescript
// Standard API response envelope
export interface APIResponse<T> {
  data: T;
  error: null | {
    code: string;
    message: string;
    details?: Record<string, any>;
  };
  meta?: Record<string, any>;
}

// Error types
export type APIErrorCode =
  | 'UNAUTHORIZED'
  | 'FORBIDDEN'
  | 'NOT_FOUND'
  | 'PREMIUM_REQUIRED'
  | 'VALIDATION_ERROR'
  | 'LLM_UNAVAILABLE'
  | 'SERVER_ERROR';
```

---

## Component Props Interfaces

### Layout Components

```typescript
// Navbar props
export interface NavbarProps {
  user: User | null;
  onLogout: () => void;
}

// Sidebar props
export interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  currentRoute: string;
  chapters: ChapterMeta[];
}

// Footer props
export interface FooterProps {
  className?: string;
}
```

### Course Components

```typescript
// Chapter card props
export interface ChapterCardProps {
  chapter: Chapter;
  onClick: (chapterId: string) => void;
  onUpgrade: () => void; // For locked chapters
}

// Chapter reader props
export interface ChapterReaderProps {
  chapter: ChapterDetail;
  onComplete: (chapterId: string) => void;
  onNavigate: (chapterId: string) => void;
}

// Markdown renderer props
export interface MarkdownRendererProps {
  content: string;
  className?: string;
}
```

### Quiz Components

```typescript
// Quiz question props
export interface QuizQuestionProps {
  question: QuizQuestion;
  selectedAnswer: number | null;
  onSelect: (optionIndex: number) => void;
  showResult: boolean; // true after submission
}

// Quiz results props
export interface QuizResultsProps {
  result: QuizResult;
  onRetake: () => void;
  onContinue: () => void;
}
```

### Progress Components

```typescript
// Progress ring props
export interface ProgressRingProps {
  progress: number; // 0-100
  size?: number; // pixels
  strokeWidth?: number;
}

// Streak calendar props
export interface StreakCalendarProps {
  dailyActivity: DailyActivity[];
  currentStreak: number;
}

// Achievement badge props
export interface AchievementBadgeProps {
  badge: {
    id: string;
    name: string;
    description: string;
    icon: string;
    earned: boolean;
  };
}
```

### Premium Components

```typescript
// Premium gate props
export interface PremiumGateProps {
  featureName: string;
  onUpgrade: () => void;
  className?: string;
}

// Upgrade modal props
export interface UpgradeModalProps {
  isOpen: boolean;
  onClose: () => void;
  onUpgrade: () => void;
}
```

---

## State Management Interfaces

### UI Store (Zustand)

```typescript
interface UIState {
  // Sidebar
  isSidebarOpen: boolean;
  openSidebar: () => void;
  closeSidebar: () => void;
  toggleSidebar: () => void;
  
  // Modals
  isUpgradeModalOpen: boolean;
  openUpgradeModal: () => void;
  closeUpgradeModal: () => void;
  
  // Theme (if light mode added in future)
  theme: 'dark' | 'light';
  setTheme: (theme: 'dark' | 'light') => void;
}
```

### Query Keys (TanStack Query)

```typescript
// Query key factory for type safety
export const queryKeys = {
  chapters: {
    all: ['chapters'] as const,
    list: () => [...queryKeys.chapters.all, 'list'] as const,
    detail: (id: string) => [...queryKeys.chapters.all, 'detail', id] as const,
  },
  quizzes: {
    all: ['quizzes'] as const,
    questions: (chapterId: string) => [...queryKeys.quizzes.all, 'questions', chapterId] as const,
  },
  progress: {
    all: ['progress'] as const,
    summary: (userId: string) => [...queryKeys.progress.all, 'summary', userId] as const,
  },
  adaptive: {
    all: ['adaptive'] as const,
    learningPath: () => [...queryKeys.adaptive.all, 'learning-path'] as const,
  },
  users: {
    all: ['users'] as const,
    me: () => [...queryKeys.users.all, 'me'] as const,
    costSummary: () => [...queryKeys.users.all, 'cost-summary'] as const,
  },
};
```

---

## Validation Rules

### Chapter Validation

```typescript
export const chapterValidation = {
  id: {
    pattern: /^ch-\d{3}$/,
    message: 'Chapter ID must be in format ch-XXX',
  },
  title: {
    minLength: 5,
    maxLength: 100,
  },
  estimated_read_time: {
    min: 1,
    max: 60,
  },
};
```

### Quiz Validation

```typescript
export const quizValidation = {
  answers: {
    minLength: 1, // At least one answer
    maxLength: 100, // Max 100 questions
  },
  option_index: {
    min: 0,
    max: 3, // Always 4 options (0-3)
  },
};
```

### Assessment Validation

```typescript
export const assessmentValidation = {
  answer_text: {
    word_count_min: 20,
    word_count_max: 500,
    validate: (text: string) => {
      const count = text.trim().split(/\s+/).length;
      return count >= 20 && count <= 500;
    },
  },
};
```

---

## References

- Phase 1 Backend Schemas: `backend/app/schemas/`
- Phase 2 Backend Schemas: `backend/app/schemas/adaptive.py`, `backend/app/schemas/assessment.py`
- Constitution: `.specify/memory/constitution.md`
