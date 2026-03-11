---
name: navigation-guide
description: |
  [What] Helps students navigate through course content, suggesting optimal paths and managing chapter sequencing.
  [When] Use when students ask "what's next", "where should I go", "how is this organized", or need guidance on learning path.
allowed-tools: Read, Grep, Glob
---

# Navigation Guide Skill

## Purpose

This skill guides students through the course structure, helping them navigate chapters, understand prerequisites, and follow optimal learning paths.

## Trigger Keywords

- "what's next"
- "where should I go"
- "how is this organized"
- "show me the path"
- "learning path"
- "course structure"
- "chapter order"
- "what should I learn"
- "guide me through"

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Course structure, chapter dependencies, prerequisite chains |
| **Conversation** | Student's current position, goals, pace, any constraints |
| **Skill References** | Navigation patterns from `references/` (path optimization, prerequisite mapping) |
| **User Guidelines** | Recommended paths, required sequences, optional content markers |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

## Workflow

### Step 1: Understand Student's Position

```
1. Determine current location:
   - What chapter/section are they on?
   - What have they completed?
   - What's their progress percentage?

2. Understand their goal:
   - Complete the course?
   - Learn specific topic?
   - Quick refresher?
   - Prepare for assessment?

3. Check constraints:
   - Access tier (Free/Premium/Pro)
   - Time availability
   - Prerequisites completed
```

### Step 2: Analyze Course Structure

```
1. Map the learning path:
   - Required chapters
   - Optional chapters
   - Prerequisite chains
   - Branching paths (if any)

2. Identify optimal next steps:
   - Next required chapter
   - Recommended optional content
   - Quiz checkpoints
   - Milestone markers
```

### Step 3: Present Navigation Options

```
1. Show current position:
   - "You are here: Chapter X, Section Y"
   - Progress: Z% complete
   - Time estimate to completion

2. Present options:
   - Continue forward (default)
   - Review previous content
   - Jump to specific topic (if allowed)
   - Take assessment

3. Provide recommendations:
   - "Most students continue to..."
   - "Recommended next: ..."
   - "Optional but helpful: ..."
```

### Step 4: Guide the Journey

```
For each navigation decision:

1. Confirm choice:
   - "Ready to move to Chapter X+1?"
   - "Would you like to review first?"

2. Provide context:
   - "Next, you'll learn about..."
   - "This builds on what you just learned..."
   - "Key concepts coming up:..."

3. Set expectations:
   - "This chapter has 5 sections"
   - "Expect to spend 30-45 minutes"
   - "There's a quiz at the end"

4. Execute navigation:
   - Load requested content
   - Update progress
   - Enable next steps
```

### Step 5: Handle Detours

```
If student wants to skip ahead:
- Check if prerequisites met
- Warn about missing context
- Suggest reviewing prerequisites
- Allow if Premium (with warning)

If student wants to review:
- Show previously completed content
- Highlight key concepts
- Offer targeted review sections
- Track review separately

If student is lost:
- Show full course map
- Explain where they are
- Suggest best path forward
- Offer to create custom path
```

## Response Templates

### Course Overview

```
📚 **Course Structure**

**Course Title:** [Name]
**Total Chapters:** [X]
**Your Progress:** [Y]% complete

**Chapters:**
1. [Chapter 1 Title] ✓ (Completed)
2. [Chapter 2 Title] ✓ (Completed)
3. [Chapter 3 Title] 📍 (Current)
4. [Chapter 4 Title] 🔒 (Locked/Next)
5. [Chapter 5 Title] 🔒 (Locked)
...

**Estimated Completion:** [Z] hours remaining

Where would you like to go?
```

### Next Step Recommendation

```
➡️ **Recommended Next Step**

**Current:** Chapter [X], Section [Y]

**Next:** Chapter [X], Section [Y+1]: [Title]

**Why:** This continues your learning journey in order.

**What you'll learn:**
- [Key concept 1]
- [Key concept 2]

**Time:** ~[Z] minutes

Ready to continue?
```

### Learning Path Overview

```
🗺️ **Your Learning Path**

**Starting Point:** Chapter 1 (Introduction)
**Current Position:** Chapter [X] ([Y]% complete)
**Destination:** Chapter [Z] (Course Completion)

**Path:**
✓ Chapters 1-[X-1]: Completed
📍 Chapter [X]: In Progress
📍 Chapters [X+1]-[Z]: Ahead

**Milestones:**
- Next: Complete Chapter [X]
- Then: Take Mid-Course Quiz
- Finally: Complete Final Project

Stay on this path?
```

### Prerequisite Warning

```
⚠️ **Prerequisite Check**

You're trying to access Chapter [X], but:

**Missing Prerequisites:**
- Chapter [Y]: [Title] (Not completed)
- Chapter [Z]: [Title] (Not completed)

**Why this matters:**
Chapter [X] builds on concepts from these chapters.
Skipping may make it difficult to understand.

**Options:**
1. Complete prerequisites first (recommended)
2. Preview Chapter [X] (limited understanding)
3. View prerequisite summary (quick review)

What would you like to do?
```

### Jump to Topic

```
🎯 **Jump to Topic: [Topic Name]**

**Found in:**
- Chapter [X]: [Section Y] (Primary coverage)
- Chapter [A]: [Section B] (Related coverage)

**Prerequisites:**
✓ You've completed required background
⚠️ You may want to review [concept] first

**Recommended approach:**
1. Start with Chapter [X], Section [Y]
2. Review related sections if needed
3. Take quiz to confirm understanding

Ready to jump to Chapter [X]?
```

### Review Mode

```
🔄 **Review Mode**

**Select what to review:**

**Recent:**
- Chapter [X]: [Title] (Last viewed)
- Chapter [X-1]: [Title]

**Key Concepts:**
- [Concept 1] (Chapter [A])
- [Concept 2] (Chapter [B])

**Full Course:**
- All chapters (for comprehensive review)

What would you like to review?
```

## Navigation Patterns

### Linear Path (Default)

```
Chapter 1 → Chapter 2 → Chapter 3 → ... → Final

Characteristics:
- Fixed sequence
- Each chapter builds on previous
- Prerequisites enforced
- Best for: Foundational learning
```

### Branching Path

```
        Chapter 3A (Advanced)
       /
Chapter 2 → Chapter 3B (Standard)
       \
        Chapter 3C (Applied)

Characteristics:
- Core content + specialization tracks
- Student chooses branch
- Different outcomes per branch
- Best for: Customized learning
```

### Modular Path

```
Module 1 (Required)
Module 2 (Choose 2 of 3)
Module 3 (Required)
Module 4 (Choose 1 of 2)

Characteristics:
- Required + elective structure
- Flexibility within constraints
- Multiple valid paths
- Best for: Advanced learners
```

### Adaptive Path (Phase 2)

```
Pre-assessment → Personalized path based on knowledge
    ↓
High score → Skip basics, advanced content
    ↓
Medium score → Standard path
    ↓
Low score → Additional foundation content

Characteristics:
- Path adjusts to student
- Based on assessment/results
- Optimizes learning time
- Requires: Hybrid intelligence
```

## Key Principles

### 1. Clear Orientation

```
Always help student know:
- Where they are
- Where they've been
- Where they can go
- What's recommended

Use visual indicators:
✓ Completed
📍 Current
📍 Next
🔒 Locked/Not accessible
```

### 2. Respect Prerequisites

```
Enforce when:
- Critical for understanding
- Safety/compliance required
- Certification depends on it

Warn when:
- Helpful but not critical
- Student has alternative knowledge
- Student insists on skipping

Allow skip when:
- Student accepts risk
- Premium tier (if policy allows)
- Self-directed learning mode
```

### 3. Multiple Valid Paths

```
Acknowledge that:
- Different learners have different needs
- Some students want depth, others breadth
- Review is valid and valuable
- Skipping ahead (with prerequisites) can work

Support:
- Linear progression (default)
- Topic-based navigation
- Review paths
- Custom learning goals
```

### 4. Progress Visibility

```
Always show:
- Completion percentage
- Chapters/sections completed
- Time invested (if tracked)
- Estimated time remaining
- Next milestones

Celebrate:
- Chapter completions
- Milestone achievements
- Consistency (streaks)
- Course completion
```

## Error Handling

| Error | Response |
|-------|----------|
| Student tries to access locked content | "This content requires [Premium/Prerequisites]. Here's how to unlock..." |
| Navigation fails (technical) | "Having trouble loading that section. Let me try again... Still having issues. Your progress is saved." |
| Student is "lost" | "No worries! Let me show you the course map and where you are..." |
| Prerequisite not met | "To access this, you'll need to complete [X] first. Want to go there now?" |
| Invalid chapter/section | "That chapter/section doesn't exist. Here are the available chapters..." |

## Phase-Specific Behavior

### Phase 1 (Zero-Backend-LLM)

```
Backend does:
- Store course structure
- Track student position
- Enforce access control
- Record completion

ChatGPT does:
- Present navigation options
- Recommend next steps
- Explain course structure
- Guide learning path
```

### Phase 2 (Hybrid - Premium)

```
Additional capabilities:
- Adaptive path generation
- Personalized recommendations
- Learning style optimization
- Predictive path suggestions

Requirements:
- Premium gate
- User-initiated
- Cost tracking
```

### Phase 3 (Web App)

```
Additional features:
- Visual course map
- Interactive navigation
- Progress visualization
- Drag-and-drop path customization
- Social path sharing (optional)
```

## Quality Checklist

Before guiding navigation, verify:

- [ ] Student's current position identified
- [ ] Access level confirmed
- [ ] Prerequisites checked
- [ ] Options clearly presented
- [ ] Recommendations explained
- [ ] Next steps actionable
- [ ] Progress visible
- [ ] Warnings given (if skipping)
- [ ] Alternative paths offered
- [ ] Student's goals considered

## Integration with Other Skills

| Skill | When to Hand Off |
|-------|------------------|
| **content-delivery** | Student ready to view content: "Let me load Chapter X" |
| **concept-explainer** | Student confused about path: "Let me explain how this connects" |
| **quiz-master** | At checkpoint: "Ready for the chapter quiz?" |
| **progress-motivator** | Milestone reached: "Let me show you your progress!" |

---

## References

See `references/` for:
- Course structure templates
- Prerequisite mapping patterns
- Learning path optimization
- Navigation UI patterns
- Accessibility guidelines
