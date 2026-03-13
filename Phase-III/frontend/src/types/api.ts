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
  apiKey: string;
  expires_at: string;
}

export interface UserProfile extends User {
  chapters_completed: number;
  total_study_time: number;
  account_created: string;
}

// Chapters
export interface ChapterMeta {
  id: string;
  title: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  estimated_read_min: number;
  sequence_order: number;
  is_locked: boolean;
  prev_chapter_id?: string;
  next_chapter_id?: string;
}

export interface Chapter extends ChapterMeta {
  status?: 'not_started' | 'in_progress' | 'completed';
  quiz_score?: number;
}

export interface ChapterDetail extends Chapter {
  content: string;
}

export interface ChapterListResponse {
  chapters: Chapter[];
}

// Quizzes
export interface QuizQuestion {
  id: string;
  question_text: string;
  options: string[];
  correct_answer: number;
}

export interface QuizSubmission {
  answers: Record<string, number>;
}

export interface QuizResult {
  score: number;
  total: number;
  percentage: number;
  correct_answers: string[];
  explanations: Record<string, string>;
  passed: boolean;
}

// Progress
export interface DailyActivity {
  date: string;
  chapters_completed: number;
  quizzes_taken: number;
  study_time: number;
}

export interface ProgressSummary {
  user_id: string;
  chapters_completed: number;
  total_chapters: number;
  overall_progress: number;
  best_quiz_score: number;
  total_study_time: number;
  current_streak: number;
  longest_streak: number;
  daily_activity: DailyActivity[];
}

// Adaptive Learning Path (Phase 2)
export interface RecommendedChapter {
  chapter_id: string;
  title: string;
  reason: string;
  priority: number;
  estimated_time: number;
}

export interface AdaptiveRecommendation {
  recommended_chapters: RecommendedChapter[];
  weak_areas: string[];
  strengths: string[];
  overall_assessment: string;
  suggested_daily_minutes: number;
  generated_at: string;
}

// Assessments (Phase 2)
export interface AssessmentQuestion {
  id: string;
  chapter_id: string;
  question_text: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  word_count_min: number;
  word_count_max: number;
}

export interface AssessmentResult {
  question_id: string;
  score: number;
  grade: 'A' | 'B' | 'C' | 'D' | 'F';
  correct_concepts: string[];
  missing_concepts: string[];
  feedback: string;
  improvement_suggestions: string[];
}

// LLM Usage (Phase 2)
export interface FeatureCost {
  feature_name: string;
  calls: number;
  cost_usd: number;
}

export interface CostSummary {
  user_id: string;
  month: string;
  total_cost_usd: number;
  feature_breakdown: FeatureCost[];
  monthly_cap: number;
  remaining_budget: number;
}

// API Response Envelope
export interface APIResponse<T> {
  data: T;
  error: null | {
    code: string;
    message: string;
    details?: Record<string, any>;
  };
  meta?: Record<string, any>;
}
