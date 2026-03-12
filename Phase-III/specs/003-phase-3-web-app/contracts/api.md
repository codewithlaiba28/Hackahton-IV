# API Contracts: Phase 3 Web Application → Backend

**Created**: 2026-03-12
**Feature**: Phase 3 Web Application
**Spec**: [spec.md](./spec.md)

---

## Authentication Endpoints

### POST /api/auth/signin

Sign in with email and password.

**Request**:
```typescript
{
  email: string;
  password: string;
}
```

**Response**:
```typescript
{
  user: User;
  token: string;
  expires_at: string;
}
```

**Auth**: None  
**Tier**: All  
**Errors**: 401 (Invalid credentials), 422 (Validation error)

---

### POST /api/auth/signup

Create new account.

**Request**:
```typescript
{
  email: string;
  password: string;
  name: string;
}
```

**Response**:
```typescript
{
  user: User;
  token: string;
  expires_at: string;
}
```

**Auth**: None  
**Tier**: All  
**Errors**: 400 (Email already exists), 422 (Validation error)

---

### POST /api/auth/signout

Sign out and invalidate session.

**Request**:
```typescript
{}
```

**Response**:
```typescript
{
  success: boolean;
}
```

**Auth**: Required  
**Tier**: All  
**Errors**: 401 (Unauthorized)

---

## Chapters Endpoints

### GET /chapters

List all chapters with user's progress status.

**Request**:
```typescript
{}
```

**Response**:
```typescript
{
  data: Chapter[];
  meta: {
    total: number;
    free_chapters: number;
    premium_chapters: number;
  };
}
```

**Auth**: Required  
**Tier**: All  
**Errors**: 401 (Unauthorized)

---

### GET /chapters/{id}

Get single chapter detail with content.

**Request**:
```typescript
{
  id: string; // path parameter
}
```

**Response**:
```typescript
{
  data: ChapterDetail;
}
```

**Auth**: Required  
**Tier**: Free (ch-001 to ch-003), Premium/Pro (ch-004+)  
**Errors**: 401 (Unauthorized), 403 (Locked - free user), 404 (Not found)

---

### GET /chapters/{id}/next

Get next chapter in sequence.

**Request**:
```typescript
{
  id: string; // path parameter
}
```

**Response**:
```typescript
{
  data: ChapterMeta | null; // null if last chapter
}
```

**Auth**: Required  
**Tier**: All  
**Errors**: 401 (Unauthorized), 404 (Not found)

---

### GET /chapters/{id}/prev

Get previous chapter in sequence.

**Request**:
```typescript
{
  id: string; // path parameter
}
```

**Response**:
```typescript
{
  data: ChapterMeta | null; // null if first chapter
}
```

**Auth**: Required  
**Tier**: All  
**Errors**: 401 (Unauthorized), 404 (Not found)

---

## Quizzes Endpoints

### GET /quizzes/{chapter_id}

Get quiz questions for a chapter.

**Request**:
```typescript
{
  chapter_id: string; // path parameter
}
```

**Response**:
```typescript
{
  data: QuizQuestion[];
  meta: {
    chapter_id: string;
    total_questions: number;
  };
}
```

**Auth**: Required  
**Tier**: All  
**Errors**: 401 (Unauthorized), 403 (Locked chapter), 404 (Not found)

---

### POST /quizzes/{chapter_id}/submit

Submit quiz answers for grading.

**Request**:
```typescript
{
  chapter_id: string; // path parameter
  answers: Record<string, number>; // question_id -> option_index (0-3)
}
```

**Response**:
```typescript
{
  data: QuizResult;
}
```

**Auth**: Required  
**Tier**: All  
**Errors**: 401 (Unauthorized), 403 (Locked chapter), 422 (Validation error)

---

## Progress Endpoints

### GET /progress/{user_id}

Get user's progress summary.

**Request**:
```typescript
{
  user_id: string; // path parameter (from session)
}
```

**Response**:
```typescript
{
  data: ProgressSummary;
  meta: {
    last_updated: string;
  };
}
```

**Auth**: Required (user_id must match session)  
**Tier**: All  
**Errors**: 401 (Unauthorized), 403 (Wrong user_id)

---

### PUT /progress/{user_id}/chapter/{chapter_id}

Update chapter progress (mark as complete).

**Request**:
```typescript
{
  user_id: string; // path parameter
  chapter_id: string; // path parameter
  status: 'completed';
  quiz_score?: number; // 0-100
}
```

**Response**:
```typescript
{
  success: boolean;
}
```

**Auth**: Required (user_id must match session)  
**Tier**: All  
**Errors**: 401 (Unauthorized), 403 (Wrong user_id), 404 (Chapter not found)

---

## Adaptive Learning Path Endpoints (Phase 2 - Premium Only)

### POST /adaptive/learning-path

Generate personalized learning path.

**Request**:
```typescript
{}
```

**Response**:
```typescript
{
  data: AdaptiveRecommendation;
  meta: {
    is_cached: boolean;
    generated_at: string;
  };
}
```

**Auth**: Required  
**Tier**: Premium/Pro only  
**Errors**: 401 (Unauthorized), 403 (Free tier), 503 (LLM unavailable)

---

### GET /adaptive/learning-path/latest

Get cached learning path recommendation.

**Request**:
```typescript
{}
```

**Response**:
```typescript
{
  data: AdaptiveRecommendation;
  meta: {
    generated_at: string;
  };
}
```

**Auth**: Required  
**Tier**: Premium/Pro only  
**Errors**: 401 (Unauthorized), 403 (Free tier), 404 (No cached recommendation)

---

## Assessments Endpoints (Phase 2 - Premium Only)

### GET /assessments/{chapter_id}/questions

Get open-ended assessment questions.

**Request**:
```typescript
{
  chapter_id: string; // path parameter
}
```

**Response**:
```typescript
{
  data: AssessmentQuestion[];
  meta: {
    chapter_id: string;
    total_questions: number;
  };
}
```

**Auth**: Required  
**Tier**: Premium/Pro only  
**Errors**: 401 (Unauthorized), 403 (Free tier), 404 (Not found)

---

### POST /assessments/{chapter_id}/submit

Submit assessment answer for LLM grading.

**Request**:
```typescript
{
  chapter_id: string; // path parameter
  answer_text: string;
  word_count: number;
}
```

**Response**:
```typescript
{
  data: AssessmentResult;
}
```

**Auth**: Required  
**Tier**: Premium/Pro only  
**Errors**: 401 (Unauthorized), 403 (Free tier), 422 (Word count validation), 503 (LLM unavailable)

---

## Users Endpoints

### GET /users/me

Get current user profile.

**Request**:
```typescript
{}
```

**Response**:
```typescript
{
  data: UserProfile;
}
```

**Auth**: Required  
**Tier**: All  
**Errors**: 401 (Unauthorized)

---

### GET /users/me/cost-summary

Get monthly LLM usage cost breakdown.

**Request**:
```typescript
{}
```

**Response**:
```typescript
{
  data: CostSummary;
  meta: {
    last_updated: string;
  };
}
```

**Auth**: Required  
**Tier**: All (Free users see $0)  
**Errors**: 401 (Unauthorized)

---

## Error Response Format

All errors follow this format:

```typescript
{
  error: {
    code: string;
    message: string;
    details?: Record<string, any>;
  };
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `UNAUTHORIZED` | 401 | Missing or invalid authentication |
| `FORBIDDEN` | 403 | Valid auth but insufficient permissions |
| `PREMIUM_REQUIRED` | 403 | Feature requires premium tier |
| `NOT_FOUND` | 404 | Resource not found |
| `VALIDATION_ERROR` | 422 | Request validation failed |
| `LLM_UNAVAILABLE` | 503 | LLM service temporarily unavailable |
| `SERVER_ERROR` | 500 | Internal server error |

---

## Rate Limiting

| Endpoint | Rate Limit |
|----------|------------|
| /chapters/* | 100 requests/minute |
| /quizzes/* | 60 requests/minute |
| /progress/* | 100 requests/minute |
| /adaptive/* | 10 requests/minute (LLM cost) |
| /assessments/* | 20 requests/minute (LLM cost) |

---

## References

- Phase 1 API Documentation: `backend/app/routers/`
- Phase 2 API Documentation: `backend/app/routers/adaptive_path.py`, `backend/app/routers/assessments.py`
- OpenAPI Docs: `http://localhost:8000/docs` (when backend running)
