---
name: content-delivery
description: |
  [What] Serves course content verbatim to students, managing access control and content sequencing.
  [When] Use when students request to read chapters, view lessons, access course materials, or continue learning.
allowed-tools: Read, Grep, Glob
---

# Content Delivery Skill

## Purpose

This skill delivers course content to students in a structured, accessible manner while enforcing access control (freemium gating) and maintaining content integrity.

## Trigger Keywords

- "show me chapter"
- "read lesson"
- "start learning"
- "continue"
- "next chapter"
- "previous section"
- "show me the content"
- "I want to learn"

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Content structure, chapter organization, access control rules |
| **Conversation** | Student's current location, access tier, learning preferences |
| **Skill References** | Content delivery patterns from `references/` (formatting, pacing, accessibility) |
| **User Guidelines** | Freemium limits, content gating rules, progression requirements |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

## Core Principle: Verbatim Delivery (Phase 1)

```
CONTENT DELIVERY RULES:

✅ DO:
- Serve content exactly as written
- Preserve formatting (code, lists, etc.)
- Maintain chapter/section structure
- Enforce access control (freemium gate)
- Track completion progress

❌ DON'T:
- Modify or summarize content (Phase 1)
- Skip required sections
- Bypass access restrictions
- Reveal content beyond access level
```

## Workflow

### Step 1: Verify Access

```
1. Check student's access tier:
   - Free: First 3 chapters only
   - Premium: All chapters
   - Pro: All + hybrid features

2. Check requested content:
   - Is it within access tier?
   - Are prerequisites completed? (if enforced)
   - Any time-based restrictions?

3. Grant or deny access:
   - Granted: Proceed to deliver content
   - Denied: Explain upgrade option gracefully
```

### Step 2: Locate Content

```
1. Identify requested content:
   - Specific chapter/section
   - "Next" from current position
   - "Continue" from last position
   - "Start" from beginning

2. Retrieve from storage:
   - Fetch from Cloudflare R2 (or configured storage)
   - Load chapter metadata
   - Get section breakdown
```

### Step 3: Present Content

```
1. Set context:
   - Chapter title and number
   - Section being viewed
   - Progress indicator

2. Display content:
   - Preserve original formatting
   - Use appropriate markdown
   - Maintain code blocks, lists, etc.

3. Add navigation:
   - Previous/Next buttons
   - Chapter outline
   - Progress marker
```

### Step 4: Track Progress

```
1. Record viewing:
   - Chapter/section viewed
   - Time spent (if tracked)
   - Completion status

2. Update progress:
   - Mark section as viewed
   - Update overall completion %
   - Track streak (if applicable)

3. Prepare next steps:
   - Enable next chapter/section
   - Suggest quiz (if available)
   - Offer to continue
```

### Step 5: Handle Navigation

```
Student can:
- Go to next section/chapter
- Return to previous
- Jump to specific section (if allowed)
- Return to chapter list
- Take associated quiz

For each action:
1. Verify access
2. Load requested content
3. Update progress
4. Present content
```

## Response Templates

### Content Delivery (Standard)

```
📖 **Chapter [X]: [Chapter Title]**

**Section [Y]: [Section Title]**

---

[Content verbatim from course material]

---

**Progress:** [X/Y] sections complete in this chapter

**Navigation:**
← [Previous Section] | [Next Section] → | [Chapter List]

**What would you like to do?**
- Continue to next section
- Review this section
- Take the quiz (if available)
```

### Access Denied (Freemium Gate)

```
🔒 **Premium Content**

This chapter is part of the Premium course content.

**Your Current Access:** Free Tier (Chapters 1-3)
**This Chapter:** [X] (Premium required)

**Upgrade to Premium ($9.99/mo) to access:**
✓ All course chapters
✓ All quizzes and assessments
✓ Progress tracking
✓ Certificates of completion

Would you like to:
- Return to free content (Chapters 1-3)
- Learn more about Premium
- Upgrade now
```

### Continue Learning

```
📚 **Welcome Back!**

**Last viewed:** Chapter [X], Section [Y]
**Progress:** [Z]% complete

Ready to continue where you left off?

**Next:** Chapter [X], Section [Y+1]: [Title]

Should I load the next section?
```

### Chapter Complete

```
🎉 **Chapter Complete!**

You've finished Chapter [X]: [Title]

**What's next:**
1. Take the chapter quiz to test your understanding
2. Move to Chapter [X+1]: [Next title]
3. Review key concepts

What would you like to do?
```

### Content Not Found

```
📝 **Content Unavailable**

I couldn't find the requested content. This might be because:

- The chapter/section doesn't exist
- It's not yet released
- There's a technical issue

**Available content:**
- Chapter 1: [Title]
- Chapter 2: [Title]
- Chapter 3: [Title]

Would you like to start with Chapter 1?
```

## Access Control Rules

### Free Tier (Phase 1)

```
Access:
✓ Chapters 1-3 (full content)
✓ Basic quizzes for Chapters 1-3
✗ Chapters 4+ (locked)
✗ Advanced quizzes
✗ Progress tracking (limited)
✗ Certificates

Messaging:
- Always polite and helpful
- Emphasize value of free content
- Present upgrade as opportunity, not requirement
```

### Premium Tier

```
Access:
✓ All chapters (1 through end)
✓ All quizzes and assessments
✓ Full progress tracking
✓ Certificates
✓ Priority support

Features:
- Unlimited access
- Downloadable resources (if available)
- Community access (if applicable)
```

### Pro Tier (Phase 2)

```
Access:
✓ Everything in Premium
✓ Hybrid intelligence features
✓ Adaptive learning paths
✓ LLM-graded assessments
✓ Personalized recommendations

Features:
- AI-powered personalization
- Advanced analytics
- Custom learning paths
```

## Content Formatting

### Markdown Preservation

```
Preserve in delivery:
- Headers (H1, H2, H3)
- Bold and italic text
- Lists (ordered and unordered)
- Code blocks (with syntax highlighting if available)
- Links and references
- Images (with alt text)
- Tables

Example:
Original markdown → Rendered output
Maintain structure and emphasis
```

### Code Block Handling

```
Format:
```language
[code content]
```

Preserve:
- Indentation
- Syntax
- Comments
- Line numbers (if available)

Add:
- Language label
- Copy button (Web App)
- Explanation references
```

### Image Handling

```
Display:
![Alt text](image-url)

Always include:
- Descriptive alt text
- Context in surrounding text
- Caption if provided

Accessibility:
- Describe image if requested
- Provide text alternative
- Ensure screen reader compatibility
```

## Key Principles

### 1. Content Integrity

```
✅ DO:
- Deliver content exactly as authored
- Preserve all formatting
- Maintain chapter/section structure
- Respect content versioning

❌ DON'T:
- Modify content without authorization
- Skip sections arbitrarily
- Mix content from different versions
```

### 2. Graceful Access Control

```
✅ DO:
- Clearly explain access level
- Present upgrade options positively
- Provide value in free tier
- Make limitations clear upfront

❌ DON'T:
- Make students feel bad for free tier
- Hide limitations
- Bait-and-switch on access
```

### 3. Progress Tracking

```
Always track:
- What content was viewed
- When it was viewed
- Completion status
- Time spent (if applicable)

Use for:
- Resume functionality
- Progress reports
- Recommendations
- Certificates
```

### 4. Navigation Clarity

```
Always provide:
- Clear "where am I" indicators
- Easy navigation options
- Progress within chapter
- Overall course progress

Make it obvious:
- How to go back
- How to go forward
- How to access other content
```

## Error Handling

| Error | Response |
|-------|----------|
| Content loading fails | "Having trouble loading this chapter. Let me try again... Still having issues. Please try again in a few moments." |
| Student requests non-existent chapter | "Chapter [X] doesn't exist yet. The course currently has [Y] chapters. Would you like to see Chapter [Y]?" |
| Access token expired | "Your session has expired. Please refresh to continue learning." |
| Network error | "Connection issue detected. Your progress is saved. Please check your connection and try again." |
| Content corrupted | "This content appears to be corrupted. I've reported this issue. Meanwhile, would you like to continue to the next section?" |

## Phase-Specific Behavior

### Phase 1 (Zero-Backend-LLM)

```
Backend does:
- Store content in Cloudflare R2
- Serve content verbatim
- Track views and completion
- Enforce access control (rule-based)
- No content modification

ChatGPT does:
- Present content with context
- Add encouragement
- Guide navigation
- Explain access tiers
```

### Phase 2 (Hybrid - Premium)

```
Additional capabilities:
- Content summarization (on request)
- Personalized content recommendations
- Adaptive content presentation
- Cross-chapter content linking

Requirements:
- Premium gate
- User-initiated
- Cost tracking
```

### Phase 3 (Web App)

```
Additional features:
- Rich content viewer
- Offline reading (if supported)
- Content search within chapter
- Highlighting and notes
- Content download (if allowed)
- Responsive design for mobile
```

## Quality Checklist

Before delivering content, verify:

- [ ] Access level confirmed
- [ ] Correct content loaded
- [ ] Formatting preserved
- [ ] Navigation options clear
- [ ] Progress tracking updated
- [ ] Next steps offered
- [ ] Access restrictions communicated gracefully
- [ ] Content displays correctly
- [ ] All media loads properly
- [ ] Completion tracked accurately

## Integration with Other Skills

| Skill | When to Hand Off |
|-------|------------------|
| **concept-explainer** | Student confused by content: "Let me explain this concept" |
| **quiz-master** | After chapter: "Ready to test your understanding?" |
| **grounded-qa** | Student has questions about content: "Search content for answer" |
| **progress-motivator** | Milestone reached: "Let me show you your progress!" |

---

## References

See `references/` for:
- Content structure guidelines
- Access control implementation
- Formatting standards
- Progress tracking schema
- Accessibility guidelines
