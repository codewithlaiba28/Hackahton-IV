# Demo Video Script: Course Companion FTE - Complete (Phase 1 + Phase 2)

**Duration:** 5 minutes
**Phases:** Phase 1 (Zero-Backend-LLM) + Phase 2 (Hybrid Intelligence)

---

## Segment 1: Introduction (0:00 - 0:30)

### Visual: Title slide with project name and team

**Script:**
> "Hi, I'm [Your Name] from Team [Team Name]. Today I'll demonstrate our Course Companion FTE - a dual-phase educational tutor built for the Panaversity Agent Factory Hackathon IV.
>
> Our Digital FTE teaches AI Agent Development with two modes:
> - **Phase 1:** Zero-Backend-LLM for cost-efficient core features
> - **Phase 2:** Selective Hybrid Intelligence for premium personalization
>
> Let me show you what we've built."

---

## Segment 2: Architecture Overview (0:30 - 1:00)

### Visual: Show architecture-diagram.svg with Phase 1 and Phase 2 highlighted

**Script:**
> "Our implementation follows a dual-phase architecture:
>
> **Phase 1 (Zero-Backend-LLM):**
> - ChatGPT handles ALL intelligence - explanations, tutoring, encouragement
> - FastAPI Backend is purely deterministic - serving content, grading quizzes, tracking progress
> - Zero LLM calls in the backend - verified by automated audits
> - Cost: $0.004 per user
>
> **Phase 2 (Hybrid Intelligence):**
> - Selective LLM calls for premium features only
> - Adaptive learning paths and LLM-graded assessments
> - Premium-gated, user-initiated, cost-tracked
> - Cost: $0.32 per premium user
>
> This achieves 99% cost savings for Phase 1, and 96.5% margins for Phase 2."

---

## Segment 3: Phase 1 Backend API Demo (1:00 - 2:00)

### Visual: Open Swagger UI at http://localhost:8000/docs

**Script:**
> "Here's our FastAPI backend with complete API documentation.
>
> We've implemented all 6 required Phase 1 features:
>
> 1. **Content Delivery** - GET /chapters serves course material
> 2. **Navigation** - GET /chapters/{id}/next for chapter sequencing
> 3. **Grounded Q&A** - GET /search for content search
> 4. **Rule-Based Quizzes** - POST /quizzes/{id}/submit with exact-match grading
> 5. **Progress Tracking** - GET and PUT /progress for completion tracking
> 6. **Freemium Gate** - GET /access/check enforces tier-based access"

### Visual: Test one endpoint (e.g., GET /chapters)

**Script:**
> "Let me test the chapters endpoint... You can see all 5 chapters returned with metadata.
>
> Notice the is_free flag - chapters 1-3 are free, chapters 4-5 require premium."

---

## Segment 4: ChatGPT App Demo - Phase 1 (2:00 - 2:45)

### Visual: ChatGPT interface with Course Companion

**Script:**
> "Now let's see the ChatGPT App in action for Phase 1 features.
>
> **Scenario 1: Content Explanation**"

### Visual: Type "Explain what an AI agent is"

**Script:**
> "I'm asking for an explanation. ChatGPT retrieves content from our backend and explains it at my level.
>
> Notice it's using the concept-explainer skill - providing analogies and checking understanding."

### Visual: Wait for response, show quality

**Script:**
> "Great explanation! Now let's test the quiz feature.
>
> **Scenario 2: Quiz Administration**"

### Visual: Type "Quiz me on Chapter 1"

**Script:**
> "ChatGPT fetches questions from our backend WITHOUT showing answers.
>
> After I answer, it submits to the backend for rule-based grading.
>
> The backend returns the score, and ChatGPT provides encouragement and explains mistakes."

---

## Segment 5: Phase 2 Hybrid Features Demo (2:45 - 3:45)

### Visual: Switch to premium user account

**Script:**
> "Now let me demonstrate Phase 2 hybrid features. I'm logged in as a Pro tier user.
>
> **Feature A: Adaptive Learning Path**"

### Visual: Type "What should I study next based on my performance?"

**Script:**
> "I'm requesting a personalized learning path. ChatGPT calls our Phase 2 endpoint:
>
> POST /api/v2/adaptive/learning-path
>
> The backend LLM analyzes my quiz performance, identifies knowledge gaps, and generates a personalized recommendation.
>
> This costs $0.0135 per request but delivers clear educational value."

### Visual: Show the adaptive path response

**Script:**
> "Perfect! The recommendation suggests reviewing Chapter 2 (where I scored 60%) before moving to Chapter 4.
>
> **Feature B: LLM-Graded Assessments**"

### Visual: Type "I want a written test on Chapter 1"

**Script:**
> "Now I'm requesting a deeper assessment. ChatGPT fetches open-ended questions from our Phase 2 endpoint.
>
> Let me submit a written answer... The backend LLM grades it with detailed feedback, identifying correct and missing concepts.
>
> This costs $0.0105 per submission but provides much deeper evaluation than MCQ."

---

## Segment 6: Cost Transparency & Freemium Gate (3:45 - 4:15)

### Visual: Show cost summary endpoint

**Script:**
> "Phase 2 includes cost transparency. Let me check my monthly usage:
>
> GET /api/v2/users/me/cost-summary
>
> This shows:
> - Adaptive Path: 3 calls ($0.04)
> - Assessments: 8 submissions ($0.08)
> - Total: $0.12 of my $5 Pro budget"

### Visual: Switch to free user account, try Phase 2 feature

**Script:**
> "Now as a free user, let me try to access the adaptive path feature...
>
> The backend returns 403 Forbidden with a clear upgrade message.
>
> ChatGPT gracefully explains the premium benefit without being pushy."

---

## Segment 7: Conclusion (4:15 - 5:00)

### Visual: Return to title slide with metrics

**Script:**
> "To summarize our complete implementation:
>
> **Phase 1 (Zero-Backend-LLM):**
> ✅ Zero LLM calls in backend - verified
> ✅ All 6 required features implemented
> ✅ 5 chapters with 8000+ words
> ✅ 25 MCQ quiz questions
> ✅ 4 Agent Skills in ChatGPT
> ✅ Cost: $0.004 per user (99% savings)
>
> **Phase 2 (Hybrid Intelligence):**
> ✅ 2 premium features (Adaptive Path + Assessments)
> ✅ Constitutional compliance verified
> ✅ Cost tracking and transparency
> ✅ 96.5% gross margins
> ✅ Clear educational value justification
>
> **Total Score Potential: 64/65 points (98%)**
>
> We're production-ready! Thank you. Questions?"

---

## Recording Tips

### Screen Setup
1. **Resolution:** 1920x1080 (Full HD)
2. **Browser:** Chrome with DevTools closed
3. **Theme:** Dark mode for better contrast
4. **Zoom:** 100% for readability

### Audio
- Use a quiet room
- Speak clearly at moderate pace
- Test microphone levels first
- Consider using a script reader app

### Tools
- **OBS Studio** (free) for screen recording
- **Loom** for quick recordings with narration
- **Zoom** (record yourself) as backup

### Editing (Optional)
- **DaVinci Resolve** (free) for professional editing
- Add transitions between segments
- Include text overlays for key points
- Background music (low volume)

---

## Checklist Before Recording

- [ ] Backend server running (`uvicorn app.main:app --reload`)
- [ ] Database seeded with chapters and quizzes
- [ ] ChatGPT App configured and tested
- [ ] Swagger UI accessible at localhost:8000/docs
- [ ] Test user API key ready
- [ ] Script printed/rehearsed
- [ ] Audio tested
- [ ] Screen resolution set to 1920x1080
- [ ] Notifications disabled
- [ ] Browser bookmarks ready

---

## Submission File

**Filename:** `demo-video-phase1.mp4`
**Format:** MP4, H.264 codec
**Max Size:** 50MB (upload to Google Drive if larger)
**Duration:** 4:30 - 5:30 minutes

---

*Good luck with your submission! 🚀*
