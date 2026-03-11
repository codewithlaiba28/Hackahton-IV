# Grounded Q&A Patterns

## Search Algorithm Patterns

### Keyword Matching

```
Exact Match:
- Search for exact keyword/phrase
- Case-insensitive by default
- Include plural/singular variations

Example:
Search: "API"
Matches: "API", "api", "APIs", "apis"
```

### Stemming

```
Reduce words to root form:

Running → Run
Connections → Connect
Implementations → Implement

Benefits:
- Broader matching
- Fewer missed results
- Better recall
```

### Synonym Expansion

```
Expand search terms:

API → "API", "Application Programming Interface"
DB → "DB", "Database"
HTTP → "HTTP", "Hypertext Transfer Protocol"

Implementation:
- Maintain synonym dictionary
- Use course glossary
- Include common abbreviations
```

### Proximity Search

```
Find words near each other:

Query: "REST API"
Match: "APIs that follow REST principles" (close)
Don't match: "REST. [50 words] API" (far)

Configurable window:
- Same sentence (strict)
- Same paragraph (medium)
- Same section (loose)
```

---

## Content Indexing Strategies

### Chapter-Based Index

```
Structure:
{
  "chapter_1": {
    "title": "Introduction to APIs",
    "sections": [...],
    "keywords": ["API", "interface", "communication"],
    "concepts": ["API definition", "API types"]
  },
  "chapter_2": {...}
}
```

### Concept Map Index

```
Structure:
{
  "API": {
    "defined_in": "chapter_1",
    "used_in": ["chapter_1", "chapter_3", "chapter_5"],
    "related_to": ["HTTP", "REST", "endpoint"],
    "prerequisites": []
  },
  "REST": {
    "defined_in": "chapter_3",
    "used_in": ["chapter_3", "chapter_4"],
    "related_to": ["API", "HTTP", "stateless"],
    "prerequisites": ["API"]
  }
}
```

### Full-Text Index

```
Inverted index for fast search:

{
  "API": ["doc_1:para_3", "doc_3:para_1", "doc_5:para_7"],
  "REST": ["doc_3:para_1", "doc_3:para_5", "doc_4:para_2"],
  ...
}

Enables:
- Fast keyword lookup
- Boolean queries (AND, OR, NOT)
- Frequency ranking
```

---

## Citation Format Examples

### Academic Style

```
"As defined in Chapter 1, Section 2:
'An API (Application Programming Interface) defines how
software components interact.'

(Source: Course Material, Chapter 1)"
```

### Informal Style

```
"From Chapter 1:
APIs are how software components talk to each other.

The course explains..."
```

### Inline Citation

```
"An API defines software interactions (Chapter 1).
This means programs can communicate without knowing
implementation details (Chapter 1, Section 3)."
```

### Footnote Style

```
"APIs enable software communication.¹
They define interfaces between components.²

---
¹ Chapter 1, Introduction
² Chapter 1, Section 2"
```

---

## Handling Ambiguous Queries

### Clarification Strategy

```
When query is unclear:

1. Acknowledge the question
2. Identify ambiguity
3. Offer interpretations
4. Ask for clarification

Example:
Student: "What about the thing we learned?"

Response:
"I want to make sure I answer correctly! 
When you say 'the thing,' are you referring to:
- The API concept from Chapter 1?
- The REST principles from Chapter 3?
- Something else?

Can you be more specific?"
```

### Context Recovery

```
Use conversation history:

Student: "What about the authentication one?"
(Previous topic was API security)

Response:
"Building on our discussion about API security:

The course covers authentication in Chapter 5:
'[Quote about authentication methods]'

Specifically, it mentions..."
```

---

## Question Classification

### Factual Questions

```
Characteristics:
- Ask for definitions
- Ask for specific information
- Have clear answers in content

Example: "What does API stand for?"

Strategy:
- Direct keyword search
- Return exact definition
- Cite source
```

### Conceptual Questions

```
Characteristics:
- Ask for understanding
- Require synthesis
- May span multiple sections

Example: "How do REST APIs work?"

Strategy:
- Search for concept
- Gather related content
- Synthesize explanation
- Cite multiple sources
```

### Comparative Questions

```
Characteristics:
- Ask to compare concepts
- Require understanding differences

Example: "What's the difference between REST and SOAP?"

Strategy:
- Find content about each
- Identify comparison points
- Present differences clearly
- Note if comparison not in content
```

### Application Questions

```
Characteristics:
- Ask how to use knowledge
- Require practical guidance

Example: "When should I use REST?"

Strategy:
- Find use cases in content
- Extract guidance
- Note if not covered
- Suggest related covered topics
```

---

## Answer Quality Rubric

| Criterion | Excellent (5) | Good (3) | Needs Work (1) |
|-----------|---------------|----------|----------------|
| **Accuracy** | Fully content-backed | Mostly accurate | Contains errors |
| **Completeness** | Fully answers question | Partial answer | Incomplete |
| **Citation** | Clear, specific | General reference | Missing |
| **Clarity** | Easy to understand | Mostly clear | Confusing |
| **Conciseness** | No wasted words | Some verbosity | Rambling |
| **Helpfulness** | Provides next steps | Basic answer | Leaves hanging |

---

## Common Edge Cases

### Case 1: Outdated Content

```
Student: "But I heard [new development]..."

Response:
"The course content was created before that development.
Here's what the course covers:

[Content from course]

For the latest developments, you'd need to consult
external resources beyond the course."
```

### Case 2: Conflicting Information

```
Student: "Chapter 2 says X, but Chapter 5 says Y..."

Response:
"Good observation! Let me show you both:

Chapter 2: '[quote]'
Chapter 5: '[quote]'

This might be:
- Different contexts
- Evolution of understanding
- An error in the content

Let me check if there's clarification..."
```

### Case 3: Student Misremembers

```
Student: "I thought the course said [incorrect]..."

Response:
"I understand the confusion. Let me show you what the course actually says:

'[Exact quote from content]'

I see how this might be confusing. The key point is..."
```

### Case 4: Question Requires Inference

```
Student: "So does that mean [inference]?"

Response:
"The course doesn't explicitly state that, but based on what it covers:

[Relevant content]

From this, your inference seems reasonable, though the course
doesn't make that claim directly."
```

---

## Phase-Specific Implementation

### Phase 1 (Zero-Backend-LLM)

```
Backend (deterministic):
- Keyword search over content
- Return exact matches
- No summarization
- No LLM calls

ChatGPT (intelligent):
- Formulate answers from results
- Add explanations
- Handle edge cases
- Cite sources
```

### Phase 2 (Hybrid Premium)

```
Additional capabilities:
- Semantic search (embeddings)
- Content summarization
- Cross-chapter synthesis
- Personalized explanations

Requirements:
- Premium gate
- User-initiated
- Cost tracking
```

### Phase 3 (Web App)

```
Additional features:
- Visual search interface
- Highlighted results
- Jump-to-source
- Search history
- Bookmarks
- Saved searches
```

---

## Search Query Optimization

### Query Expansion

```
Original: "API auth"
Expanded: "API" OR "Application Programming Interface"
          AND
          "auth" OR "authentication" OR "authorization"

Benefits:
- Better recall
- Handles variations
- More comprehensive
```

### Query Weighting

```
Weight terms by importance:

Query: "REST API best practices"

Weights:
- "REST": 1.0 (specific)
- "API": 0.8 (common)
- "best practices": 1.2 (specific phrase)

Rank results by weighted match score.
```

### Negative Queries

```
Exclude unwanted terms:

Query: "API -SOAP"
Meaning: Find API content, exclude SOAP

Use when:
- Student wants distinction
-排除无关内容
- Focus on specific aspect
```

---

## Content Snippet Extraction

### Optimal Snippet Size

```
For definitions: 1-2 sentences
For concepts: 1 paragraph
For examples: Full example + context
For procedures: Complete step sequence

Goal: Enough context to understand, not overwhelm
```

### Snippet Formatting

```
Highlight matched terms:
"An **API** defines how software components interact."

Use ellipsis for omitted text:
"An API defines... interactions. It specifies..."

Preserve formatting:
- Code blocks remain code
- Lists remain lists
- Tables remain tables
```

---

## Accessibility Considerations

### Screen Reader Compatibility

```
- Use semantic markup
- Provide alt text for images
- Ensure citations are clear
- Avoid visual-only indicators
```

### Cognitive Load

```
- Keep answers focused
- Break long answers into sections
- Use clear headings
- Provide summaries
```

### Language Considerations

```
- Define technical terms
- Avoid idioms
- Use clear, simple English
- Provide glossary references
```
