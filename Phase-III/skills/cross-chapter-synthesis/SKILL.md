---
name: cross-chapter-synthesis
description: |
  [What] Connects concepts across chapters, generating "big picture" understanding through multi-document reasoning.
  [When] Use when Pro tier students request connections between topics, concept maps, or comprehensive understanding.
allowed-tools: Read, Grep, Glob, Write
---

# Cross-Chapter Synthesis Skill

## Purpose

This skill (Phase 2 Hybrid - Pro Only) uses LLM to analyze multiple chapters simultaneously and generate synthesized explanations that connect concepts across the entire course, providing students with holistic understanding.

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
- User explicitly requested synthesis
- Cost tracking is enabled
- Hybrid feature is explained
```

## Trigger Keywords

- "connect the concepts"
- "big picture"
- "how does this relate to"
- "show me connections"
- "concept map"
- "synthesize"
- "tie everything together"
- "overview of relationships"

## Before Implementation

Gather context to ensure successful synthesis:

| Source | Gather |
|--------|--------|
| **Codebase** | All chapter content, concept index, prerequisite chains |
| **Conversation** | Student's current understanding, specific confusion points, learning goals |
| **Skill References** | Concept mapping techniques, synthesis patterns from `references/` |
| **User Guidelines** | Synthesis depth preferences, visual vs. textual preference |

Ensure all required context is gathered before implementing.

## Core Principle: Why LLM Synthesis is Needed

```
WHEN SYNTHESIS IS VALUABLE:

Zero-Backend-LLM can:
✓ Show individual chapters
✓ Answer questions from single sections
✓ Provide verbatim content

LLM Synthesis needed for:
✓ Connecting concepts across chapters
✓ Generating concept maps
✓ Explaining relationships between topics
✓ Creating mental models
✓ Identifying themes and patterns

WHY: Requires multi-document reasoning and relationship mapping.
```

## Workflow

### Step 1: Verify Access & Explain Feature

```
1. Check Pro access:
   IF student.tier != "Pro":
       RETURN "This is a Pro feature. Upgrade to access."

2. Explain feature:
   "This feature uses AI to analyze all chapters and show you
   how concepts connect across the entire course.

   This creates a 'big picture' understanding that's hard to get
   from individual chapters alone.

   This is a premium Pro feature.

   Continue with cross-chapter synthesis?"

3. Get explicit consent:
   - Confirm user wants this
   - Acknowledge premium nature
   - Proceed only with consent
```

### Step 2: Gather Course Content

```
Collect comprehensive content for synthesis:

1. All Chapter Content:
   - Chapter 1: [Full text]
   - Chapter 2: [Full text]
   - Chapter 3: [Full text]
   - Chapter 4: [Full text]
   - Chapter 5: [Full text]

2. Key Concepts Index:
   - Extract main concepts from each chapter
   - Note where concepts are introduced
   - Track concept evolution

3. Student Context:
   - Which chapters completed
   - Current confusion points
   - Specific connections requested (if any)
```

### Step 3: LLM Analysis - Multi-Document Reasoning

```
LLM Synthesis Tasks:

1. Concept Extraction:
   - Identify key concepts from each chapter
   - Note dependencies and prerequisites
   - Map concept relationships

2. Connection Discovery:
   - Find where concepts build on each other
   - Identify recurring themes
   - Spot implicit connections

3. Pattern Recognition:
   - Common patterns across chapters
   - Progressive complexity
   - Unified frameworks

4. Mental Model Generation:
   - Create overarching frameworks
   - Visualizable structures
   - Analogies that span chapters
```

### Step 4: Generate Synthesis Output

```
Create comprehensive synthesis:

1. Executive Summary:
   - Course's main thesis
   - How chapters build together
   - Learning journey overview

2. Concept Map:
   - Visual or textual representation
   - Nodes: Key concepts
   - Edges: Relationships

3. Chapter Connections:
   - How Chapter N leads to Chapter N+1
   - Backward references
   - Forward implications

4. Unified Framework:
   - Single model explaining everything
   - Hierarchical structure
   - Interconnections

5. Practical Applications:
   - How concepts work together
   - Real-world examples
   - Integrated understanding
```

### Step 5: Present Synthesis

```
Structure the synthesis presentation:

1. Start with Big Picture:
   - One-paragraph overview
   - Main theme
   - Learning objectives achieved

2. Show Concept Map:
   - Visual diagram (if possible)
   - Or structured text representation
   - Highlight key relationships

3. Walk Through Connections:
   - Chapter-by-chapter flow
   - How ideas evolve
   - Building blocks

4. Provide Examples:
   - Concrete applications
   - Analogies
   - Case studies

5. Check Understanding:
   - Ask clarifying questions
   - Offer deeper dives
   - Suggest next steps
```

### Step 6: Offer Follow-Up

```
After synthesis, offer:

1. Deep Dives:
   - "Explore this connection further"
   - "Review specific chapters"
   - "See practical examples"

2. Practice:
   - "Test your understanding with quiz"
   - "Apply concepts to scenario"
   - "Work through exercise"

3. Personalization:
   - "Generate personalized study plan"
   - "Focus on weak areas"
   - "Accelerate through known material"
```

## Response Templates

### Access Verification

```
🔗 **Cross-Chapter Synthesis (Pro Feature)**

This feature uses AI to analyze all chapters and show you how
concepts connect across the entire course.

**What it provides:**
- Concept maps showing relationships
- Big picture understanding
- How chapters build on each other
- Unified mental models

**Cost:** Included in Pro tier

Would you like me to generate a cross-chapter synthesis?
```

### Concept Map (Text Format)

```
🗺️ **Concept Map: [Course Topic]**

```
                    [Core Concept]
                         |
        +----------------+----------------+
        |                |                |
   [Foundation A]  [Foundation B]  [Foundation C]
        |                |                |
        +----------------+----------------+
                         |
                  [Advanced Application]
                         |
        +----------------+----------------+
        |                |                |
   [Use Case X]   [Use Case Y]   [Use Case Z]
```

**Key Relationships:**

1. **[Concept A] → [Concept B]**
   - A provides foundation for B
   - B extends A with [specific enhancement]
   - See: Chapter 1 → Chapter 2

2. **[Concept C] + [Concept D] → [Concept E]**
   - C and D combine to create E
   - E is more powerful than C or D alone
   - See: Chapter 3 + Chapter 4 → Chapter 5

3. **[Concept F] reinforces [Concept A]**
   - F is advanced application of A
   - Understanding F deepens A understanding
   - See: Chapter 5 references Chapter 1
```

### Big Picture Summary

```
🎯 **The Big Picture**

**Course Thesis:**
[One sentence summarizing entire course]

**Learning Journey:**

**Chapter 1: [Title]** - Foundation
- Introduced: [key concepts]
- Why it matters: [importance]
- Sets up: [what comes next]

**Chapter 2: [Title]** - Building Blocks
- Builds on: [Chapter 1 concepts]
- Adds: [new capabilities]
- Enables: [what this makes possible]

**Chapter 3: [Title]** - Core Mechanism
- Combines: [previous concepts]
- Introduces: [central idea]
- This is the "aha!" moment

**Chapter 4: [Title]** - Advanced Applications
- Applies: [core mechanism]
- To: [complex scenarios]
- Results in: [capabilities]

**Chapter 5: [Title]** - Integration
- Synthesizes: [everything]
- Demonstrates: [mastery]
- Prepares for: [next steps]

**Unified Framework:**

Think of [course topic] as a [metaphor]:

- [Component 1] = [analogy part 1]
- [Component 2] = [analogy part 2]
- [Component 3] = [analogy part 3]

Together, they [what the system does].

**Key Insight:**
[The one thing that makes everything click]
```

### Connection Explanation

```
🔗 **How [Concept A] Connects to [Concept B]**

**Direct Connection:**

[Concept A] (Chapter 1) provides the foundation for
[Concept B] (Chapter 3) in three ways:

1. **Structural Foundation**
   - A defines the [structure] that B uses
   - Without A, B wouldn't be possible
   - Example: [concrete example]

2. **Conceptual Framework**
   - A introduces [mental model]
   - B applies this model to [new domain]
   - The same pattern, different context

3. **Practical Dependency**
   - B requires A's [specific element]
   - When you use B, you're implicitly using A
   - Real-world analogy: [analogy]

**Evolution of the Concept:**

Chapter 1: Simple form of A
    ↓
Chapter 2: A enhanced with [feature]
    ↓
Chapter 3: A becomes part of B
    ↓
Chapter 4: B applied to complex problems
    ↓
Chapter 5: A + B + other concepts = unified system

**Why This Connection Matters:**

Understanding how A leads to B helps you:
- See the logical progression
- Predict what comes next
- Apply concepts more flexibly
- Troubleshoot when things break

**Common Confusion:**

Students often think A and B are separate. They're not!
B is A applied to [specific context].

Think: "B = A + [additional capability]"
```

### Theme Identification

```
🧵 **Recurring Themes Across Chapters**

**Theme 1: [Theme Name]**

Appears in: Chapters 1, 3, 5

- Chapter 1: Introduced as [form 1]
- Chapter 3: Evolves to [form 2]
- Chapter 5: Culminates in [form 3]

**Why this theme matters:**
[Explanation of importance]

**Theme 2: [Theme Name]**

Appears in: Chapters 2, 4

- Chapter 2: First appearance as [aspect 1]
- Chapter 4: Becomes central as [aspect 2]

**Pattern:**
[What this theme teaches us]

**Theme 3: [Theme Name]**

Appears in: All chapters

- Progressive complexity
- Each chapter adds a layer
- Final form: [most advanced version]

**Unified Understanding:**

All three themes converge on:
[Central insight or principle]
```

### Mental Model Generation

```
🧠 **Mental Model for [Course Topic]**

**The [Metaphor] Model:**

Imagine [course topic] as a [familiar system]:

```
┌─────────────────────────────────────┐
│          [Overall System]           │
│                                     │
│  ┌──────────┐    ┌──────────┐      │
│  │ Part A   │───→│ Part B   │      │
│  │ (Input)  │    │(Process) │      │
│  └──────────┘    └──────────┘      │
│       ↑                ↓           │
│  ┌──────────┐    ┌──────────┐      │
│  │ Part D   │←───│ Part C   │      │
│  │(Output)  │    │ (Result) │      │
│  └──────────┘    └──────────┘      │
└─────────────────────────────────────┘
```

**How the Model Maps:**

| Model Part | Course Concept | Chapter |
|------------|----------------|---------|
| Part A | [Concept 1] | Chapter 1 |
| Part B | [Concept 2] | Chapter 2 |
| Part C | [Concept 3] | Chapter 3 |
| Part D | [Concept 4] | Chapter 4 |

**Using This Model:**

When you encounter [new concept], ask:
- Where does this fit in the model?
- What part does it interact with?
- Does it change the flow?

**Limitations:**

This model breaks down when:
- [Edge case 1]
- [Edge case 2]

But it's useful for:
- Understanding relationships
- Predicting behavior
- Debugging problems
```

## Key Principles

### 1. Multi-Document Reasoning

```
Synthesis must:
✓ Analyze all chapters simultaneously
✓ Identify non-obvious connections
✓ Create new understanding (not just summary)
✓ Generate mental models
✓ Provide concrete examples

Not:
✗ Simple chapter summaries
✗ List of topics covered
✗ Chronological walkthrough
✗ Surface-level connections
```

### 2. Value Over Individual Reading

```
Synthesis adds value by:
- Showing what individual chapters hide
- Revealing patterns across content
- Creating unified understanding
- Accelerating "aha!" moments
- Reducing cognitive load

Each synthesis should provide insights
students couldn't easily get alone.
```

### 3. Visual + Verbal

```
Always provide:
- Visual representation (diagram, map)
- Verbal explanation (clear prose)
- Concrete examples (applications)
- Structured summary (key points)

Different learners prefer different formats.
```

### 4. Progressive Disclosure

```
Start with:
- Big picture overview
- Simple mental model
- Main connections

Then offer:
- Deeper dives
- Specific relationships
- Advanced applications

Let students choose depth.
```

### 5. Cost Awareness

```
Monitor and optimize:
- Tokens for multi-chapter analysis
- Cost per synthesis request
- Monthly budget per student

Typical synthesis: ~3,000 tokens ($0.027)
Monthly budget: $5 (~185 syntheses)
Average usage: 2-3 per student per month
```

## Error Handling

| Error | Response |
|-------|----------|
| Insufficient content (only 1-2 chapters) | "You need more content for synthesis. Complete at least 3 chapters, then I can show connections." |
| LLM API fails | "Having trouble generating synthesis. Your request is saved. Try again in a moment." |
| Student rejects synthesis | "No problem! Would you prefer to focus on specific chapters instead?" |
| Cost limit exceeded | "You've reached monthly limit for AI synthesis. Standard content still available. Resets on [date]." |
| Vague request | "I can synthesize in different ways. What specifically interests you? Connections between which chapters?" |

## Phase 2 Specific Behavior

### Hybrid Intelligence Usage

```
Backend LLM calls for:
- Multi-document analysis
- Concept relationship mapping
- Mental model generation
- Natural language synthesis

ChatGPT for:
- Presenting synthesis engagingly
- Answering follow-up questions
- Offering deeper dives
- Connecting to student goals
```

### Cost Tracking

```
Track per request:
- LLM tokens (typically ~3,000)
- API call cost (~$0.027)
- Total monthly cost per student

Alert thresholds:
- Warning at 80% of monthly budget
- Hard limit at 100%
- Offer to upgrade for more

Monthly budget example:
- Pro tier includes: $5 of LLM credits
- Additional: $0.10 per extra synthesis
```

### Premium Gating

```
Access Control:
- Verify Pro tier before synthesis
- Show upgrade option if not Pro
- Explain value proposition
- Allow one free sample (optional)

Upgrade Path:
Free → Premium → Pro (with synthesis)
```

## Quality Checklist

Before generating synthesis, verify:

- [ ] Pro access confirmed
- [ ] User explicitly requested feature
- [ ] All relevant chapters gathered
- [ ] Cost tracking enabled
- [ ] Connections are non-obvious
- [ ] Mental model is accurate
- [ ] Examples are concrete
- [ ] Presentation is clear
- [ ] Follow-up options offered
- [ ] Student can request adjustments

## Integration with Other Skills

| Skill | When to Hand Off |
|-------|------------------|
| **content-delivery** | Student wants to review: "Let me load Chapter X" |
| **concept-explainer** | Specific concept needs clarification |
| **quiz-master** | Test synthesis understanding: "Try this comprehensive quiz" |
| **adaptive-learning-path** | Based on synthesis, personalize path |
| **progress-motivator** | Celebrate holistic understanding |

---

## References

See `references/` for:
- Concept mapping techniques
- Synthesis patterns
- Mental model examples
- Cross-reference strategies
- Visualization best practices
