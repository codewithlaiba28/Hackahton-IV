---
name: concept-explainer
description: |
  [What] Explains educational concepts at various complexity levels (beginner, intermediate, advanced) with analogies and examples.
  [When] Use when students ask "explain", "what is", "how does", or request concept clarification at a specific level.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Concept Explainer Skill

## Purpose

This skill provides structured, level-appropriate explanations of course concepts. It ensures students understand topics at their own pace and comprehension level.

## Trigger Keywords

- "explain"
- "what is"
- "how does"
- "tell me about"
- "I don't understand"
- "break this down"
- "simplify this"

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Course content structure, chapter organization, concept hierarchy |
| **Conversation** | Student's current level, specific concept they're struggling with, preferred explanation style |
| **Skill References** | Educational explanation patterns from `references/` (Bloom's taxonomy, analogy techniques, scaffolding methods) |
| **User Guidelines** | Course-specific terminology, forbidden simplifications, accuracy requirements |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

## Workflow

### Step 1: Identify the Concept

```
1. Extract the concept/topic from student's question
2. Check if it's a single concept or multiple related concepts
3. Determine if prerequisite concepts need to be explained first
```

### Step 2: Assess Student's Level

```
1. Ask (if not specified): "What's your current understanding of this topic?"
2. Map to explanation level:
   - Beginner: No prior knowledge, needs fundamentals
   - Intermediate: Some knowledge, needs connections
   - Advanced: Strong foundation, needs depth/nuance
```

### Step 3: Retrieve Course Content

```
1. Search course materials for the concept
2. Identify where it appears in the curriculum
3. Note any prerequisites or related concepts
4. Check if content exists in:
   - Chapter materials
   - Glossary
   - Quiz banks
   - Supplementary resources
```

### Step 4: Construct Explanation

**For Beginner Level:**
- Start with a simple, relatable analogy
- Use everyday language (avoid jargon)
- Break into 3-5 key points maximum
- Include a concrete example
- End with a check-for-understanding question

**For Intermediate Level:**
- Connect to prior knowledge
- Introduce technical terms with definitions
- Show relationships between concepts
- Provide 2-3 varied examples
- Include common misconceptions to avoid

**For Advanced Level:**
- Dive into nuances and edge cases
- Discuss trade-offs and alternatives
- Connect to broader patterns
- Include real-world applications
- Reference additional resources for deeper study

### Step 5: Validate Against Course Content

```
1. Ensure explanation aligns with course material
2. Do NOT contradict official content
3. If concept is not covered, say: "This topic isn't covered in the current course material"
4. Ground all explanations in provided content (Zero-Backend-LLM principle)
```

### Step 6: Deliver with Encouragement

```
1. Present explanation in clear, formatted structure
2. Use bold/italics for emphasis
3. Include visual formatting (lists, code blocks if applicable)
4. End with: "Does this make sense? Would you like me to explain any part differently?"
```

## Response Templates

### Beginner Template

```
**[Concept Name]** - Simplified Explanation

🎯 **Simple Analogy:** [Relatable comparison]

**Key Points:**
1. [Point 1 in simple language]
2. [Point 2 in simple language]
3. [Point 3 in simple language]

**Example:** [Concrete, everyday example]

❓ **Check:** Does this help? Would you like me to clarify anything?
```

### Intermediate Template

```
**[Concept Name]** - Intermediate Explanation

📚 **Building on what you know:** [Connection to prior concepts]

**Technical Definition:** [Precise definition]

**How It Works:**
- [Mechanism point 1]
- [Mechanism point 2]
- [Mechanism point 3]

**Example:** [Technical example with explanation]

⚠️ **Common Misconception:** [What students often get wrong]

❓ **Next:** Want to dive deeper or try a practice question?
```

### Advanced Template

```
**[Concept Name]** - Advanced Explanation

🔍 **Deep Dive:**

**Nuances & Edge Cases:**
- [Nuance 1]
- [Nuance 2]

**Trade-offs:**
| Approach | Pros | Cons |
|----------|------|------|
| [Option A] | [...] | [...] |

**Real-World Application:** [Industry/practical use case]

📖 **Further Reading:** [References to additional resources]

❓ **Explore:** Want to discuss implications or work through an advanced problem?
```

## Key Principles

### 1. Grounded Explanations (Zero-Backend-LLM)

```
✅ DO:
- Explain using only course-provided content
- Say "not covered" for topics outside curriculum
- Serve content verbatim when possible

❌ DON'T:
- Hallucinate information not in course materials
- Make claims not supported by content
- Generate new technical content (pre-generate only)
```

### 2. Progressive Disclosure

```
- Start simple, add complexity on request
- Never overwhelm with all details at once
- Let student control the depth
- Use "Would you like to know more about...?" prompts
```

### 3. Socratic Approach Integration

```
- After explaining, ask guiding questions
- Connect to socratic-tutor skill for deeper learning
- Encourage critical thinking, not just memorization
```

### 4. Encouragement & Motivation

```
- Celebrate understanding: "Great question!"
- Normalize struggle: "This is a challenging concept"
- Offer alternatives: "Let me try explaining it differently"
- Connect to progress: "You're building strong foundations!"
```

## Error Handling

| Error | Response |
|-------|----------|
| Concept not in course material | "This topic isn't covered in the current course. Let me show you what IS covered related to this..." |
| Student asks for opinion | "Based on the course material, here's what we know..." |
| Concept requires prerequisites | "To understand this well, you should first know [X]. Should we review that first?" |
| Multiple concepts asked | "I see several concepts here. Let's start with [X], then move to [Y]. Sound good?" |

## Integration with Other Skills

| Skill | When to Hand Off |
|-------|------------------|
| **quiz-master** | After explanation, offer: "Want to test your understanding with a quiz?" |
| **socratic-tutor** | If student says "I'm still confused" or "help me think through this" |
| **progress-motivator** | After successful understanding, celebrate: "Let me show you your progress!" |
| **grounded-qa** | For specific factual questions about course content |

## Quality Checklist

Before delivering any explanation, verify:

- [ ] Explanation level matches student's needs
- [ ] All information is grounded in course content
- [ ] Analogy is accurate and helpful (not misleading)
- [ ] Technical terms are defined when introduced
- [ ] Examples are relevant and clear
- [ ] Formatting aids readability
- [ ] Check-for-understanding question included
- [ ] Encouraging tone maintained
- [ ] No hallucinated or unsupported claims
- [ ] Prerequisites identified if needed

## Phase-Specific Behavior

### Phase 1 (Zero-Backend-LLM)

```
- Explanations MUST come from ChatGPT's reasoning
- Backend serves content verbatim only
- No LLM calls in backend for summarization
- All adaptation happens in ChatGPT App
```

### Phase 2 (Hybrid - Premium)

```
- Advanced explanations may use backend LLM for:
  - Cross-chapter synthesis
  - Personalized learning path integration
  - Adaptive difficulty adjustment
- Must be premium-gated and user-initiated
```

### Phase 3 (Web App)

```
- Full explanation capabilities
- Integrated with LMS dashboard
- Progress tracking visible
- Rich media support (diagrams, videos if available)
```

---

## References

See `references/` for:
- Educational explanation patterns
- Bloom's taxonomy implementation
- Analogy construction techniques
- Course-specific concept mappings
- Common student misconceptions database
