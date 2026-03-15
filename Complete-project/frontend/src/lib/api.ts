import {
  APIResponse,
  ChapterListResponse,
  ChapterDetail,
  ChapterMeta,
  QuizQuestion,
  QuizSubmission,
  QuizResult,
  ProgressSummary,
  AdaptiveRecommendation,
  AssessmentQuestion,
  AssessmentResult,
  CostSummary,
  User,
} from '@/types/api';

const API_BASE = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000').replace(/\/+$/, '');

// Helper function for typed fetch with API key
async function fetchWithAuth<T>(
  endpoint: string,
  options: RequestInit = {},
  apiKey?: string
): Promise<APIResponse<T>> {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(apiKey ? { 'X-API-Key': apiKey } : {}),
    ...options.headers,
  };

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

export const api = {
  // Chapters
  chapters: {
    list: (apiKey?: string) => fetchWithAuth<ChapterListResponse>('/chapters', {}, apiKey),
    get: (id: string, apiKey?: string) =>
      fetchWithAuth<ChapterDetail>(`/chapters/${id}`, {}, apiKey),
    next: (id: string, apiKey?: string) =>
      fetchWithAuth<ChapterMeta | null>('/chapters/' + id + '/next', {}, apiKey),
    prev: (id: string, apiKey?: string) =>
      fetchWithAuth<ChapterMeta | null>('/chapters/' + id + '/prev', {}, apiKey),
  },

  // Quizzes
  quizzes: {
    get: (chapterId: string, apiKey?: string) =>
      fetchWithAuth<QuizQuestion[]>(`/quizzes/${chapterId}`, {}, apiKey),
    submit: (chapterId: string, answers: QuizSubmission, apiKey?: string) =>
      fetchWithAuth<QuizResult>(`/quizzes/${chapterId}/submit`, {
        method: 'POST',
        body: JSON.stringify(answers),
      }, apiKey),
  },

  // Progress
  progress: {
    get: (userId: string, apiKey?: string) =>
      fetchWithAuth<ProgressSummary>(`/progress/${userId}`, {}, apiKey),
    update: (userId: string, chapterId: string, status: string, apiKey?: string) =>
      fetchWithAuth<{ success: boolean }>(`/progress/${userId}/chapter/${chapterId}`, {
        method: 'PUT',
        body: JSON.stringify({ status }),
      }, apiKey),
  },

  // Adaptive Learning Path (Phase 2 - Premium)
  adaptive: {
    generate: (apiKey?: string) =>
      fetchWithAuth<AdaptiveRecommendation>('/api/v2/adaptive/learning-path', {
        method: 'POST',
      }, apiKey),
    latest: (apiKey?: string) =>
      fetchWithAuth<AdaptiveRecommendation>('/api/v2/adaptive/learning-path/latest', {}, apiKey),
  },

  // Assessments (Phase 2 - Premium)
  assessments: {
    questions: (chapterId: string, apiKey?: string) =>
      fetchWithAuth<AssessmentQuestion[]>(`/api/v2/assessments/${chapterId}/questions`, {}, apiKey),
    submit: (chapterId: string, questionId: string, answerText: string, apiKey?: string) =>
      fetchWithAuth<AssessmentResult>(`/api/v2/assessments/${chapterId}/submit`, {
        method: 'POST',
        body: JSON.stringify({ answer_text: answerText, question_id: questionId }),
      }, apiKey),
    results: (chapterId: string, apiKey?: string) =>
      fetchWithAuth<AssessmentResult[]>(`/api/v2/assessments/${chapterId}/results`, {}, apiKey),
  },

  // Users
  users: {
    me: (apiKey?: string) => fetchWithAuth<User>('/users/me', {}, apiKey),
    getCostSummary: (apiKey?: string) =>
      fetchWithAuth<CostSummary>('/users/me/cost-summary', { headers: apiKey ? { 'X-API-Key': apiKey } : {} }),
    upgrade: (apiKey?: string) =>
      fetchWithAuth<User>('/users/me/upgrade', { method: 'POST', headers: apiKey ? { 'X-API-Key': apiKey } : {} }),
  },

  // Search
  search: {
    query: (query: string, apiKey?: string) =>
      fetchWithAuth<any[]>(`/search?q=${encodeURIComponent(query)}`, {
        method: 'GET'
      }, apiKey),
  },

  // Auth (Phase 3 backend endpoints)
  auth: {
    register: (email: string, password: string, name: string, tier: string = 'free') =>
      fetchWithAuth<{ user_id: string; api_key: string; tier: string; name: string }>(
        '/auth/register',
        {
          method: 'POST',
          body: JSON.stringify({ email, password, name, tier }),
        }
      ),
    login: (email: string, password: string) =>
      fetchWithAuth<{ user_id: string; api_key: string; tier: string; name: string }>(
        '/auth/login',
        {
          method: 'POST',
          body: JSON.stringify({ email, password }),
        }
      ),
  },
};
