# Course Companion FTE - Agent Skills Documentation

## Overview

This document lists all Agent Skills created for the **Course Companion FTE** project as specified in Hackahton.md (Section 8 - Agent Skills Design).

**Total Skills Created:** 10

---

## Skill Inventory by Phase

### Phase 1: Zero-Backend-LLM (Required Runtime Skills)

| # | Skill Name | Type | Purpose | Status |
|---|------------|------|---------|--------|
| 1 | `concept-explainer` | Guide | Explains concepts at various complexity levels | ✅ Complete |
| 2 | `quiz-master` | Guide | Conducts quizzes with encouragement and feedback | ✅ Complete |
| 3 | `socratic-tutor` | Guide | Guides learning through questioning | ✅ Complete |
| 4 | `progress-motivator` | Guide | Celebrates achievements and tracks progress | ✅ Complete |
| 5 | `grounded-qa` | Analyzer | Answers questions using ONLY course content | ✅ Complete |
| 6 | `content-delivery` | Automation | Serves course content verbatim | ✅ Complete |
| 7 | `navigation-guide` | Guide | Helps navigate course structure and paths | ✅ Complete |

### Phase 2: Hybrid Intelligence (Premium Features - Pro Tier)

| # | Skill Name | Type | Purpose | Status |
|---|------------|------|---------|--------|
| 8 | `adaptive-learning-path` | Analyzer | Generates personalized learning recommendations | ✅ Complete |
| 9 | `llm-assessment-grader` | Validator | Evaluates free-form written answers with LLM | ✅ Complete |

### Phase 3: Web App (Full LMS Dashboard)

| # | Skill Name | Type | Purpose | Status |
|---|------------|------|---------|--------|
| 10 | `web-dashboard-manager` | Automation | Manages comprehensive LMS dashboard | ✅ Complete |

---

## Skill Details

### 1. concept-explainer

**Location:** `skills/concept-explainer/`

**Description:** Explains educational concepts at various complexity levels (beginner, intermediate, advanced) with analogies and examples.

**Trigger Keywords:** "explain", "what is", "how does", "tell me about", "I don't understand"

**Key Features:**
- Level-appropriate explanations (Beginner/Intermediate/Advanced)
- Relatable analogies
- Grounded in course content (Zero-Backend-LLM)
- Check-for-understanding questions
- Progressive disclosure

**References:**
- `references/explanation-patterns.md` - Bloom's taxonomy, analogy techniques, scaffolding methods

---

### 2. quiz-master

**Location:** `skills/quiz-master/`

**Description:** Guides students through quizzes with encouragement, presents questions, and provides immediate feedback.

**Trigger Keywords:** "quiz", "test me", "practice", "assess me", "check my understanding"

**Key Features:**
- Multiple question types (MCQ, True/False, Multiple Select, Fill-in-Blank)
- Immediate educational feedback
- Encouraging tone
- Progress tracking integration
- Gamification elements (badges, points)

**References:**
- `references/quiz-patterns.md` - Question design, feedback phrases, difficulty calibration

---

### 3. socratic-tutor

**Location:** `skills/socratic-tutor/`

**Description:** Guides learning through questioning rather than direct answers, helping students discover understanding themselves.

**Trigger Keywords:** "help me think", "I'm stuck", "guide me", "don't just tell me"

**Key Features:**
- Socratic questioning techniques (6 types)
- Hint hierarchy (5 levels)
- Productive struggle support
- Metacognitive prompts
- Scaffolded discovery

**References:**
- `references/socratic-techniques.md` - Question types, hint examples, problem-solving heuristics

---

### 4. progress-motivator

**Location:** `skills/progress-motivator/`

**Description:** Celebrates achievements, maintains motivation, and helps students track their learning progress with encouragement.

**Trigger Keywords:** "my progress", "streak", "how am I doing", "motivate me"

**Key Features:**
- Progress visualization
- Streak tracking
- Achievement badges
- Growth mindset messaging
- Milestone celebrations

**References:**
- `references/motivation-patterns.md` - Growth mindset language, gamification, encouragement phrases

---

### 5. grounded-qa

**Location:** `skills/grounded-qa/`

**Description:** Answers student questions using ONLY course-provided content, ensuring accuracy and preventing hallucination.

**Trigger Keywords:** "what does [concept] mean", "where does it say", "according to the course"

**Key Features:**
- Strict content grounding (Zero-Backend-LLM)
- Keyword and concept search
- Clear citations
- Handles edge cases gracefully
- "Not covered" acknowledgment

**References:**
- `references/search-patterns.md` - Search algorithms, indexing, citation formats

---

### 6. content-delivery

**Location:** `skills/content-delivery/`

**Description:** Serves course content verbatim to students, managing access control and content sequencing.

**Trigger Keywords:** "show me chapter", "read lesson", "continue", "next chapter"

**Key Features:**
- Verbatim content delivery
- Freemium access control
- Progress tracking
- Navigation support
- Format preservation

**Key Principles:**
- Zero-Backend-LLM (Phase 1)
- Content integrity
- Graceful access control

---

### 7. navigation-guide

**Location:** `skills/navigation-guide/`

**Description:** Helps students navigate through course content, suggesting optimal paths and managing chapter sequencing.

**Trigger Keywords:** "what's next", "where should I go", "learning path", "course structure"

**Key Features:**
- Course structure visualization
- Prerequisite checking
- Path recommendations
- Multiple valid paths support
- Progress visibility

**Navigation Patterns:**
- Linear path (default)
- Branching path
- Modular path
- Adaptive path (Phase 2)

---

### 8. adaptive-learning-path

**Location:** `skills/adaptive-learning-path/`

**Description:** Generates personalized learning recommendations by analyzing student patterns, performance, and learning history.

**Trigger Keywords:** "personalized path", "adaptive learning", "recommend me what to study"

**⚠️ Premium Feature:** Pro Tier Only

**Key Features:**
- LLM-powered pattern analysis
- Personalized recommendations
- Strength/weakness identification
- Optimized learning sequences
- Cost-tracked usage

**Hybrid Justification:**
- Requires reasoning over learning data
- Cross-chapter synthesis
- Personalization at scale

**References:**
- Learning analytics patterns
- Personalization algorithms
- Cost optimization strategies

---

### 9. llm-assessment-grader

**Location:** `skills/llm-assessment-grader/`

**Description:** Evaluates free-form written answers using LLM analysis, providing detailed feedback beyond rule-based grading.

**Trigger Keywords:** "grade my answer" (written), "evaluate my response", "written assessment"

**⚠️ Premium Feature:** Pro Tier Only

**Key Features:**
- LLM-powered evaluation
- Detailed educational feedback
- Partial credit recognition
- Misconception identification
- Model answer comparison

**Hybrid Justification:**
- Rule-based can't evaluate reasoning
- Requires semantic understanding
- Nuanced feedback generation

**References:**
- Grading rubric templates
- Feedback phrase library
- Misconception database

---

### 10. web-dashboard-manager

**Location:** `skills/web-dashboard-manager/`

**Description:** Manages the comprehensive LMS dashboard for the Web App, including progress visualization, analytics, and admin features.

**Trigger Keywords:** "dashboard", "analytics", "course management", "admin panel"

**Phase:** Phase 3 (Web App)

**Key Features:**
- Home dashboard with progress overview
- Detailed analytics (charts, trends)
- Course content browser
- Quiz dashboard
- Achievements & gamification
- Settings & preferences
- Admin panel (instructor view)

**Technical Stack:**
- Frontend: Next.js/React, TypeScript, Tailwind CSS
- Visualizations: Recharts/Chart.js
- Backend: FastAPI with full LLM integration

**References:**
- Dashboard component library
- Visualization best practices
- Accessibility guidelines

---

## Skill Architecture

### Skill Structure (All Skills)

```
skill-name/
├── SKILL.md                    # Main skill definition
└── references/
    └── [domain-expertise].md   # Embedded knowledge
```

### SKILL.md Components

Each SKILL.md contains:
1. **YAML Frontmatter** - Name, description, allowed-tools
2. **Purpose** - What the skill accomplishes
3. **Trigger Keywords** - When the skill activates
4. **Before Implementation** - Context gathering guide
5. **Workflow** - Step-by-step procedures
6. **Response Templates** - Example outputs
7. **Key Principles** - Guidelines and constraints
8. **Error Handling** - Edge case responses
9. **Phase-Specific Behavior** - Phase 1/2/3 differences
10. **Quality Checklist** - Verification criteria
11. **Integration Points** - Hand-offs to other skills

---

## Phase Implementation Summary

### Phase 1: Zero-Backend-LLM

**Architecture:**
```
User → ChatGPT App → Deterministic Backend
```

**Skills Active:** 7 skills
- concept-explainer
- quiz-master
- socratic-tutor
- progress-motivator
- grounded-qa
- content-delivery
- navigation-guide

**Backend Responsibilities:**
- Serve content verbatim
- Rule-based quiz grading
- Progress tracking
- Access control
- NO LLM calls

**ChatGPT Responsibilities:**
- All explanations
- Tutoring and encouragement
- Adaptation to student level
- Motivation

---

### Phase 2: Hybrid Intelligence (Premium)

**Architecture:**
```
User → ChatGPT App → Backend → LLM APIs
                    └─→ Deterministic APIs (Phase 1)
```

**Additional Skills:** 2 skills
- adaptive-learning-path (Pro only)
- llm-assessment-grader (Pro only)

**Hybrid Features:**
- Personalized learning paths
- LLM-graded assessments
- Cross-chapter synthesis
- Adaptive recommendations

**Requirements:**
- Premium-gated (Pro tier)
- User-initiated
- Cost-tracked
- Isolated API routes

---

### Phase 3: Web App

**Architecture:**
```
Web App (Next.js) → Backend (FastAPI) → LLM APIs
```

**Additional Skills:** 1 skill
- web-dashboard-manager

**Full Features:**
- All Phase 1 & 2 features
- Rich LMS dashboard
- Interactive visualizations
- Admin features
- Social features (optional)
- Advanced analytics

---

## Skill Integration Matrix

| From \ To | concept-explainer | quiz-master | socratic-tutor | progress-motivator | grounded-qa | content-delivery | navigation-guide |
|-----------|-------------------|-------------|----------------|-------------------|-------------|------------------|------------------|
| **concept-explainer** | - | ✓ After explanation | ✓ If confused | ✓ After understanding | ✓ For facts | ✓ To show content | ✓ For context |
| **quiz-master** | ✓ If struggling | - | ✓ For guided help | ✓ After quiz | ✓ During quiz | ✓ To review | ✓ For path |
| **socratic-tutor** | ✓ For concepts | ✓ For practice | - | ✓ For encouragement | ✓ For facts | ✓ For content | ✓ For direction |
| **progress-motivator** | ✓ To learn more | ✓ To test | ✓ To work through | - | ✓ For questions | ✓ To continue | ✓ For path |
| **grounded-qa** | ✓ For explanation | ✓ For quiz | ✓ For thinking | ✓ For motivation | - | ✓ For source | ✓ For location |
| **content-delivery** | ✓ For explanation | ✓ For quiz | ✓ For help | ✓ For progress | ✓ For questions | - | ✓ For navigation |
| **navigation-guide** | ✓ For concepts | ✓ For checkpoint | ✓ For guidance | ✓ For milestones | ✓ For info | ✓ To load | - |

---

## Cost Analysis

### Phase 1 (Zero-Backend-LLM)

**LLM Cost:** $0 (all intelligence in ChatGPT)

**Infrastructure Cost (10K users):**
- Cloudflare R2: ~$5
- Database: $0-25
- Compute: ~$10
- **Total:** $16-41/month
- **Cost per user:** $0.002-0.004

### Phase 2 (Hybrid - Premium)

**LLM Cost per Request:**
- Adaptive path analysis: ~$0.018
- LLM assessment grading: ~$0.014

**Monthly Budget (Pro tier):**
- Includes: $5 LLM credits (~250-350 requests)
- Overage: $0.10 per additional analysis

### Phase 3 (Web App)

**Full LLM Integration:**
- All features use LLM
- Higher usage expected
- Pricing: Included in Pro tier
- Monitor: Cost per user, usage patterns

---

## Quality Assurance

### Skill Quality Checklist

All skills verified for:
- [x] Clear purpose and description
- [x] Trigger keywords defined
- [x] Workflow documented step-by-step
- [x] Response templates provided
- [x] Key principles articulated
- [x] Error handling covered
- [x] Phase-specific behavior documented
- [x] Integration points identified
- [x] Reference materials included

### Domain Expertise Embedded

Each skill includes:
- Educational best practices
- Domain-specific patterns
- Common misconceptions
- Quality rubrics
- Accessibility considerations

---

## Usage Guidelines

### For Students

**Free Tier:**
- Access to all Phase 1 skills
- Chapters 1-3 content
- Basic quizzes
- Limited progress tracking

**Premium Tier:**
- All chapters
- All quizzes
- Full progress tracking
- Certificates

**Pro Tier:**
- Everything in Premium
- Adaptive learning path
- LLM-graded assessments
- Priority support

### For Instructors/Admins

**Dashboard Access:**
- Student performance analytics
- Content effectiveness metrics
- At-risk student detection
- Content management tools

---

## Future Enhancements

### Potential Additional Skills

1. **peer-collaboration** - Facilitate study groups and peer learning
2. **content-authoring** - Help instructors create course content
3. **analytics-deep-dive** - Advanced learning analytics
4. **mobile-optimizer** - Mobile-specific learning experiences
5. **certification-manager** - Certificate generation and verification

### Phase 4+ Possibilities

- Multi-FTE collaboration (A2A Protocol)
- Advanced agent workflows
- Real-time collaboration features
- VR/AR learning experiences
- Voice-based interactions

---

## References

### Project Documentation

- **Hackahton.md** - Main project specification
- **Agent Factory Architecture** - Overall system design
- **Zero-Backend-LLM vs Hybrid** - Architecture comparison

### Skill Creation Resources

- **skill-creator-pro** - Meta-skill for creating skills
- **SKILL.md templates** - Standard structure
- **Reference patterns** - Domain expertise libraries

### External Resources

- OpenAI Apps SDK documentation
- FastAPI documentation
- Next.js documentation
- Learning science research

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | March 10, 2026 | Initial creation - All 10 skills documented |

---

**Prepared for:** Panaversity Agent Factory Development Hackathon IV

**Project:** Course Companion FTE - Digital Full-Time Equivalent Educational Tutor

**Status:** ✅ All Required Skills Complete
