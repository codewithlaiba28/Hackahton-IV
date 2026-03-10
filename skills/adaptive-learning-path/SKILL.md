---
name: adaptive-learning-path
description: |
  [What] Generates personalized learning recommendations by analyzing student patterns, performance, and learning history.
  [When] Use when premium students request personalized guidance, adaptive recommendations, or optimized learning paths.
allowed-tools: Read, Grep, Glob, Write
---

# Adaptive Learning Path Skill

## Purpose

This skill (Phase 2 Hybrid - Premium Only) analyzes student learning patterns, quiz performance, and engagement data to generate personalized learning path recommendations that optimize understanding and retention.

## ⚠️ Premium Feature Gate

```
ACCESS REQUIREMENT: Pro Tier Only

This skill uses backend LLM calls and must be:
✓ Premium-gated (Pro tier only)
✓ User-initiated (explicit request)
✓ Cost-tracked (monitor per-user cost)
✓ Isolated (separate API route)

Before activation, verify:
- Student has Pro access
- User explicitly requested feature
- Cost tracking is enabled
- Hybrid feature is explained
```

## Trigger Keywords

- "personalized path"
- "adaptive learning"
- "recommend me what to study"
- "optimize my learning"
- "what should I focus on"
- "create learning plan"
- "adaptive recommendations"
- "personalized study plan"

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Student performance data, learning analytics, path optimization algorithms |
| **Conversation** | Student's goals, constraints, preferences, time availability |
| **Skill References** | Adaptive learning patterns from `references/` (personalization algorithms, learning science) |
| **User Guidelines** | Cost limits, recommendation frequency, path adjustment policies |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

## Core Principle: Selective Hybrid Intelligence

```
HYBRID FEATURE RULES:

✅ DO:
- Verify Pro access before activation
- Explain this uses premium LLM analysis
- Track costs per recommendation
- Provide clear value over free features
- Allow opt-out at any time

❌ DON'T:
- Auto-trigger without request
- Hide that this is premium feature
- Use for core course navigation
- Exceed cost limits
- Make recommendations without data
```

## Workflow

### Step 1: Verify Access & Explain Feature

```
1. Check Pro access:
   IF student.tier != "Pro":
       RETURN "This is a Pro feature. Upgrade to access."

2. Explain feature:
   "This feature uses AI to analyze your learning patterns
   and create a personalized study plan.

   This is a premium Pro feature.

   Continue with personalized analysis?"

3. Get explicit consent:
   - Confirm user wants this
   - Acknowledge premium nature
   - Proceed only with consent
```

### Step 2: Gather Learning Data

```
Collect comprehensive student data:

1. Performance Data:
   - Quiz scores (all attempts)
   - Time per question
   - First-try vs. retry success
   - Improvement trends
   - Knowledge gaps identified

2. Engagement Data:
   - Time spent per chapter
   - Completion rates
   - Streak patterns
   - Drop-off points
   - Review frequency

3. Learning Preferences:
   - Preferred content types (if tracked)
   - Pace (fast/slow learner)
   - Best performance time (if available)
   - Stated goals

4. Course Structure:
   - Remaining chapters
   - Prerequisite chains
   - Difficulty levels
   - Estimated times
```

### Step 3: Analyze Patterns (LLM-Powered)

```
LLM Analysis Tasks:

1. Identify Strengths:
   - Topics with high scores
   - Fast comprehension areas
   - Consistent performance

2. Identify Weaknesses:
   - Topics with low scores
   - Multiple retry attempts
   - Slow completion times
   - Knowledge gaps

3. Detect Patterns:
   - Performance by topic type
   - Time-of-day effects (if available)
   - Learning velocity changes
   - Engagement correlation

4. Predict Challenges:
   - Upcoming difficult topics
   - Potential struggle points
   - Optimal review timing
```

### Step 4: Generate Personalized Path

```
Create adaptive learning plan:

1. Immediate Next Steps (1-3 days):
   - Address critical gaps
   - Build on recent success
   - Optimal difficulty level

2. Short-Term Plan (1 week):
   - Chapter sequence
   - Review sessions
   - Quiz checkpoints

3. Medium-Term Plan (2-4 weeks):
   - Milestone goals
   - Challenge areas to tackle
   - Completion targets

4. Long-Term Trajectory:
   - Course completion date
   - Mastery timeline
   - Certification path
```

### Step 5: Present Recommendations

```
Structure the personalized plan:

1. Executive Summary:
   - Overall assessment
   - Key strengths
   - Primary focus areas

2. Personalized Path:
   - Day-by-day or week-by-week plan
   - Specific chapters/sections
   - Review sessions included

3. Rationale:
   - Why this sequence
   - What the data shows
   - Expected outcomes

4. Flexibility:
   - Can adjust based on progress
   - Optional acceleration
   - Modification options
```

### Step 6: Track & Adjust

```
Ongoing optimization:

1. Monitor Progress:
   - Track plan adherence
   - Measure effectiveness
   - Note deviations

2. Gather Feedback:
   - Was recommendation helpful?
   - Difficulty level appropriate?
   - Pace comfortable?

3. Adjust Path:
   - If struggling → slow down, add review
   - If excelling → accelerate, add challenges
   - If stuck → alternative approach

4. Regenerate as Needed:
   - Weekly check-ins
   - After major assessments
   - On student request
```

## Response Templates

### Access Verification

```
🌟 **Personalized Learning Path (Pro Feature)**

This feature uses AI to analyze your learning patterns and create
a customized study plan optimized for YOUR needs.

**What it analyzes:**
- Your quiz performance
- Learning pace and patterns
- Knowledge gaps
- Optimal review timing

**Cost:** Included in Pro tier

Would you like me to generate your personalized learning path?
```

### Personalized Path Summary

```
📊 **Your Personalized Learning Path**

**Generated:** [Date]
**Based on:** [X] chapters completed, [Y] quizzes taken

---

**YOUR STRENGTHS:**
✓ [Strength 1] - [Evidence]
✓ [Strength 2] - [Evidence]
✓ [Strength 3] - [Evidence]

**FOCUS AREAS:**
⚠️ [Area 1] - [Why it needs attention]
⚠️ [Area 2] - [Why it needs attention]

---

**RECOMMENDED PATH:**

**This Week:**
- Day 1: [Chapter X, Section Y] (~20 min)
- Day 2: [Review Topic A] + Quiz (~15 min)
- Day 3: [Chapter X+1] (~25 min)
- Day 4: Rest or catch-up
- Day 5: [Practice Quiz] (~20 min)
- Weekend: [Optional deep dive]

**Next Week:**
- Focus: [Specific topic]
- Goal: [Milestone]
- Assessment: [Quiz/Checkpoint]

---

**WHY THIS PATH:**
[Explanation of recommendation rationale]

**EXPECTED OUTCOME:**
- Course completion by: [Date]
- Confidence level: [High/Medium/Improving]

Would you like to:
- Start with today's recommendation
- Adjust the plan
- See more details
```

### Struggle Detection & Support

```
⚠️ **I Notice You're Finding This Challenging**

Based on your recent performance:

**Pattern Detected:**
- [Topic] quiz attempts: [X]
- Average score: [Y]%
- Time spent: Higher than average

**This is normal!** These concepts are challenging for many students.

**My Recommendation:**

1. **Review Foundation:**
   - Revisit Chapter [A]: [Key concept]
   - Review your notes from [section]

2. **Targeted Practice:**
   - Try these specific exercises
   - Focus on [sub-topic]

3. **Alternative Approach:**
   - Watch video explanation (if available)
   - Try the worked examples
   - Use the Socratic tutor for guided help

4. **Take a Break:**
   - Sometimes stepping away helps
   - Come back fresh tomorrow

Would you like me to:
- Load the review material
- Connect you with guided practice
- Adjust your learning path
```

### Acceleration Path (Fast Learner)

```
🚀 **You're Excelling! Let's Accelerate**

**Your Performance:**
- Average quiz score: [X]% (Excellent!)
- Completion pace: Ahead of schedule
- Understanding: Strong

**Accelerated Path Recommended:**

**Option 1: Standard Acceleration**
- Skip optional review sections
- Move to next chapter immediately
- Take challenge quizzes

**Option 2: Deep Dive**
- Stay at current pace
- Explore advanced topics
- Work on mastery projects

**Option 3: Help Others**
- Join study groups (if available)
- Answer peer questions
- Contribute to discussions

Which path appeals to you?
```

### Weekly Check-In

```
📅 **Weekly Learning Check-In**

**This Week's Progress:**
✓ Completed: [X chapters/sections]
✓ Quizzes passed: [Y]
✓ Time invested: [Z hours]
✓ Streak: [N] days

**Path Adherence:**
- On track: [Yes/Partially/No]
- Adjustments made: [Any]
- Goals met: [Which ones]

**Next Week's Optimized Plan:**
[Updated recommendations based on progress]

**Questions:**
1. How are you feeling about your progress?
2. Any topics you're struggling with?
3. Any time constraints I should know about?

Based on your answers, I can further refine your path.
```

## Key Principles

### 1. Data-Driven Personalization

```
Base recommendations on:
✓ Actual performance data
✓ Observed learning patterns
✓ Measured engagement
✓ Stated goals and constraints

Not on:
✗ Assumptions about learner type
✗ One-size-fits-all approach
✗ Arbitrary timelines
```

### 2. Actionable Recommendations

```
Every recommendation should be:
- Specific (what exactly to do)
- Timed (how long it takes)
- Sequenced (what order)
- Achievable (realistic given constraints)
- Measurable (how to know it worked)
```

### 3. Flexibility & Adaptation

```
Paths should:
- Adjust to changing circumstances
- Allow student agency
- Accommodate life events
- Support different goals
- Enable acceleration/deceleration
```

### 4. Transparency

```
Always explain:
- Why this recommendation
- What data it's based on
- What alternatives exist
- How to modify the plan
- Expected outcomes
```

### 5. Cost Awareness

```
Monitor and optimize:
- LLM API calls per recommendation
- Token usage for analysis
- Cost per student per month
- Value delivered vs. cost

Keep costs sustainable for Pro tier pricing
```

## Error Handling

| Error | Response |
|-------|----------|
| Insufficient data for analysis | "I need more data to personalize. Complete 2-3 more chapters, then I can create a tailored path. Meanwhile, here's the standard path..." |
| LLM API fails | "Having trouble generating personalized analysis. Your data is saved. Try again in a few moments." |
| Student rejects recommendation | "No problem! Learning is personal. What would work better for you? Let me adjust." |
| Cost limit exceeded | "You've reached the monthly limit for AI-generated recommendations. Standard recommendations are still available. Limit resets on [date]." |
| Performance data inconsistent | "I'm seeing some mixed signals in your data. Let me ask you a few questions to better understand your needs..." |

## Phase 2 Specific Behavior

### Hybrid Intelligence Usage

```
Backend LLM calls for:
- Pattern recognition in learning data
- Natural language explanation generation
- Cross-chapter synthesis
- Personalized feedback composition

ChatGPT for:
- Presenting recommendations warmly
- Answering follow-up questions
- Gathering student preferences
- Encouraging and motivating
```

### Cost Tracking

```
Track per request:
- LLM tokens used
- API call cost
- Total monthly cost per student

Alert thresholds:
- Warning at 80% of monthly budget
- Hard limit at 100%
- Offer to upgrade for more

Monthly budget example:
- Pro tier includes: $5 of LLM credits
- Additional: $0.10 per extra analysis
```

### Premium Gating

```
Access Control:
- Verify Pro tier before analysis
- Show upgrade option if not Pro
- Explain value proposition
- Allow one free sample (optional)

Upgrade Path:
Free → Premium → Pro (with adaptive learning)
```

## Quality Checklist

Before generating adaptive path, verify:

- [ ] Pro access confirmed
- [ ] User explicitly requested feature
- [ ] Sufficient data collected
- [ ] Cost tracking enabled
- [ ] Strengths accurately identified
- [ ] Weaknesses correctly diagnosed
- [ ] Recommendations are actionable
- [ ] Timeline is realistic
- [ ] Alternatives offered
- [ ] Explanation is clear
- [ ] Student can modify plan

## Integration with Other Skills

| Skill | When to Hand Off |
|-------|------------------|
| **content-delivery** | Student ready to start: "Let me load Chapter X" |
| **quiz-master** | Assessment point: "Time to test your understanding" |
| **progress-motivator** | Encouragement needed: "Look at your progress!" |
| **socratic-tutor** | Struggle detected: "Let's work through this together" |

---

## References

See `references/` for:
- Learning analytics patterns
- Personalization algorithms
- Adaptive learning research
- Cost optimization strategies
- Recommendation quality rubric
