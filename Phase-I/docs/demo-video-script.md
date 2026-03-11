# Demo Video Script: Course Companion FTE - Phase 1

**Duration:** 5 minutes
**Phase:** 1 (Zero-Backend-LLM)

---

## Segment 1: Introduction (0:00 - 0:30)

### Visual: Title slide with project name and team

**Script:**
> "Hi, I'm [Your Name] from Team [Team Name]. Today I'll demonstrate our Course Companion FTE - a Zero-Backend-LLM educational tutor built for the Panaversity Agent Factory Hackathon IV.
>
> Our Digital FTE teaches AI Agent Development, operating 24/7 at 99% cost savings compared to human tutors."

### Visual: Switch to architecture overview

**Script:**
> "Let me show you what we've built."

---

## Segment 2: Architecture Overview (0:30 - 1:00)

### Visual: Show architecture-diagram.svg

**Script:**
> "Our Phase 1 implementation follows the Zero-Backend-LLM architecture:
>
> - **ChatGPT App** handles ALL intelligence - explanations, tutoring, and encouragement
> - **FastAPI Backend** is purely deterministic - serving content, grading quizzes, tracking progress
> - **Zero LLM calls** in the backend - verified by automated audits
>
> This achieves a cost of just $0.004 per user compared to $50 for human tutoring."

---

## Segment 3: Backend API Demo (1:00 - 2:00)

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

## Segment 4: ChatGPT App Demo (2:00 - 3:30)

### Visual: ChatGPT interface with Course Companion

**Script:**
> "Now let's see the ChatGPT App in action. This is where all the intelligence lives.
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

### Visual: Complete one quiz question

**Script:**
> "Perfect! The quiz-master skill is working correctly."

---

## Segment 5: Freemium Gate Demo (3:30 - 4:00)

### Visual: Show access check with free user

**Script:**
> "Let's demonstrate the freemium gate.
>
> I'm logged in as a free user trying to access Chapter 4 (premium content).
>
> The backend returns 403 Forbidden with upgrade_required: true.
>
> ChatGPT gracefully explains the upgrade option without being pushy."

### Visual: Show the gate response

---

## Segment 6: Phase 2 Preview (4:00 - 4:30)

### Visual: Show Phase 2 architecture slide

**Script:**
> "For Phase 2, we're adding selective hybrid intelligence:
>
> - **Adaptive Learning Paths** - LLM analyzes patterns for personalized recommendations
> - **LLM-Graded Assessments** - Free-form answer evaluation
>
> Both features are premium-gated and user-initiated, maintaining our cost efficiency."

---

## Segment 7: Conclusion (4:30 - 5:00)

### Visual: Return to title slide with metrics

**Script:**
> "To summarize our Phase 1 achievements:
>
> ✅ Zero-Backend-LLM architecture - verified, no LLM calls
> ✅ All 6 required features implemented and tested
> ✅ 5 chapters with 8000+ words of content
> ✅ 25 quiz questions with explanations
> ✅ ChatGPT App with 4 Agent Skills
> ✅ Cost of $0.004 per user - 99% savings
>
> **We're ready for production!**
>
> Thank you. Questions?"

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
