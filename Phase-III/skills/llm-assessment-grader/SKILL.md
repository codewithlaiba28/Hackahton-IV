---
name: llm-assessment-grader
description: |
  [What] Evaluates free-form written answers using LLM analysis, providing detailed feedback beyond rule-based grading.
  [When] Use when Pro tier students submit written assessments, essays, or complex answers requiring nuanced evaluation.
allowed-tools: Read, Grep, Glob, Write
---

# LLM Assessment Grader Skill

## Purpose

This skill (Phase 2 Hybrid - Pro Only) uses LLM analysis to evaluate free-form written answers that cannot be graded with simple rule-based matching, providing detailed, educational feedback.

## ⚠️ Premium Feature Gate

```
ACCESS REQUIREMENT: Pro Tier Only

This skill uses backend LLM calls and must be:
✓ Premium-gated (Pro tier only)
✓ User-initiated (explicit request for assessment)
✓ Cost-tracked (monitor per-answer cost)
✓ Isolated (separate assessment API route)
✓ Educationally-justified (explain why rule-based won't work)

Before activation, verify:
- Student has Pro access
- Question type requires LLM grading
- User understands this is premium feature
- Cost tracking is enabled
```

## Trigger Keywords

- "grade my answer" (for written responses)
- "evaluate my response"
- "assess my understanding"
- "written assessment"
- "essay feedback"
- "detailed feedback"
- "explain my mistakes"

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Assessment rubrics, grading criteria, feedback templates |
| **Conversation** | Student's submitted answer, question context, self-assessment |
| **Skill References** | Assessment patterns from `references/` (rubrics, feedback strategies, grading criteria) |
| **User Guidelines** | Grading standards, feedback tone, score thresholds, retry policies |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

## Core Principle: Why LLM Grading is Needed

```
WHEN RULE-BASED GRADING FAILS:

Rule-based works for:
✓ Multiple choice (exact match)
✓ True/False (binary)
✓ Fill-in-blank (exact terms)
✓ Simple calculations

LLM grading needed for:
✓ Free-form explanations
✓ Reasoning demonstrations
✓ Problem-solving approaches
✓ Critical thinking responses
✓ Synthesis questions
✓ Real-world application essays

WHY: These require understanding meaning, not just matching text.
```

## Workflow

### Step 1: Verify Access & Question Type

```
1. Check Pro access:
   IF student.tier != "Pro":
       RETURN "LLM-graded assessments are a Pro feature."

2. Verify question type requires LLM:
   IF question.type in ["multiple_choice", "true_false", "fill_blank"]:
       RETURN "This can be graded with rule-based. Use quiz-master skill."
   
   IF question.type in ["essay", "explanation", "analysis", "synthesis"]:
       PROCEED to LLM grading

3. Explain premium feature:
   "This assessment uses AI-powered grading to evaluate
   your understanding and provide detailed feedback.
   
   This is included in your Pro tier.
   
   Ready to submit your answer for grading?"
```

### Step 2: Collect Submission

```
Gather for grading:

1. Question Details:
   - Full question text
   - Learning objective being tested
   - Points possible
   - Grading rubric/criteria

2. Student Answer:
   - Complete written response
   - Any diagrams/code (if applicable)
   - Time spent (if tracked)
   - Draft history (if available)

3. Context:
   - Chapter/topic covered
   - Prerequisite knowledge
   - Expected complexity level
   - Sample answer (if available)
```

### Step 3: LLM Evaluation

```
LLM Grading Tasks:

1. Comprehension Check:
   - Does student understand the question?
   - Did they address what was asked?
   - Is the response relevant?

2. Knowledge Accuracy:
   - Are facts correct?
   - Are concepts properly applied?
   - Are there misconceptions?

3. Reasoning Quality:
   - Is logic sound?
   - Are connections made clear?
   - Is the argument coherent?

4. Completeness:
   - Did they cover all parts?
   - Is depth appropriate?
   - Are key points included?

5. Critical Thinking:
   - Did they go beyond recall?
   - Is there original analysis?
   - Are connections made to broader concepts?
```

### Step 4: Generate Score & Feedback

```
Scoring Rubric (Example):

| Criteria | Excellent (5) | Good (3-4) | Needs Work (1-2) |
|----------|---------------|------------|------------------|
| Accuracy | All facts correct | Minor errors | Significant errors |
| Completeness | All parts addressed | Mostly complete | Missing key parts |
| Reasoning | Clear, logical | Some gaps | Unclear/flawed |
| Depth | Insightful | Adequate | Superficial |
| Communication | Clear, organized | Understandable | Confusing |

Feedback Structure:

1. Overall Assessment:
   - Score: [X]/[Y] or [Z]%
   - One-sentence summary

2. Strengths:
   - What student did well
   - Specific examples from answer

3. Areas for Improvement:
   - What was missing/incorrect
   - Specific misconceptions
   - What to focus on

4. Model Answer/Key Points:
   - What a complete answer includes
   - Alternative valid approaches
   - Reference to course content

5. Next Steps:
   - Specific study recommendations
   - Practice suggestions
   - When to retry
```

### Step 5: Deliver Feedback

```
Present feedback educationally:

1. Start Positive:
   - Acknowledge effort
   - Highlight what was correct
   - Validate partial understanding

2. Constructive Criticism:
   - Be specific about errors
   - Explain WHY it's incorrect
   - Point to correct understanding

3. Educational Value:
   - Turn mistakes into learning
   - Connect to course content
   - Suggest resources

4. Encourage Growth:
   - Emphasize this is formative
   - Offer retry opportunity
   - Express confidence in improvement
```

### Step 6: Offer Follow-Up

```
After grading, offer:

1. Review Options:
   - "Review the relevant chapter section"
   - "See model answer with explanation"
   - "Try a similar practice question"

2. Additional Help:
   - "Connect with Socratic tutor for guided help"
   - "Get concept explanation"
   - "Schedule review session"

3. Retry Policy:
   - "You can retry after reviewing"
   - "Best score will be recorded"
   - "Here's what to focus on before retrying"
```

## Response Templates

### Submission Acknowledgment

```
📝 **Assessment Submitted**

**Question:** [Brief description]
**Type:** Written response
**Points Possible:** [X]

Your answer has been submitted for AI-powered grading.

**What happens next:**
- AI will analyze your understanding
- Check for accuracy and completeness
- Provide detailed feedback
- Suggest next steps

**Grading time:** ~30 seconds

Please wait while your answer is evaluated...
```

### Grading Results (Strong Performance)

```
✅ **Assessment Results**

**Score:** [X]/[Y] ([Z]%)
**Level:** Excellent

---

**WHAT YOU DID WELL:**

✓ **[Strength 1]:**
  [Specific example from answer]

✓ **[Strength 2]:**
  [Specific example from answer]

✓ **[Strength 3]:**
  [Specific example from answer]

---

**MINOR IMPROVEMENTS:**

⚠️ [Small area that could be enhanced]
   [Specific suggestion]

---

**KEY TAKEAWAYS:**
Your answer demonstrates strong understanding of [concepts].
You effectively [specific skill demonstrated].

---

**NEXT STEPS:**
- ✓ Ready to move to next topic
- Optional: Deepen understanding with [advanced topic]
- Consider helping peers (if community feature)

Congratulations on excellent work!
```

### Grading Results (Moderate Performance)

```
📊 **Assessment Results**

**Score:** [X]/[Y] ([Z]%)
**Level:** Good - Room for Improvement

---

**STRENGTHS:**

✓ **[What was correct]:**
  [Specific example from answer]

✓ **[Good understanding of]:**
  [Specific concept they grasped]

---

**AREAS FOR IMPROVEMENT:**

⚠️ **[Misconception 1]:**
  You wrote: "[quote from student]"
  
  **Issue:** [Explain the misconception]
  
  **Correct understanding:** [Explain clearly]
  
  **Reference:** Chapter [N], Section [M]

⚠️ **[Missing concept]:**
  Your answer didn't address [important point]
  
  **Why it matters:** [Explain importance]
  
  **Reference:** Chapter [N], Section [M]

---

**MODEL ANSWER KEY POINTS:**

A complete answer should include:
1. [Key point 1]
2. [Key point 2]
3. [Key point 3]

---

**RECOMMENDED NEXT STEPS:**

1. **Review:** Chapter [X], Section [Y]
2. **Practice:** Try similar question
3. **Retry:** You can retake this assessment after review

Would you like to:
- Review the relevant chapter?
- See a detailed model answer?
- Try a practice question first?
```

### Grading Results (Needs Improvement)

```
📚 **Assessment Results**

**Score:** [X]/[Y] ([Z]%)
**Level:** Needs More Study

---

**I can see you're working to understand this. Let's break down where things went:**

**WHAT YOU GOT RIGHT:**

✓ [Acknowledge any correct elements, even if small]

---

**KEY GAPS TO ADDRESS:**

❌ **[Major misconception 1]:**
  You wrote: "[quote]"
  
  **This is incorrect because:** [Clear explanation]
  
  **The correct concept is:** [Teach it clearly]
  
  **Example:** [Concrete example]
  
  **Study:** Chapter [N], Section [M]

❌ **[Major misconception 2]:**
  [Same structure as above]

---

**FOUNDATIONAL CONCEPTS TO REVIEW:**

Before retrying, make sure you understand:
- [Concept 1] from Chapter [X]
- [Concept 2] from Chapter [Y]
- [Concept 3] from Chapter [Z]

---

**STUDY PLAN:**

1. **First:** Re-read Chapter [X] carefully
2. **Then:** Review your notes from [section]
3. **Next:** Try the practice quiz (easier questions)
4. **Finally:** Retry this assessment

---

**REMEMBER:**
This assessment is to help YOU learn, not to judge you.
Every expert was once a beginner.
The fact that you're trying shows you're on the path to learning.

**I recommend:**
- Don't be discouraged
- Take time to review thoroughly
- Use the Socratic tutor for guided help
- Retry when you feel more confident

Would you like me to:
- Load the review material?
- Connect you with guided practice?
- Explain any specific concept?
```

### Partial Credit Explanation

```
📝 **Detailed Feedback on Your Answer**

**Your Answer:**
"[Student's full response]"

---

**GRADING BREAKDOWN:**

| Criteria | Points | Notes |
|----------|--------|-------|
| Accuracy | X/5 | [Specific feedback] |
| Completeness | X/5 | [Specific feedback] |
| Reasoning | X/5 | [Specific feedback] |
| **Total** | **X/15** | |

---

**LINE-BY-LINE ANALYSIS:**

**Paragraph 1:**
"[Quote]"
✓ Good: [What was correct]
⚠️ Issue: [What needs correction]

**Paragraph 2:**
"[Quote]"
✓ Good: [What was correct]
⚠️ Missing: [What should be added]

---

**HOW TO IMPROVE:**

To earn full marks:
1. [Specific action 1]
2. [Specific action 2]
3. [Specific action 3]
```

## Key Principles

### 1. Educational Feedback First

```
Feedback should:
✓ Teach, not just evaluate
✓ Explain WHY, not just WHAT
✓ Point to resources
✓ Encourage improvement
✓ Be specific and actionable

Not:
✗ Just give a score
✗ Vague comments ("good job")
✗ Only point out errors
✗ Discourage the learner
```

### 2. Partial Credit Recognition

```
Always acknowledge:
- Correct elements in partially correct answers
- Good reasoning even with wrong conclusion
- Effort and attempt
- Progress from previous submissions

This encourages:
- Risk-taking in learning
- Learning from mistakes
- Persistence through difficulty
```

### 3. Growth Mindset Language

```
Use language like:
- "You're developing understanding of..."
- "This is challenging - keep working on it"
- "Your effort shows in..."
- "With more practice, you'll master..."
- "Not yet, but you're getting there"

Avoid:
- "You don't understand this"
- "This is wrong"
- Fixed ability labels
```

### 4. Actionable Next Steps

```
Every assessment should end with:
- Clear what to study next
- Specific resources to use
- When to retry
- How to prepare for retry
- Support available
```

## Error Handling

| Error | Response |
|-------|----------|
| LLM API fails during grading | "Having trouble grading right now. Your answer is saved. Try again in a moment." |
| Student submits blank/minimal answer | "I need more to evaluate. Please write a more complete response explaining your thinking." |
| Answer is off-topic | "Your answer doesn't address the question. Let me show you what's being asked..." |
| Suspected plagiarism | "This answer seems familiar. Can you explain your thinking in your own words?" |
| Cost limit exceeded | "You've reached monthly LLM grading limit. Standard quizzes still available. Limit resets [date]." |

## Phase 2 Specific Behavior

### Hybrid Intelligence Usage

```
Backend LLM calls for:
- Understanding answer semantics
- Evaluating reasoning quality
- Identifying misconceptions
- Generating personalized feedback
- Comparing to model answers

ChatGPT for:
- Presenting feedback encouragingly
- Answering follow-up questions
- Connecting to study resources
- Motivating continued effort
```

### Cost Management

```
Cost per assessment:
- Short answer (~500 tokens): $0.005
- Medium answer (~1500 tokens): $0.015
- Long essay (~3000 tokens): $0.030

Monthly budget:
- Pro tier includes: 50 assessments
- Overage: Standard rates apply
- Alert at 80% usage
```

### Quality Assurance

```
Ensure grading quality:
- Consistent rubric application
- Fair partial credit
- Accurate misconception identification
- Constructive tone
- Actionable feedback
```

## Quality Checklist

Before delivering grade, verify:

- [ ] Score accurately reflects rubric
- [ ] Strengths specifically identified
- [ ] Weaknesses clearly explained
- [ ] Misconceptions correctly diagnosed
- [ ] References to course content provided
- [ ] Next steps are actionable
- [ ] Tone is encouraging and educational
- [ ] Partial credit fairly awarded
- [ ] Model answer key points included
- [ ] Retry options explained

## Integration with Other Skills

| Skill | When to Hand Off |
|-------|------------------|
| **concept-explainer** | Student needs concept review: "Let me explain this concept" |
| **socratic-tutor** | Student wants guided help: "Help me work through this" |
| **quiz-master** | Student ready for practice: "Try some practice questions" |
| **progress-motivator** | Student discouraged: "Let me show you your overall progress" |

---

## References

See `references/` for:
- Grading rubric templates
- Feedback phrase library
- Misconception database
- Model answer examples
- Cost optimization strategies
