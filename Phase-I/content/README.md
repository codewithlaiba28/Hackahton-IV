# Course Content Seed Script

This script seeds all 5 chapters and 25 quiz questions into the database and Cloudflare R2.

## Setup Instructions

1. **Install dependencies:**
   ```bash
   cd backend
   uv pip install -e .
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and R2 credentials
   ```

3. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

4. **Run seed script:**
   ```bash
   python -m seed.seed_chapters
   python -m seed.seed_quizzes
   ```

## Chapter Content

### Chapter 1: Introduction to AI Agents (Free)
- **File:** `content/ch-001-intro-to-agents.md`
- **Status:** ✅ Created
- **Content:** AI Agent basics, types, characteristics, examples

### Chapter 2: Claude Agent SDK (Free)
- **File:** `content/ch-002-claude-agent-sdk.md`
- **Status:** ⏳ TODO
- **Content:** SDK overview, installation, basic agent creation, examples

### Chapter 3: MCP Basics (Free)
- **File:** `content/ch-003-mcp-basics.md`
- **Status:** ⏳ TODO
- **Content:** Model Context Protocol, resources, prompts, tools

### Chapter 4: Agent Skills (Premium)
- **File:** `content/ch-004-agent-skills.md`
- **Status:** ⏳ TODO
- **Content:** Skill design, triggers, workflows, best practices

### Chapter 5: Agent Factory Architecture (Premium)
- **File:** `content/ch-005-agent-factory.md`
- **Status:** ⏳ TODO
- **Content:** Factory pattern, spec-driven development, automation

## Quiz Questions

Each chapter has 5 questions (mix of MCQ and True/False):

### Chapter 1 Quiz
1. What is the primary characteristic of an AI Agent? (MCQ)
2. True/False: Simple reflex agents maintain internal state
3. Which agent type maximizes a satisfaction metric? (MCQ)
4. True/False: AI Agents can only react, not take initiative
5. What are the four key characteristics of AI Agents? (MCQ)

### Chapter 2-5 Quizzes
- Similar structure (5 questions each)
- Mix of recall and understanding questions
- Aligned with chapter learning objectives

## Remaining Work

### Content Creation (4 chapters)
- [ ] Chapter 2: Claude Agent SDK (800+ words)
- [ ] Chapter 3: MCP Basics (800+ words)
- [ ] Chapter 4: Agent Skills (800+ words)
- [ ] Chapter 5: Agent Factory (800+ words)

### Quiz Creation (4 quizzes × 5 questions)
- [ ] Chapter 2 quiz (5 questions)
- [ ] Chapter 3 quiz (5 questions)
- [ ] Chapter 4 quiz (5 questions)
- [ ] Chapter 5 quiz (5 questions)

### Seed Scripts
- [ ] `seed_chapters.py` - Upload to R2 + insert metadata
- [ ] `seed_quizzes.py` - Insert quiz questions

## File Structure

```
content/
├── ch-001-intro-to-agents.md          ✅
├── ch-002-claude-agent-sdk.md         ⏳
├── ch-003-mcp-basics.md               ⏳
├── ch-004-agent-skills.md             ⏳
├── ch-005-agent-factory.md            ⏳
└── quizzes/
    ├── ch-001-quiz.json               ⏳
    ├── ch-002-quiz.json               ⏳
    ├── ch-003-quiz.json               ⏳
    ├── ch-004-quiz.json               ⏳
    └── ch-005-quiz.json               ⏳

backend/seed/
├── __init__.py                        ✅
├── seed_chapters.py                   ⏳
└── seed_quizzes.py                    ⏳
```

## Next Steps

1. Create remaining 4 chapter Markdown files
2. Create 5 quiz JSON files (25 questions total)
3. Implement seed scripts
4. Run seeds against database
5. Verify content accessible via API

---

**Status:** Chapter 1 complete. 4 chapters + 20 questions remaining.
