# Quiz Design Patterns

## Question Quality Rubric

| Criterion | Excellent (5) | Good (3) | Needs Work (1) |
|-----------|---------------|----------|----------------|
| **Clarity** | Unambiguous, clear wording | Minor ambiguity | Confusing |
| **Relevance** | Directly tests learning objective | Somewhat relevant | Off-topic |
| **Difficulty** | Appropriate for level | Slightly off | Too easy/hard |
| **Distractors** | Plausible, educational | Some weak | Obvious |
| **Explanation** | Thorough, references content | Basic | Missing |

---

## Bloom's Taxonomy Question Types

### Remembering (Recall)

```
Question Type: Multiple Choice, True/False, Fill-in-blank
Verbs: define, list, state, identify, name

Example: "What does API stand for?"
A) Application Programming Interface ✓
B) Applied Protocol Integration
C) Automated Process Interface
D) Application Process Integration
```

### Understanding (Comprehension)

```
Question Type: Multiple Choice, Short Answer
Verbs: explain, describe, summarize, interpret

Example: "Which statement BEST describes REST architecture?"
```

### Applying (Application)

```
Question Type: Scenario-based, Problem-solving
Verbs: use, demonstrate, solve, implement

Example: "Given this scenario, which HTTP method should you use?"
```

### Analyzing (Analysis)

```
Question Type: Compare/contrast, Debug, Multiple select
Verbs: analyze, compare, distinguish, examine

Example: "Select ALL differences between SOAP and REST:"
```

### Evaluating (Evaluation)

```
Question Type: Justification, Best choice
Verbs: evaluate, justify, recommend, defend

Example: "Which API design is MOST appropriate for this use case? Justify your answer."
```

### Creating (Synthesis)

```
Question Type: Design, Build (Phase 2 LLM-graded)
Verbs: design, create, develop, construct

Example: "Design an API endpoint for user registration. Include method, URL, request body, and response."
```

---

## Distractor Construction

### Good Distractors

```
Characteristics:
- Plausible to students with gaps in understanding
- Based on common misconceptions
- Similar length/structure to correct answer
- Grammatically consistent with question stem

Example:
Q: "What is the time complexity of binary search?"
A) O(n)           ← Plausible (linear search confusion)
B) O(log n) ✓     ← Correct
C) O(n log n)     ← Plausible (sorting confusion)
D) O(1)           ← Plausible (hash table confusion)
```

### Bad Distractors

```
Problems to avoid:
- Obviously wrong
- Too similar to correct answer
- Longer/shorter than other options
- Grammatical inconsistencies

Example (BAD):
Q: "What is an API?"
A) Application Programming Interface ✓
B) A type of fruit        ← Obviously wrong
C) A programming language ← Obviously wrong
D) Application Programming← Incomplete
```

---

## Feedback Phrase Library

### Correct Answer Praise

```
Enthusiastic:
- "Excellent!"
- "Perfect!"
- "You got it!"
- "That's exactly right!"
- "Well done!"

Acknowledgment:
- "Correct!"
- "Yes, that's right."
- "Good work!"
- "You understand this well."

Progress-oriented:
- "You're mastering this!"
- "Great progress!"
- "This shows real understanding."
- "You've clearly studied this."
```

### Incorrect Answer Support

```
Normalize:
- "This is a common mistake."
- "Many students find this tricky."
- "Don't worry - this is how we learn."
- "Mistakes help our brains grow."

Encourage:
- "Let's figure this out together."
- "You'll get this next time."
- "The important thing is you're practicing."
- "Keep going - you're improving!"

Redirect:
- "Let's review the key concept."
- "Think about [related principle]."
- "Remember when we learned..."
```

### Explanation Starters

```
Why correct:
- "This is correct because..."
- "The key here is..."
- "Recall that..."

Why incorrect:
- "This isn't quite right because..."
- "The issue with this answer is..."
- "What's missing here is..."

Reference content:
- "As we covered in Chapter X..."
- "Remember the rule that..."
- "This relates to [concept] because..."
```

---

## Difficulty Calibration

### Easy Questions

```
Characteristics:
- Direct recall from content
- Single concept tested
- Minimal distractors needed
- 80%+ students should get correct

Use for:
- Warm-up quizzes
- Confidence building
- Basic comprehension checks
```

### Medium Questions

```
Characteristics:
- Requires understanding, not just recall
- May combine 2 concepts
- Plausible distractors
- 60-80% success rate expected

Use for:
- Standard chapter quizzes
- Progress assessment
- Practice exams
```

### Hard Questions

```
Characteristics:
- Multi-step reasoning
- Synthesis of multiple concepts
- Subtle distinctions
- 40-60% success rate expected

Use for:
- Challenge quizzes
- Advanced learners
- Final assessments
```

---

## Quiz Structures

### Quick Check (3-5 questions)

```
Purpose: Rapid comprehension check
Time: 2-3 minutes
Use: After reading a section
Scoring: Informal, no pressure

Structure:
- 2 recall questions
- 2 understanding questions
- 1 application question
```

### Standard Quiz (10 questions)

```
Purpose: Chapter mastery assessment
Time: 10-15 minutes
Use: End of chapter
Scoring: Pass/fail or percentage

Structure:
- 3 recall questions
- 4 understanding questions
- 2 application questions
- 1 analysis question
```

### Comprehensive Exam (20-30 questions)

```
Purpose: Cumulative assessment
Time: 30-45 minutes
Use: Midterm, final, certification
Scoring: Graded, certificate eligibility

Structure:
- Mix of all Bloom's levels
- Weighted by importance
- Time tracking recommended
```

### Practice Quiz (Unlimited)

```
Purpose: Learning through repetition
Time: Self-paced
Use: Anytime practice
Scoring: Low-stakes, retry allowed

Structure:
- Randomized question order
- Randomized answer options
- Immediate detailed feedback
- Retry with different questions
```

---

## Special Question Formats

### Scenario-Based Questions

```
Structure:
1. Present realistic scenario
2. Ask application question
3. Provide context-specific options

Example:
"You're building a weather app that needs to fetch current temperature data every 5 minutes. The data is the same for all users. Which HTTP method and caching strategy should you use?"

A) POST with no caching
B) GET with appropriate cache headers ✓
C) PUT with client-side caching
D) DELETE with no caching
```

### "Select All That Apply"

```
Structure:
- Clear instruction: "Select ALL that apply"
- 2-5 correct answers
- Partial credit possible

Example:
"Which of the following are principles of REST architecture? (Select all that apply)"

□ Client-server architecture ✓
□ State interactions ✓
□ Cacheable responses ✓
□ Required JSON format ✗
□ Layered system ✓
□ Uniform interface ✓
```

### Matching Questions

```
Structure:
- Two columns to match
- Clear pairing instructions
- More options than targets (optional)

Example:
"Match each HTTP status code to its meaning:"

200 → OK
404 → Not Found
500 → Internal Server Error
403 → Forbidden
```

### Assertion-Reason Questions

```
Structure:
- Statement A (Assertion)
- Statement R (Reason)
- Evaluate both and relationship

Example:
Assertion: REST APIs should use stateless communication.
Reason: This allows the server to scale more easily.

A) Both A and R are true, and R explains A ✓
B) Both A and R are true, but R doesn't explain A
C) A is true, R is false
D) A is false, R is true
```

---

## Accessibility Considerations

### Visual Impairments

```
DO:
- Use clear, readable formatting
- Provide text alternatives for diagrams
- Ensure screen reader compatibility
- Use sufficient color contrast

DON'T:
- Rely only on color to convey information
- Use images without alt text
- Create complex visual layouts
```

### Cognitive Load

```
DO:
- Keep questions concise
- Use simple sentence structure
- Define technical terms in question
- Break complex questions into parts

DON'T:
- Use double negatives
- Include irrelevant information
- Require excessive working memory
- Rush time limits
```

### Language Considerations

```
DO:
- Use clear, simple English
- Avoid idioms and colloquialisms
- Define acronyms on first use
- Allow extra time for non-native speakers

DON'T:
- Use culture-specific references
- Rely on wordplay or puns
- Use overly complex vocabulary
```

---

## Phase-Specific Implementation

### Phase 1 (Zero-Backend-LLM)

```
Backend (deterministic):
- Store questions in database/R2
- Grade using answer key (exact match)
- Track scores in progress database
- Enforce freemium limits

ChatGPT (intelligent):
- Present questions with personality
- Provide educational explanations
- Encourage and motivate
- Adapt tone to performance
```

### Phase 2 (Hybrid Premium)

```
Additional capabilities:
- LLM-graded free-form answers
- Personalized question selection
- Adaptive difficulty
- Detailed feedback generation
- Weakness pattern analysis

Requirements:
- Premium gate
- User-initiated
- Cost tracking
```

### Phase 3 (Web App)

```
Additional features:
- Rich interactive UI
- Timer display
- Progress visualization
- Drag-drop interfaces
- Instant feedback animations
- Quiz history dashboard
- Achievement badges display
```

---

## Quiz Security (Anti-Cheating)

### Question Randomization

```
- Shuffle question order
- Shuffle answer options
- Generate unique quiz instances
- Use question pools (select random subset)
```

### Time Management

```
- Set reasonable time limits
- Track time per question
- Flag suspiciously fast completion
- Allow pauses with limits
```

### Academic Integrity Messaging

```
Frame quizzes as:
- Learning tools, not just assessment
- Safe space to make mistakes
- Progress tracking for YOU
- Practice makes perfect

Avoid:
- High-pressure language
- Over-emphasis on scores
- Comparison to others
```
