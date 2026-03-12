# Feature Specification: Phase 2 Hybrid Intelligence Layer

**Feature Branch**: `1-phase-2-hybrid-features`
**Created**: 2026-03-11
**Status**: Draft
**Input**: Complete Phase 2 Feature Specification - Adaptive Learning Path + LLM-Graded Assessments

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Premium Student Gets Personalized Study Plan (Priority: P1)

As a premium student, I want the Course Companion to analyze my learning patterns and generate a personalized study plan, so that I can focus my time on areas where I need the most improvement.

**Why this priority**: This is the core value proposition of Phase 2 - personalized learning at scale. Without this, the Pro tier has no differentiation from Premium.

**Independent Test**: Can be fully tested by a premium user requesting "What should I study next?" and receiving a structured, personalized recommendation with clear rationale.

**Acceptance Scenarios**:

1. **Given** a premium student has completed 3 chapters with quiz scores [85%, 60%, 40%], **When** they ask "Give me a study plan", **Then** they receive a personalized recommendation identifying Chapter 3 as a weak area requiring review, with specific sections highlighted
2. **Given** a premium student has strong performance across all chapters (>80%), **When** they request a learning path, **Then** they receive an accelerated path recommending advanced topics or chapter completion
3. **Given** a free student asks for a learning path, **When** the request is made, **Then** they receive a 403 error with a clear upgrade message explaining this is a Pro feature

---

### User Story 2 - Premium Student Submits Written Answer for Detailed Feedback (Priority: P2)

As a premium student, I want to write free-form answers to open-ended questions and receive detailed educational feedback, so that I can develop deeper understanding beyond multiple-choice quizzes.

**Why this priority**: This provides the second pillar of Pro value - rich assessment that develops conceptual understanding rather than just testing recall.

**Independent Test**: Can be fully tested by a premium student submitting a paragraph-length answer to a conceptual question and receiving scored feedback with specific correct/missing concepts identified.

**Acceptance Scenarios**:

1. **Given** a premium student submits a correct answer explaining MCP using different vocabulary than the model answer, **When** the answer is graded, **Then** they receive full credit with feedback confirming their understanding despite vocabulary differences
2. **Given** a premium student submits a partially correct answer missing key concepts, **When** graded, **Then** they receive partial credit with specific feedback on what was correct and what concepts are missing
3. **Given** a premium student submits an answer with significant misconceptions, **When** graded, **Then** they receive a low score with educational feedback explaining the misconceptions and pointing to relevant chapter sections
4. **Given** a free student attempts to submit a written assessment, **When** the request is made, **Then** they receive a 403 error with an upgrade message

---

### User Story 3 - Student Views Their Cost Usage Transparency (Priority: P3)

As a student (premium or pro), I want to see how much of my monthly LLM budget I've used, so that I can manage my usage and understand the cost implications.

**Why this priority**: Cost transparency is a constitutional requirement (CC-04) and builds trust with users. However, it's lower priority than the core features themselves.

**Independent Test**: Can be fully tested by a student calling the cost summary endpoint and receiving accurate current month usage data.

**Acceptance Scenarios**:

1. **Given** a premium student has used 3 adaptive learning path requests and 10 assessments this month, **When** they request their cost summary, **Then** they see total cost, remaining budget, and usage breakdown by feature
2. **Given** a student approaches 80% of their monthly budget, **When** they use a hybrid feature, **Then** they receive a warning alert before the feature executes
3. **Given** a student has exhausted their monthly budget, **When** they request a hybrid feature, **Then** they receive a graceful message explaining the limit and when it resets

---

### Edge Cases

- What happens when the LLM API times out (>15 seconds)? System returns graceful fallback message asking student to retry, without charging them
- How does the system handle a student with no prior progress data? System returns a standard learning path based on chapter sequence, not personalized
- What happens if a student submits a 5-word answer (below 20-word minimum)? System rejects before LLM call with clear message about minimum length
- What happens if a student submits a 600-word answer (above 500-word maximum)? System rejects before LLM call with clear message about maximum length
- How does the system handle LLM API being completely unavailable? System returns cached recommendations (if available) or graceful degradation message

## Requirements *(mandatory)*

### Functional Requirements

**Feature A: Adaptive Learning Path**

- **FR-A-001**: System MUST provide endpoint `POST /api/v2/adaptive/learning-path` accessible only to premium/pro tier users
- **FR-A-002**: System MUST collect student's complete progress data including chapter completion percentages, quiz scores per chapter, quiz attempt counts, and streak data
- **FR-A-003**: System MUST fetch chapter metadata for all available chapters before calling LLM
- **FR-A-004**: System MUST call Claude Sonnet (claude-sonnet-4-20250514) with student data and chapter metadata as context
- **FR-A-005**: LLM MUST return structured JSON containing: recommended chapters (top 3), reasoning per recommendation, identified weak areas, identified strengths, overall assessment, suggested daily goal in minutes
- **FR-A-006**: System MUST store the LLM response in `adaptive_recommendations` table with timestamp and user_id
- **FR-A-007**: System MUST provide endpoint `GET /api/v2/adaptive/learning-path/latest` that returns the most recent recommendation without re-calling LLM
- **FR-A-008**: Free users MUST receive HTTP 403 with structured upgrade message when accessing any adaptive learning endpoint
- **FR-A-009**: LLM call MUST be user-initiated only (student explicitly requests learning path, never auto-generated by system)
- **FR-A-010**: Token usage MUST be logged to `llm_usage` table immediately after every LLM call with user_id, feature_name, model, input_tokens, output_tokens, cost_usd
- **FR-A-011**: If LLM call fails (timeout, API error, rate limit), system MUST return last stored recommendation or graceful error message if none exists

**Feature B: LLM-Graded Assessments**

- **FR-B-001**: System MUST provide endpoint `POST /api/v2/assessments/{chapter_id}/submit` accessible only to premium/pro tier users
- **FR-B-002**: Assessment questions MUST be open-ended (short paragraph answers), stored in database separate from MCQ quiz questions
- **FR-B-003**: Request body MUST contain: question_id (string), answer_text (string, 20-500 words)
- **FR-B-004**: System MUST fetch the question text, model answer criteria, and relevant chapter content from R2 as grading context before calling LLM
- **FR-B-005**: System MUST call Claude Sonnet with question, student answer, and chapter content as context
- **FR-B-006**: LLM MUST return structured JSON containing: score (0-100), grade (A/B/C/D/F), correct_concepts (list), missing_concepts (list), feedback (string), improvement_suggestions (string), word_count (integer)
- **FR-B-007**: System MUST store the grading result in `assessment_results` table with timestamp and user_id
- **FR-B-008**: System MUST provide endpoint `GET /api/v2/assessments/{chapter_id}/results` that returns all past assessment results for the requesting student
- **FR-B-009**: Free users MUST receive HTTP 403 with structured upgrade message when accessing any assessment endpoint
- **FR-B-010**: Answer length MUST be validated before LLM call: minimum 20 words, maximum 500 words (reject with clear error message, no wasted tokens)
- **FR-B-011**: Token usage MUST be logged to `llm_usage` table immediately after every LLM call
- **FR-B-012**: If LLM call fails, system MUST return error message asking student to retry (do NOT return partial or provisional grades)
- **FR-B-013**: System MUST provide endpoint `GET /api/v2/assessments/{chapter_id}/questions` that returns open-ended questions for a chapter (without answer keys or model criteria)

**Cross-Cutting Requirements**

- **FR-C-001**: System MUST provide endpoint `GET /api/v2/users/me/cost-summary` that shows current month's hybrid feature usage cost and remaining budget
- **FR-C-002**: All LLM calls MUST use async (non-blocking) HTTP to Anthropic API
- **FR-C-003**: Claude API key MUST be read from environment variable (never hardcoded), default variable name: `ANTHROPIC_API_KEY`
- **FR-C-004**: System MUST enforce monthly cost cap per user: $2.00 for premium tier, $5.00 for pro tier
- **FR-C-005**: When user reaches monthly cost cap, system MUST gracefully deny further hybrid feature access until next month with clear message

### Key Entities *(include if feature involves data)*

- **Student Learning Profile**: Represents a student's accumulated learning data including chapter completion status, quiz scores across attempts, time spent per chapter, streak counts, and performance trends over time
- **Adaptive Recommendation**: A personalized learning suggestion generated by LLM analysis, containing recommended chapters with priority ordering, rationale for each recommendation, identified knowledge gaps, and estimated time commitments
- **Written Assessment**: An open-ended question requiring paragraph-length answers, associated with a specific chapter, with model answer criteria used for LLM grading
- **Assessment Result**: The graded outcome of a written assessment submission, containing numerical score, letter grade, concept-level feedback, and improvement suggestions
- **LLM Usage Log**: A cost tracking record capturing every LLM API call with user attribution, feature identification, token counts, model used, and calculated cost in USD

### Non-Functional Requirements

- **NF-001**: Adaptive learning path endpoint MUST respond within 8 seconds (includes LLM latency budget)
- **NF-002**: LLM assessment grading endpoint MUST respond within 10 seconds (includes LLM latency budget)
- **NF-003**: Both features MUST implement timeout handling: if LLM call exceeds 15 seconds, return graceful fallback response (not HTTP 500)
- **NF-004**: Monthly LLM cost per premium user MUST NOT exceed $2.00 (enforced by hard cap, not just monitoring)
- **NF-005**: All LLM API calls MUST use async HTTP to prevent blocking other requests
- **NF-006**: System MUST achieve 99% uptime for Phase 1 endpoints regardless of Phase 2 feature availability
- **NF-007**: LLM usage logs MUST be written within 1 second of LLM response (eventual consistency acceptable for cost dashboard)

## Success Criteria *(mandatory)*

<!--
  IMPORTANT: Success criteria must be MEASURABLE and TECHNOLOGY-AGNOSTIC.
  Focus on user outcomes and business value, not implementation details.
-->

### Educational Impact

- **SC-E-001**: Premium students who use adaptive learning path recommendations show 30% improvement in quiz scores within 2 weeks compared to students who don't use the feature
- **SC-E-002**: Students submitting written assessments receive feedback within 10 seconds that they rate as "helpful" or "very helpful" in 80% of cases (measured via optional feedback prompt)
- **SC-E-003**: Students using LLM-graded assessments demonstrate 25% better retention on follow-up quizzes compared to MCQ-only students

### User Experience

- **SC-U-001**: 90% of premium students can complete the flow from "requesting learning path" to "understanding what to study next" in under 2 minutes
- **SC-U-002**: 85% of students agree with the statement "The feedback on my written answer helped me understand what I got right and what I missed" (measured via survey)
- **SC-U-003**: Less than 5% of students encounter LLM timeout errors (indicating system is meeting latency requirements)

### Cost Efficiency

- **SC-C-001**: Average monthly LLM cost per premium user stays below $1.50 (targeting 25% buffer under $2.00 cap)
- **SC-C-002**: 95% of LLM calls complete successfully on first attempt (indicating good error handling and API reliability)
- **SC-C-003**: Cost tracking dashboard shows accurate usage data updated within 5 seconds of feature usage

### Adoption & Engagement

- **SC-A-001**: 60% of premium students use adaptive learning path feature at least once per week
- **SC-A-002**: Premium students submit an average of 3+ written assessments per month
- **SC-A-003**: Less than 10% of premium users hit their monthly cost cap (indicating caps are set appropriately)

## Assumptions

<!--
  Document assumptions made while writing this spec. These are reasonable defaults
  based on industry standards and context.
-->

1. **Student Motivation**: Students using premium features are motivated to improve their understanding and will engage thoughtfully with personalized recommendations and detailed feedback

2. **Content Quality**: Chapter content and model answer criteria are well-written and accurate, providing a solid foundation for LLM analysis

3. **LLM Reliability**: Anthropic Claude API maintains >99% uptime and reasonable latency (<10 seconds for typical requests)

4. **User Internet**: Students have stable internet connections capable of handling 8-10 second API response times

5. **Answer Authenticity**: Students write their own answers rather than copying from external sources (honor system, no plagiarism detection in scope)

6. **Feedback Value**: Detailed, educational feedback on written answers provides more learning value than simple right/wrong MCQ feedback

7. **Cost Predictability**: Token usage per request is predictable enough that monthly caps can be set and enforced without frequent user complaints

8. **Privacy Compliance**: Student learning data can be processed by LLM APIs in compliance with applicable privacy regulations (FERPA, GDPR, etc.)

## Out of Scope *(Phase 2 Specific)*

The following are explicitly OUT OF SCOPE for Phase 2:

- **Cross-Chapter Synthesis (Feature C)**: Not selected for Phase 2 implementation
- **AI Mentor Agent (Feature D)**: Not selected for Phase 2 implementation
- **Web Frontend**: Phase 3 deliverable, not part of Phase 2
- **Modifying Phase 1 APIs**: No changes allowed to existing Phase 1 endpoints (chapters, quizzes, progress, access, search, users)
- **Auto-Triggering LLM Features**: System never initiates LLM calls without explicit user request
- **Free User Access**: Free tier users have zero access to hybrid features (no trials, no previews)
- **LLM Model Selection**: Users cannot choose which LLM model grades their work (always Claude Sonnet)
- **Custom Rubrics**: Students cannot provide their own grading rubrics (uses model answer criteria only)
- **Answer Revision**: Students cannot revise and resubmit answers for re-grading (one submission per question)
- **Peer Comparison**: Students cannot see how their answers compare to peers (privacy and academic integrity)

## Dependencies

- **Phase 1 Completion**: All Phase 1 features must be functional before Phase 2 implementation begins
- **Anthropic API Access**: Valid Anthropic API key with sufficient quota for development and production
- **Database Migration**: New tables required: `llm_usage_logs`, `adaptive_recommendations`, `assessment_questions`, `assessment_results`
- **Environment Configuration**: Secure storage for `ANTHROPIC_API_KEY` in production environment
- **Cost Monitoring**: Infrastructure for aggregating and querying LLM usage data (can use existing PostgreSQL)

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| LLM API costs exceed projections | High | Medium | Enforce hard caps per user, monitor daily, optimize prompts for token efficiency |
| LLM latency causes poor UX | Medium | Medium | Implement timeout handling, async calls, graceful fallbacks, cache recommendations |
| Students game the system (AI-written answers) | Medium | Low | Design assessments for conceptual understanding, not fact recall; honor system |
| LLM hallucinates incorrect feedback | High | Low | Ground all prompts in course content, include hallucination guards in system prompt, structured output validation |
| Premium gate bypassed | Critical | Low | Tier check before LLM call, service-layer enforcement, integration tests for 403 responses |
| Phase 1 code contaminated with LLM calls | Critical | Medium | Strict code review, automated grep scans, git diff verification on Phase 1 files |

## Glossary

- **Hybrid Intelligence**: Backend architecture that selectively uses LLM API calls for specific premium features while maintaining deterministic Phase 1 core
- **Adaptive Learning Path**: Personalized study recommendations generated by LLM analysis of student performance data
- **LLM-Graded Assessment**: Open-ended written answers evaluated by LLM with detailed educational feedback
- **Premium Tier**: Subscription level ($9.99/mo) with full content access but NO hybrid features
- **Pro Tier**: Subscription level ($19.99/mo) with full content access PLUS hybrid features (adaptive path + LLM assessments)
- **Cost Cap**: Maximum monthly LLM cost per user ($2 for premium, $5 for pro) before features are disabled
- **User-Initiated**: Feature triggered only by explicit student request, never auto-triggered by system

---

## Appendix A: LLM Prompt Contracts

### Adaptive Learning Path - System Prompt

```
You are an educational analytics expert analyzing a student's learning data for an AI Agent Development course. Base ALL recommendations strictly on the provided student data and chapter information. Do not recommend chapters or topics not present in the provided chapter list. Return ONLY valid JSON matching the specified schema. No preamble, no explanation outside JSON.
```

### Adaptive Learning Path - User Prompt Template

```
Student Learning Data: {student_progress_json}
Available Chapters: {chapters_metadata_json}

Generate a personalized learning path recommendation. Return JSON with this exact schema:
{
  "recommended_chapters": [
    {
      "chapter_id": "ch-XXX",
      "title": "...",
      "priority": 1,
      "reason": "...",
      "estimated_time_minutes": 30
    }
  ],
  "weak_areas": ["...", "..."],
  "strengths": ["...", "..."],
  "overall_assessment": "...",
  "suggested_daily_goal_minutes": 45
}
```

### LLM Assessment - System Prompt

```
You are an expert educator grading a student's written answer for an AI Agent Development course. Grade based ONLY on the provided course content and the model answer criteria. Do not give credit for concepts not covered in the provided chapter content. Return ONLY valid JSON matching the specified schema. No preamble, no markdown, no explanation outside JSON. Hallucination guard: If the student mentions concepts not in the course content, do not mark them as correct.
```

### LLM Assessment - User Prompt Template

```
Chapter Content (use as grading reference): {chapter_content_markdown}
Question: {question_text}
Model Answer Criteria: {model_answer_criteria}
Student's Answer: {student_answer_text}

Grade this answer and return JSON with this exact schema:
{
  "score": 85,
  "grade": "B",
  "correct_concepts": ["concept1", "concept2"],
  "missing_concepts": ["concept3"],
  "feedback": "Your answer demonstrates a solid understanding of...",
  "improvement_suggestions": "To improve, consider adding...",
  "word_count": 120
}
```

---

**Specification Status**: ✅ Ready for Planning

**Next Phase**: `/sp.plan` - Create Technical Implementation Plan

**Constitution Compliance**: This specification adheres to Constitution v2.0.0, specifically:
- Principle VIII: Hybrid Selectivity Law (premium-only, user-initiated, max 2 features)
- Principle IX: Architectural Separation Law (Phase 1 APIs unchanged)
- Principle X: Cost Control Standards (caps, logging, transparency)
- Principle XI: LLM Quality Standards (grounding, structured output, fallbacks)
- Principle XII: Premium Gate Enforcement (tier checks, clear messages)
