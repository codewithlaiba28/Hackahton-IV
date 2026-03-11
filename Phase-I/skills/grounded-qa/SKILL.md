---
name: grounded-qa
description: |
  [What] Answers student questions using ONLY course-provided content, ensuring accuracy and preventing hallucination.
  [When] Use when students ask factual questions about course material, request clarification, or seek information from the curriculum.
allowed-tools: Read, Grep, Glob
---

# Grounded Q&A Skill

## Purpose

This skill provides accurate, content-grounded answers to student questions by searching and referencing course materials. It strictly adheres to the Zero-Backend-LLM principle by only using provided content.

## Trigger Keywords

- "what does [concept] mean"
- "where does it say"
- "according to the course"
- "in chapter X"
- "is [X] covered"
- "find information about"
- "search for"
- "tell me from the content"

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Course content structure, chapter organization, content indexing |
| **Conversation** | Student's specific question, context, what they're trying to understand |
| **Skill References** | Search patterns from `references/` (keyword matching, content retrieval, citation formats) |
| **User Guidelines** | Course-specific content organization, citation requirements, access levels |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

## Core Principle: Zero-Backend-LLM

```
GROUNDED Q&A RULES:

✅ DO:
- Answer ONLY from course-provided content
- Say "not covered" for topics outside curriculum
- Quote content verbatim when appropriate
- Cite specific chapters/sections
- Acknowledge uncertainty if content is unclear

❌ DON'T:
- Hallucinate information not in content
- Use external knowledge to fill gaps
- Make claims not supported by content
- Generate new technical content
- Call LLM APIs for answers (Phase 1)
```

## Workflow

### Step 1: Understand the Question

```
1. Parse student's question:
   - What concept/topic are they asking about?
   - What specific information do they need?
   - Is this a factual question or conceptual?

2. Determine search strategy:
   - Keyword search for specific terms
   - Concept search for broader topics
   - Cross-reference for related concepts
```

### Step 2: Search Course Content

```
1. Search in order:
   a. Glossary (if exists)
   b. Current chapter
   c. Related chapters
   d. All course materials

2. Search methods:
   - Keyword matching
   - Synonym matching (if index exists)
   - Section header scanning
   - Full-text search

3. Collect relevant passages:
   - Extract exact quotes
   - Note chapter/section locations
   - Identify context around matches
```

### Step 3: Evaluate Search Results

```
Decision Tree:

Found relevant content?
├── Yes → Proceed to Step 4
└── No → Check for related content
    ├── Found related → "Not directly covered, but..."
    └── Nothing found → "This topic isn't covered in the course"

Content clear and unambiguous?
├── Yes → Answer confidently
└── No → "The course mentions this briefly..."
```

### Step 4: Construct Grounded Answer

**Answer Structure:**

```
1. Direct Answer (from content)
   - Start with the answer
   - Use content's language/definitions
   - Quote when appropriate

2. Citation
   - "According to Chapter X, Section Y..."
   - "As stated in [chapter title]..."
   - "The course explains..."

3. Context (if helpful)
   - Related concepts from content
   - Prerequisites mentioned
   - Examples from content

4. Offer More
   - "Would you like me to explain further?"
   - "Should we review the full section?"
   - "Want to see related topics?"
```

### Step 5: Handle Edge Cases

**Question Outside Course Scope:**
```
"This topic isn't covered in the current course material.

The course focuses on:
- [Related topic 1]
- [Related topic 2]

Would you like to learn about these instead?
```

**Question Partially Covered:**
```
"The course mentions [X] briefly in Chapter [N], but doesn't go into depth.

Here's what it says:
[Quote from content]

For more detailed coverage, you might need external resources.
```

**Ambiguous Question:**
```
"I want to make sure I answer correctly. Are you asking about:
- [Interpretation A], or
- [Interpretation B]?

Or something else?
```

**Multiple Topics in One Question:**
```
"I see several concepts in your question. Let me address each:

1. [Topic A]: [Answer from content]
2. [Topic B]: [Answer from content]

Would you like me to elaborate on any of these?
```

## Response Templates

### Direct Answer (Content Found)

```
📖 **From the Course:**

[Direct answer using course content]

**Source:** Chapter [X], Section [Y]: "[Quote if helpful]"

**Related:** This connects to [related concept] covered in [Chapter Z].

Would you like me to explain further or find more information?
```

### Partial Answer (Limited Content)

```
📝 **What the Course Covers:**

The course mentions [topic] in [Chapter X]:

"[Relevant quote]"

However, this topic isn't covered in depth. The course focuses more on [related topics that ARE covered].

Would you like to:
- Review what IS covered?
- Move to a related topic?
```

### Not Covered (No Content Found)

```
❌ **Not in Course Material**

I searched the course content, and [topic] isn't covered.

**What IS covered:**
- [Related topic 1]
- [Related topic 2]
- [Related topic 3]

Would you like to learn about one of these instead?
```

### Clarification Needed

```
🤔 **Let Me Clarify**

I want to give you the most helpful answer. Are you asking about:

A) [Interpretation 1]
B) [Interpretation 2]
C) Something else?

Or can you rephrase your question?
```

### Cross-Reference Answer

```
🔗 **Connected Concepts**

Your question about [X] relates to several chapters:

**Chapter A:** [Brief summary of relevant content]
**Chapter B:** [Brief summary of relevant content]

**Key connection:** [How concepts relate]

Would you like me to elaborate on any of these?
```

## Search Strategies

### Keyword Search

```
Process:
1. Extract keywords from question
2. Search content for exact matches
3. Also search for variations:
   - Plurals
   - Different tenses
   - Abbreviations
   - Acronyms

Example:
Question: "What are APIs?"
Search: "API", "APIs", "Application Programming Interface"
```

### Concept Search

```
Process:
1. Identify core concept
2. Find where concept is introduced
3. Track where it's used throughout
4. Gather all relevant mentions

Example:
Concept: "REST"
Find: Introduction, principles, examples, comparisons
```

### Context Search

```
Process:
1. Find keyword/concept
2. Read surrounding paragraphs
3. Understand full context
4. Extract complete explanation

Why: Single sentences may lack necessary context
```

## Content Citation Formats

### Simple Citation

```
"According to Chapter 3: [content]"
```

### Detailed Citation

```
"From Chapter 3, Section 2 ('REST Principles'):
'[exact quote]'
(Page/Section ID if available)"
```

### Summary Citation

```
"Chapter 5 explains that [summary]. Specifically:
- Point 1
- Point 2
- Point 3"
```

### Cross-Reference Citation

```
"This is covered in multiple places:
- Chapter 2 introduces the concept
- Chapter 4 provides examples
- Chapter 7 discusses advanced applications"
```

## Key Principles

### 1. Accuracy Over Completeness

```
✅ DO:
- Give accurate, content-backed answers
- Admit when content is limited
- Point to what IS available

❌ DON'T:
- Fabricate details not in content
- Guess at answers
- Present external knowledge as course content
```

### 2. Verbatim When Appropriate

```
Use exact quotes when:
- Definition is precise
- Wording matters
- Technical accuracy required

Paraphrase when:
- Content is lengthy
- Simplification helps understanding
- Multiple sections need synthesis
```

### 3. Clear Attribution

```
Always make clear:
- What comes from course content
- Where in the content it's from
- If answer is complete or partial

Never imply:
- External knowledge is from course
- Inference is stated fact
- Partial answer is complete
```

### 4. Helpful Redirects

```
When content doesn't exist:
- Acknowledge the gap
- Suggest related covered topics
- Offer to search for alternatives
- Don't leave student empty-handed
```

## Error Handling

| Error | Response |
|-------|----------|
| Content search fails | "I'm having trouble searching right now. Let me try again... Still having issues. Can you tell me which chapter this might be in?" |
| Student asks for opinion | "The course presents [X perspective]. Here's what it says: [quote]" |
| Student asks about current events | "The course content was created before recent developments. Here's what it covers: [content]" |
| Student wants external resources | "The course doesn't link to external resources. But based on what's covered, you understand the fundamentals!" |
| Contradiction in content | "I notice the content mentions this in two places with slightly different explanations. Let me show you both..." |

## Phase-Specific Behavior

### Phase 1 (Zero-Backend-LLM)

```
Backend does:
- Store content in searchable format
- Provide keyword search API
- Return exact content matches
- No summarization or LLM calls

ChatGPT does:
- Formulate answers from search results
- Add context and explanation
- Cite sources clearly
- Handle edge cases gracefully
```

### Phase 2 (Hybrid - Premium)

```
Additional capabilities (premium-gated):
- Semantic search (embeddings)
- Cross-chapter synthesis
- Summarization of long content
- Personalized explanations based on history

Requirements:
- Premium gate
- User-initiated
- Cost tracking
```

### Phase 3 (Web App)

```
Additional features:
- In-content search UI
- Highlighted search results
- Jump-to-source navigation
- Search history
- Saved answers/bookmarks
```

## Quality Checklist

Before answering, verify:

- [ ] Answer is grounded in course content
- [ ] Source/chapter is cited
- [ ] No hallucinated information
- [ ] Unclear gaps are acknowledged
- [ ] Quotes are accurate (if used)
- [ ] Answer addresses the question
- [ ] Redirects offered if content limited
- [ ] Language is clear and accessible
- [ ] Technical terms defined (from content)
- [ ] Offer for follow-up included

## Integration with Other Skills

| Skill | When to Hand Off |
|-------|------------------|
| **concept-explainer** | Student needs deeper explanation: "Let me explain this concept more thoroughly" |
| **quiz-master** | After answering: "Want to test your understanding with a quiz?" |
| **socratic-tutor** | Student wants to explore: "Let's think through this together" |
| **progress-motivator** | Student discouraged by gaps: "Let me show you how much you've learned!" |

---

## References

See `references/` for:
- Search algorithm patterns
- Content indexing strategies
- Citation format examples
- Handling ambiguous queries
- Course content structure guide
