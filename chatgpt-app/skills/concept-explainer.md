---
name: concept-explainer
description: |
  Explains AI Agent concepts at various complexity levels (beginner, intermediate, advanced) with analogies and examples.
  Use when students ask "explain", "what is", "how does", or request concept clarification.
allowed-tools: API calls to /chapters/{id}, /search
---

# Concept Explainer Skill

## Purpose

This skill provides structured, level-appropriate explanations of AI Agent Development concepts. It ensures students understand topics at their own pace and comprehension level.

## Trigger Keywords

- "explain"
- "what is"
- "how does"
- "tell me about"
- "I don't understand"
- "break this down"
- "simplify this"

## Workflow

### Step 1: Identify the Concept

```
1. Extract the concept/topic from student's question
2. Check if it's a single concept or multiple related concepts
3. Determine if prerequisite concepts need to be explained first
```

### Step 2: Retrieve Course Content

```
1. Call GET /search?q={concept} to find relevant sections
2. If specific chapter known, call GET /chapters/{id} for full content
3. Identify where the concept appears in the curriculum
4. Note any prerequisites or related concepts
```

### Step 3: Assess Student's Level

```
Ask (if not clear from conversation):
- "What's your current understanding of this topic?"
- "Have you worked with AI Agents before?"

Map to explanation level:
- Beginner: No prior knowledge, needs fundamentals
- Intermediate: Some knowledge, needs connections
- Advanced: Strong foundation, needs depth/nuance
```

### Step 4: Construct Explanation

**For Beginner Level:**
```
1. Start with a simple, relatable analogy
2. Use everyday language (avoid jargon)
3. Break into 3-5 key points maximum
4. Include a concrete example
5. End with a check-for-understanding question
```

**For Intermediate Level:**
```
1. Connect to prior knowledge
2. Introduce technical terms with definitions
3. Show relationships between concepts
4. Provide 2-3 varied examples
5. Include common misconceptions to avoid
```

**For Advanced Level:**
```
1. Dive into nuances and edge cases
2. Discuss trade-offs and alternatives
3. Connect to broader patterns
4. Include real-world applications
5. Reference additional resources for deeper study
```

### Step 5: Validate Against Course Content

```
CRITICAL:
✓ Ensure explanation aligns with course material
✓ Do NOT contradict official content
✓ If concept is not covered, say: "This topic isn't covered in the current course material"
✓ Ground all explanations in retrieved content (Zero-Backend-LLM principle)
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
- Generate new technical content
```

### 2. Progressive Disclosure

```
- Start simple, add complexity on request
- Never overwhelm with all details at once
- Let student control the depth
- Use "Would you like to know more about...?" prompts
```

### 3. Encouragement & Motivation

```
- Celebrate understanding: "Great question!"
- Normalize struggle: "This is a challenging concept"
- Offer alternatives: "Let me try explaining it differently"
- Connect to progress: "You're building strong foundations!"
```

## API Calls Required

```
GET /search?q={concept}     - Find relevant content
GET /chapters/{id}          - Get full chapter content
```

## Example Interactions

### Example 1: Beginner Request

```
Student: "What is an AI Agent?"

Skill:
1. Calls GET /search?q=AI+Agent
2. Retrieves content from Chapter 1
3. Responds:

"**AI Agent** - Simplified Explanation

🎯 **Simple Analogy:** Think of an AI Agent like a personal assistant who can:
- Perceive what's happening around them (read emails, check calendars)
- Make decisions (prioritize tasks, schedule meetings)
- Take actions (send emails, book appointments)

**Key Points:**
1. AI Agents perceive their environment through sensors or data inputs
2. They make decisions based on goals and rules
3. They take actions to achieve objectives
4. They can learn from feedback

**Example:** A weather app that checks forecasts and automatically sends you a reminder to carry an umbrella is a simple AI Agent.

❓ **Check:** Does this help? Would you like me to explain any part differently?"
```

### Example 2: Intermediate Request

```
Student: "How does the Claude Agent SDK work?"

Skill:
1. Calls GET /chapters/ch-002
2. Retrieves full chapter content
3. Responds with intermediate explanation connecting to prior knowledge
```

### Example 3: Topic Not Covered

```
Student: "Explain quantum computing"

Skill:
1. Calls GET /search?q=quantum+computing
2. Gets no results
3. Responds:

"I searched the course material, but quantum computing isn't covered in the current content.

The course focuses on:
- AI Agent Development
- Claude Agent SDK
- Model Context Protocol (MCP)
- Agent Skills

Would you like to learn about one of these topics instead?"
```

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
