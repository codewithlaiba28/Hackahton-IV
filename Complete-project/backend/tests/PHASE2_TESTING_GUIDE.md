# Phase 2 Testing Guide

**Date:** March 12, 2026
**Status:** Ready for Testing

---

## 📋 Overview

This guide covers comprehensive testing of Phase 2 Hybrid Features for both **Free** and **Premium/Pro** tiers.

### Test Categories

1. **Automated Tests** (Pytest) - 15 test cases
2. **Manual API Tests** (Swagger UI)
3. **Integration Tests** (ChatGPT App)

---

## 🧪 Automated Tests

### Run All Phase 2 Tests

```bash
cd backend

# Run all Phase 2 tests
python -m pytest tests/test_phase2.py -v

# Run with coverage
python -m pytest tests/test_phase2.py -v --cov=app --cov-report=html

# Run specific test category
python -m pytest tests/test_phase2.py -v -k "free_user"
python -m pytest tests/test_phase2.py -v -k "premium_user"
python -m pytest tests/test_phase2.py -v -k "cost"
```

### Test Breakdown

| Test ID | Test Name | Tier | Expected Result |
|---------|-----------|------|-----------------|
| T001 | Free user cannot access adaptive path | Free | 403 Forbidden |
| T002 | Premium user can access adaptive path | Premium | 200 OK + LLM call |
| T003 | Pro user can access adaptive path | Pro | 200 OK + LLM call |
| T004 | Free user cannot access assessments | Free | 403 Forbidden |
| T005 | Premium user can access assessments | Premium | 200 OK (no criteria exposed) |
| T006 | Free user cannot submit assessment | Free | 403 Forbidden |
| T007 | Premium user can submit assessment | Premium | 200 OK + graded result |
| T008 | Assessment rejects short answer | Premium | 422 (< 20 words) |
| T009 | Assessment rejects long answer | Premium | 422 (> 500 words) |
| T010 | Free user cost summary is zero | Free | 200 OK, $0.00 |
| T011 | Premium user cost summary | Premium | 200 OK, $2.00 cap |
| T012 | Pro user cost summary | Pro | 200 OK, $5.00 cap |
| T013 | Cached recommendation (no LLM) | Premium | 200 OK, cached |
| T014 | Phase 1 endpoints still work | All | 200 OK |
| T015 | Premium gate error message quality | Free | Clear upgrade message |

---

## 🔧 Manual API Testing (Swagger UI)

### Prerequisites

1. **Start Backend:**
   ```bash
   cd backend
   uv run uvicorn app.main:app --reload
   ```

2. **Open Swagger UI:**
   ```
   http://localhost:8000/docs
   ```

3. **Create Test Users:**
   ```bash
   # Run seed script or create via API
   # You'll need 3 API keys:
   - Free user API key: free_test_key_...
   - Premium user API key: premium_test_key_...
   - Pro user API key: pro_test_key_...
   ```

---

### Test Scenario 1: Free User - Phase 2 Access Denied

**Goal:** Verify free users cannot access hybrid features.

#### Step 1.1: Try Adaptive Learning Path

1. Open Swagger UI: `http://localhost:8000/docs`
2. Find endpoint: `POST /api/v2/adaptive/learning-path`
3. Click "Try it out"
4. Enter API key header: `X-API-Key: free_test_key_...`
5. Request body:
   ```json
   {"include_review": true}
   ```
6. Click "Execute"

**Expected Result:**
```json
{
  "detail": {
    "error": "PREMIUM_REQUIRED",
    "message": "Adaptive learning paths are a premium feature. Upgrade to access."
  }
}
```
**Status:** 403 Forbidden ✅

#### Step 1.2: Try Assessment Questions

1. Find endpoint: `GET /api/v2/assessments/{chapter_id}/questions`
2. Enter chapter_id: `ch-001`
3. Enter API key: `X-API-Key: free_test_key_...`
4. Click "Execute"

**Expected Result:**
```json
{
  "detail": {
    "error": "PREMIUM_REQUIRED",
    "message": "LLM-graded assessments are a premium feature. Upgrade to access."
  }
}
```
**Status:** 403 Forbidden ✅

#### Step 1.3: Try Cost Summary

1. Find endpoint: `GET /api/v2/users/me/cost-summary`
2. Enter API key: `X-API-Key: free_test_key_...`
3. Click "Execute"

**Expected Result:**
```json
{
  "data": {
    "month": "2026-03-01",
    "total_cost_usd": 0.0,
    "breakdown": [],
    "monthly_cap": 0.0,
    "remaining_budget": 0.0
  }
}
```
**Status:** 200 OK ✅

---

### Test Scenario 2: Premium User - Full Access

**Goal:** Verify premium users can access all Phase 2 features.

#### Step 2.1: Access Adaptive Learning Path

1. Find endpoint: `POST /api/v2/adaptive/learning-path`
2. Enter API key: `X-API-Key: premium_test_key_...`
3. Request body:
   ```json
   {"include_review": true}
   ```
4. Click "Execute"

**Expected Result:**
```json
{
  "data": {
    "recommended_chapters": [
      {
        "chapter_id": "ch-002",
        "priority": 1,
        "reason": "Review based on quiz performance",
        "estimated_time_min": 15
      }
    ],
    "weak_areas": ["MCP basics"],
    "strengths": ["AI Agents"],
    "overall_assessment": "Good foundation, needs review",
    "suggested_daily_minutes": 25
  },
  "meta": {
    "llm_call": true,
    "cached": false
  }
}
```
**Status:** 200 OK ✅

#### Step 2.2: Get Assessment Questions

1. Find endpoint: `GET /api/v2/assessments/ch-001/questions`
2. Enter API key: `X-API-Key: premium_test_key_...`
3. Click "Execute"

**Expected Result:**
```json
{
  "data": [
    {
      "id": "uuid-here",
      "question_text": "Explain what an AI Agent is...",
      "difficulty": "conceptual"
    }
  ],
  "meta": {
    "criteria_exposed": false
  }
}
```

**CRITICAL CHECK:** `model_answer_criteria` MUST NOT be in response! ✅

#### Step 2.3: Submit Assessment Answer

1. Find endpoint: `POST /api/v2/assessments/ch-001/submit`
2. Enter API key: `X-API-Key: premium_test_key_...`
3. Request body:
   ```json
   {
     "question_id": "uuid-from-previous-step",
     "answer_text": "AI agents are autonomous systems that perceive their environment and act to achieve goals. They differ from traditional programs because they can learn and adapt. For example, a self-driving car uses sensors to perceive the road and actuators to control steering and braking. This perception-action loop is key to agency."
   }
   ```
4. Click "Execute"

**Expected Result:**
```json
{
  "data": {
    "score": 85,
    "grade": "B",
    "feedback": "Good explanation with relevant example...",
    "correct_concepts": ["autonomous systems", "perception-action loop"],
    "missing_concepts": ["goal-directed behavior"],
    "improvement_suggestions": "Consider mentioning...",
    "word_count": 67
  },
  "meta": {
    "llm_call": true
  }
}
```
**Status:** 200 OK ✅

#### Step 2.4: Check Cost Summary

1. Find endpoint: `GET /api/v2/users/me/cost-summary`
2. Enter API key: `X-API-Key: premium_test_key_...`
3. Click "Execute"

**Expected Result:**
```json
{
  "data": {
    "month": "2026-03-01",
    "total_cost_usd": 0.027,
    "breakdown": [
      {
        "feature_name": "adaptive_path",
        "calls": 1,
        "cost_usd": 0.0135
      },
      {
        "feature_name": "assessment_grading",
        "calls": 1,
        "cost_usd": 0.0105
      }
    ],
    "monthly_cap": 2.00,
    "remaining_budget": 1.973
  }
}
```
**Status:** 200 OK ✅

---

### Test Scenario 3: Validation Tests

#### Step 3.1: Too Short Answer (< 20 words)

1. Find endpoint: `POST /api/v2/assessments/ch-001/submit`
2. Enter API key: `X-API-Key: premium_test_key_...`
3. Request body:
   ```json
   {
     "question_id": "uuid",
     "answer_text": "AI agents are cool and smart."
   }
   ```
4. Click "Execute"

**Expected Result:**
```json
{
  "detail": {
    "error": "WORD_COUNT_TOO_LOW",
    "message": "Answer must be at least 20 words (got 6)"
  }
}
```
**Status:** 422 Unprocessable Entity ✅

#### Step 3.2: Too Long Answer (> 500 words)

1. Same endpoint
2. Submit 501 words

**Expected Result:**
```json
{
  "detail": {
    "error": "WORD_COUNT_TOO_HIGH",
    "message": "Answer must be at most 500 words (got 501)"
  }
}
```
**Status:** 422 Unprocessable Entity ✅

---

### Test Scenario 4: Caching Tests

#### Step 4.1: Get Cached Recommendation

1. First, call `POST /api/v2/adaptive/learning-path` (from Step 2.1)
2. Then call `GET /api/v2/adaptive/learning-path/latest`
3. Enter API key: `X-API-Key: premium_test_key_...`
4. Click "Execute"

**Expected Result:**
```json
{
  "data": {
    "recommended_chapters": [...],
    "weak_areas": [...],
    ...
  },
  "meta": {
    "llm_call": false,
    "cached": true
  }
}
```
**Status:** 200 OK ✅

**Verification:** No new LLM call was made (cost unchanged).

---

### Test Scenario 5: Phase 1 Isolation

**Goal:** Verify Phase 1 endpoints work unchanged.

#### Step 5.1: Free User - Phase 1 Features

1. `GET /chapters` → 200 OK
2. `GET /chapters/ch-001` → 200 OK
3. `GET /search?q=AI` → 200 OK
4. `GET /quizzes/ch-001` → 200 OK
5. `GET /progress/{user_id}` → 200 OK

**All should work for free users!** ✅

---

## 📊 Test Results Checklist

### Free User Tests

- [ ] T001: Adaptive path → 403 Forbidden
- [ ] T004: Assessment questions → 403 Forbidden
- [ ] T006: Assessment submission → 403 Forbidden
- [ ] T010: Cost summary → $0.00
- [ ] T014: Phase 1 endpoints → 200 OK

### Premium User Tests

- [ ] T002: Adaptive path → 200 OK + LLM call
- [ ] T005: Assessment questions → 200 OK (no criteria)
- [ ] T007: Assessment submission → 200 OK + graded
- [ ] T008: Short answer → 422
- [ ] T009: Long answer → 422
- [ ] T011: Cost summary → $2.00 cap
- [ ] T013: Cached recommendation → no LLM call
- [ ] T014: Phase 1 endpoints → 200 OK

### Pro User Tests

- [ ] T003: Adaptive path → 200 OK
- [ ] T012: Cost summary → $5.00 cap

### Constitutional Compliance

- [ ] Principle VIII: Max 2 hybrid features ✅
- [ ] Principle VIII: Premium-gated only ✅
- [ ] Principle VIII: User-initiated ✅
- [ ] Principle IX: Phase 1 unchanged ✅
- [ ] Principle X: Cost tracking ✅
- [ ] Principle XII: Clear upgrade messages ✅

---

## 🐛 Common Issues & Solutions

### Issue 1: 401 Unauthorized

**Problem:** API key not recognized.

**Solution:**
```bash
# Check .env file
API_KEY=your-test-api-key

# Ensure header format is correct
X-API-Key: your-api-key
```

### Issue 2: 500 Internal Server Error (LLM)

**Problem:** Anthropic API key missing or invalid.

**Solution:**
```bash
# Check .env file
ANTHROPIC_API_KEY=sk-ant-...

# Verify key is valid at https://console.anthropic.com
```

### Issue 3: Database Not Migrated

**Problem:** Phase 2 tables missing.

**Solution:**
```bash
cd backend
python -m alembic upgrade head
```

### Issue 4: Assessment Questions Missing

**Problem:** No questions in database.

**Solution:**
```bash
# Run seed script
python -m seed.seed_assessments
```

---

## 📈 Performance Benchmarks

### Expected Response Times

| Endpoint | Expected Time | LLM Call |
|----------|---------------|----------|
| POST /adaptive/learning-path | 2-5 seconds | Yes |
| GET /adaptive/learning-path/latest | < 500ms | No |
| GET /assessments/{id}/questions | < 500ms | No |
| POST /assessments/{id}/submit | 3-7 seconds | Yes |
| GET /assessments/{id}/results | < 500ms | No |
| GET /users/me/cost-summary | < 500ms | No |

---

## ✅ Sign-Off Criteria

Phase 2 testing is complete when:

- [ ] All 15 automated tests pass
- [ ] All manual API tests pass
- [ ] Free users get 403 on all Phase 2 endpoints
- [ ] Premium/Pro users get 200 with correct responses
- [ ] Cost tracking is accurate
- [ ] model_answer_criteria never exposed
- [ ] Word count validation works
- [ ] Caching works (no unnecessary LLM calls)
- [ ] Phase 1 endpoints unchanged

---

**Ready to Test! 🚀**
