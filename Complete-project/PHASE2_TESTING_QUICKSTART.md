# Phase 2 Testing - Quick Start Guide

**TL;DR:** Phase 2 is complete. Here's how to test Free and Premium tiers.

---

## 🚀 Quick Test (5 minutes)

### Step 1: Start Backend

```bash
cd backend
uv run uvicorn app.main:app --reload
```

### Step 2: Open Swagger UI

```
http://localhost:8000/docs
```

### Step 3: Test Free User (2 minutes)

**Test 1: Try Adaptive Path (should fail with 403)**

1. Find: `POST /api/v2/adaptive/learning-path`
2. Click "Try it out"
3. Header: `X-API-Key: free_test_key`
4. Body: `{"include_review": true}`
5. Execute

**Expected:** 403 Forbidden with message about premium upgrade ✅

**Test 2: Try Assessment (should fail with 403)**

1. Find: `GET /api/v2/assessments/ch-001/questions`
2. Header: `X-API-Key: free_test_key`
3. Execute

**Expected:** 403 Forbidden ✅

---

### Step 4: Test Premium User (3 minutes)

**Test 3: Access Adaptive Path (should work with 200)**

1. Find: `POST /api/v2/adaptive/learning-path`
2. Header: `X-API-Key: premium_test_key`
3. Body: `{"include_review": true}`
4. Execute

**Expected:** 200 OK with personalized recommendation ✅

**Test 4: Access Assessment (should work with 200)**

1. Find: `GET /api/v2/assessments/ch-001/questions`
2. Header: `X-API-Key: premium_test_key`
3. Execute

**Expected:** 200 OK with questions (NO `model_answer_criteria`) ✅

**Test 5: Check Cost (should show $2 cap)**

1. Find: `GET /api/v2/users/me/cost-summary`
2. Header: `X-API-Key: premium_test_key`
3. Execute

**Expected:** 200 OK with `$2.00` monthly cap ✅

---

## 🧪 Automated Tests (1 minute)

```bash
cd backend
python -m pytest tests/test_phase2.py -v
```

**Expected:** All 15 tests pass ✅

---

## ✅ Test Checklist

### Free User
- [ ] Adaptive Path → 403
- [ ] Assessment Questions → 403
- [ ] Assessment Submit → 403
- [ ] Cost Summary → $0.00

### Premium User
- [ ] Adaptive Path → 200 + recommendation
- [ ] Assessment Questions → 200 (no criteria exposed)
- [ ] Assessment Submit → 200 + graded feedback
- [ ] Cost Summary → $2.00 cap

### Pro User
- [ ] Cost Summary → $5.00 cap

---

## 📋 Detailed Documentation

- **Full Testing Guide:** `backend/tests/PHASE2_TESTING_GUIDE.md`
- **Verification Report:** `PHASE2_VERIFICATION_REPORT.md`
- **Test Code:** `backend/tests/test_phase2.py`

---

## 🎯 Expected Results

### Free User Experience
- Can access Phase 1 features (chapters, quizzes, progress)
- Gets 403 on all Phase 2 endpoints
- Sees $0.00 cost (can't access hybrid features)

### Premium User Experience
- Can access ALL Phase 1 + Phase 2 features
- Gets personalized learning paths
- Gets LLM-graded assessments with feedback
- Sees cost tracking ($2 monthly cap)

### Pro User Experience
- Same as Premium, but $5 monthly cap
- More LLM calls allowed

---

## ⚠️ Common Issues

### Issue: 401 Unauthorized
**Fix:** Check API key format in header: `X-API-Key: your-key`

### Issue: 500 Error on Phase 2
**Fix:** Check `ANTHROPIC_API_KEY` in `.env`

### Issue: Database Error
**Fix:** Run migrations: `python -m alembic upgrade head`

---

**Ready to Test! 🚀**
