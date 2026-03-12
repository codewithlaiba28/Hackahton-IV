---
name: web-dashboard-manager
description: |
  [What] Manages the comprehensive LMS dashboard for the Web App, including progress visualization, analytics, and admin features.
  [When] Use when students access the Web App dashboard, view progress analytics, or manage their learning experience.
allowed-tools: Read, Grep, Glob, Write
---

# Web Dashboard Manager Skill

## Purpose

This skill (Phase 3 Web App) provides a comprehensive learning management system (LMS) dashboard with rich progress visualizations, detailed analytics, course management, and administrative features.

## Trigger Keywords

- "dashboard"
- "my progress"
- "analytics"
- "course management"
- "admin panel"
- "statistics"
- "learning insights"
- "web app"

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Dashboard components, analytics APIs, visualization libraries |
| **Conversation** | User role (student/instructor/admin), preferences, goals |
| **Skill References** | Dashboard patterns from `references/` (UX best practices, visualization types, accessibility) |
| **User Guidelines** | Branding, feature flags, role-based access, data privacy |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

## Core Principle: Comprehensive Web Experience

```
WEB APP ADVANTAGES (Phase 3):

✓ Full LMS dashboard
✓ Rich visualizations
✓ Interactive components
✓ Offline capabilities (optional)
✓ Admin features
✓ Social features (optional)
✓ Advanced analytics
✓ Customization options

Unlike ChatGPT App (Phase 1 & 2):
- More screen real estate
- Persistent UI elements
- Complex interactions
- Multi-tasking support
```

## Dashboard Sections

### 1. Home Dashboard (Student View)

```
Components:

┌─────────────────────────────────────────────┐
│  Welcome Back, [Name]!                     │
│  [Streak Counter] [Current Course]         │
├─────────────────────────────────────────────┤
│  Progress Overview                          │
│  [Course Progress Circle Chart]             │
│  65% Complete                               │
│  [████████░░░░░░░░░░░░]                    │
├─────────────────────────────────────────────┤
│  Continue Learning                          │
│  → Chapter 7: Advanced Concepts             │
│  [Resume Button]                            │
├─────────────────────────────────────────────┤
│  Recent Activity                            │
│  • Completed Quiz: Chapter 6 (85%)          │
│  • Studied: 2 hours today                   │
│  • Streak: 12 days 🔥                       │
├─────────────────────────────────────────────┤
│  Recommended Next                           │
│  • Review: Data Structures (due in 2 days)  │
│  • New: Chapter 7, Section 3                │
└─────────────────────────────────────────────┘
```

### 2. Progress Analytics

```
Detailed Progress Page:

┌─────────────────────────────────────────────┐
│  Progress Analytics                         │
├─────────────────────────────────────────────┤
│  Overall Stats                              │
│  ┌──────────┬──────────┬──────────┐        │
│  │  Time    │ Chapters │  Quizzes │        │
│  │  Spent   │ Complete │  Passed  │        │
│  │  24.5h   │   8/12   │   15/18  │        │
│  └──────────┴──────────┴──────────┘        │
├─────────────────────────────────────────────┤
│  Weekly Activity                            │
│  [Bar Chart: Hours per day this week]       │
│  M   T   W   T   F   S   S                  │
│  ██  ███ ██  ████ ██  ░   ░                 │
├─────────────────────────────────────────────┤
│  Quiz Performance Trend                     │
│  [Line Chart: Quiz scores over time]        │
│  100% ┤     ╭───╮                           │
│   80% ┤  ╭──╯   ╰──╮  ╭──                   │
│   60% ┤──╯         ╰──╯                     │
│       Jan  Feb  Mar  Apr  May               │
├─────────────────────────────────────────────┤
│  Topic Mastery                              │
│  [Radar Chart: Skills by topic]             │
│  • APIs: ████████░░ 80%                     │
│  • REST: ███████░░░ 70%                     │
│  • Auth: ██████░░░░ 60%                     │
│  • Testing: █████░░░░░ 50%                  │
└─────────────────────────────────────────────┘
```

### 3. Course Content Browser

```
Course Content Page:

┌─────────────────────────────────────────────┐
│  Course Content                             │
├─────────────────────────────────────────────┤
│  Filter: [All] [Completed] [In Progress]    │
├─────────────────────────────────────────────┤
│  ✓ Chapter 1: Introduction to APIs          │
│    1.1 What is an API?           [✓]       │
│    1.2 API Types                 [✓]       │
│    1.3 REST Basics               [✓]       │
│    [Quiz: 90%]                   [✓]       │
├─────────────────────────────────────────────┤
│  ✓ Chapter 2: HTTP Fundamentals             │
│    [All sections completed]      [✓]       │
├─────────────────────────────────────────────┤
│  📍 Chapter 3: Advanced REST                │
│    3.1 Resource Naming           [✓]       │
│    3.2 HTTP Methods              [✓]       │
│    3.3 Status Codes              [◐] In Progress
│    3.4 Error Handling            [ ]       │
│    [Quiz: Not taken]            [ ]        │
├─────────────────────────────────────────────┤
│  🔒 Chapter 4: Authentication               │
│    [Complete Chapter 3 to unlock]           │
└─────────────────────────────────────────────┘
```

### 4. Quiz Dashboard

```
Quiz Management Page:

┌─────────────────────────────────────────────┐
│  Quiz Dashboard                             │
├─────────────────────────────────────────────┤
│  Available Quizzes                          │
│  ┌─────────────────────────────────────┐   │
│  │ Chapter 1 Quiz                      │   │
│  │ Status: ✓ Completed                 │   │
│  │ Score: 90% (9/10)                   │   │
│  │ Attempts: 1                         │   │
│  │ [Review Answers] [Retake]           │   │
│  └─────────────────────────────────────┘   │
├─────────────────────────────────────────────┤
│  Chapter 3 Quiz                             │
│  Status: ⏳ Ready to Start                 │
│  Questions: 15                              │
│  Time Limit: 30 minutes                     │
│  [Start Quiz]                               │
├─────────────────────────────────────────────┤
│  Practice Quizzes                           │
│  • API Basics (10 questions) [Start]        │
│  • REST Principles (15 questions) [Start]   │
│  • Mixed Practice (25 questions) [Start]    │
└─────────────────────────────────────────────┘
```

### 5. Achievements & Gamification

```
Achievements Page:

┌─────────────────────────────────────────────┐
│  Achievements & Badges                      │
├─────────────────────────────────────────────┤
│  Earned Badges (12/30)                      │
│  ┌─────┬─────┬─────┬─────┐                 │
│  │ 🏅  │ 🔥  │ 💯  │ 📚  │                 │
│  │First│ 7-Day│Perfect│Speed│                │
│  │Steps│ Streak│Score │Learner│               │
│  └─────┴─────┴─────┴─────┘                 │
│  [View All Badges]                          │
├─────────────────────────────────────────────┤
│  In Progress                                │
│  ┌─────────────────────────────────────┐   │
│  │ 30-Day Streak                       │   │
│  │ [███████░░░] 21/30 days             │   │
│  └─────────────────────────────────────┘   │
│  ┌─────────────────────────────────────┐   │
│  │ Course Complete                     │   │
│  │ [████████░░] 8/12 chapters          │   │
│  └─────────────────────────────────────┘   │
├─────────────────────────────────────────────┤
│  Leaderboard (Opt-in)                       │
│  1. Alice Chen - 2,450 pts                  │
│  2. Bob Smith - 2,380 pts                   │
│  3. You - 2,150 pts                         │
│  [View Full Leaderboard]                    │
└─────────────────────────────────────────────┘
```

### 6. Settings & Preferences

```
Settings Page:

┌─────────────────────────────────────────────┐
│  Settings                                   │
├─────────────────────────────────────────────┤
│  Profile                                    │
│  • Name: [Edit]                             │
│  • Email: [Edit]                            │
│  • Avatar: [Upload]                         │
├─────────────────────────────────────────────┤
│  Learning Preferences                       │
│  • Daily Goal: [30 min ▼]                   │
│  • Reminder Time: [9:00 AM ▼]               │
│  • Difficulty: [Adaptive ▼]                 │
│  • Notifications: [Toggle]                  │
├─────────────────────────────────────────────┤
│  Accessibility                              │
│  • Font Size: [Normal ▼]                    │
│  • High Contrast: [Toggle]                  │
│  • Screen Reader Mode: [Toggle]             │
│  • Reduced Motion: [Toggle]                 │
├─────────────────────────────────────────────┤
│  Privacy                                    │
│  • Profile Visibility: [Private ▼]          │
│  • Leaderboard: [Opt-in]                    │
│  • Data Export: [Download]                  │
│  • Delete Account: [Button]                 │
├─────────────────────────────────────────────┤
│  Subscription                               │
│  Current Plan: Pro                          │
│  Renewal: May 15, 2026                      │
│  [Manage Billing] [Upgrade]                 │
└─────────────────────────────────────────────┘
```

### 7. Admin Dashboard (Instructor View)

```
Admin Panel:

┌─────────────────────────────────────────────┐
│  Admin Dashboard                            │
├─────────────────────────────────────────────┤
│  Course Analytics                           │
│  • Total Students: 1,245                    │
│  • Active (7 days): 856                     │
│  • Completion Rate: 68%                     │
│  • Avg Quiz Score: 78%                      │
├─────────────────────────────────────────────┤
│  Student Performance                        │
│  [Table: Student names, progress, scores]   │
│  Name       │ Progress │ Avg Score │ Status │
│  ─────────────────────────────────────────  │
│  Alice C.   │   95%    │    92%    │ ✓      │
│  Bob S.     │   67%    │    78%    │ ◐      │
│  Carol D.   │   34%    │    65%    │ ⚠      │
├─────────────────────────────────────────────┤
│  Content Performance                        │
│  • Most Difficult Chapter: Chapter 5        │
│  • Highest Drop-off: Section 3.2            │
│  • Best Quiz Performance: Chapter 2         │
├─────────────────────────────────────────────┤
│  Manage Content                             │
│  • [Edit Chapters]                          │
│  • [Add Quiz Questions]                     │
│  • [Upload Resources]                       │
│  • [View Version History]                   │
└─────────────────────────────────────────────┘
```

## Key Features

### 1. Real-Time Progress Sync

```
Features:
- Auto-save progress
- Cross-device sync
- Offline mode with sync
- Conflict resolution

Implementation:
- WebSocket for real-time updates
- LocalStorage for offline
- Background sync when online
```

### 2. Interactive Visualizations

```
Chart Types:
- Progress circles
- Bar charts (activity)
- Line charts (trends)
- Radar charts (skills)
- Heat maps (activity)
- Gantt charts (timeline)

Libraries:
- Chart.js / Recharts
- D3.js for custom
- React-Vis
```

### 3. Customization Options

```
Customizable:
- Dashboard layout (drag-drop)
- Color themes
- Widget visibility
- Notification preferences
- Data density
- Sidebar position
```

### 4. Export & Sharing

```
Export Options:
- Progress report (PDF)
- Certificate download
- Data export (JSON/CSV)
- Share achievements (social)
- Transcript generation
```

## Phase 3 Specific Features

### Full LLM Integration

```
Unlike Phase 1 (Zero-Backend-LLM):

Phase 3 Web App uses LLM throughout:
✓ All content delivery
✓ Personalized recommendations
✓ Adaptive assessments
✓ Natural language search
✓ AI tutor integration
✓ Automated feedback

Backend Architecture:
FastAPI → LLM APIs → All Features
```

### Advanced Analytics

```
Available in Phase 3:
- Learning pattern analysis
- Predictive completion dates
- At-risk student detection
- Content effectiveness
- A/B testing results
- Cohort comparisons
```

### Social Features (Optional)

```
If enabled:
- Study groups
- Discussion forums
- Peer code review
- Leaderboards
- Achievement sharing
- Collaborative projects
```

## Technical Implementation

### Frontend Stack

```
Recommended:
- Next.js / React
- TypeScript
- Tailwind CSS
- React Query (data fetching)
- Zustand/Redux (state)
- Recharts/Chart.js (visualizations)
```

### Backend APIs

```
Required Endpoints:

Dashboard:
GET /api/dashboard/overview
GET /api/dashboard/progress
GET /api/dashboard/analytics

Content:
GET /api/courses/{id}/content
GET /api/chapters/{id}
POST /api/progress/track

Quizzes:
GET /api/quizzes/available
POST /api/quizzes/{id}/submit
GET /api/quizzes/{id}/results

Analytics:
GET /api/analytics/personal
GET /api/analytics/activity
POST /api/analytics/export
```

### Data Visualization

```
Key Metrics to Visualize:

1. Progress:
   - Overall completion %
   - Chapter-by-chapter progress
   - Time spent

2. Performance:
   - Quiz scores trend
   - Topic mastery
   - Improvement rate

3. Engagement:
   - Daily/weekly activity
   - Streak tracking
   - Session duration

4. Achievements:
   - Badges earned
   - Milestones reached
   - Leaderboard position
```

## Accessibility Requirements

### WCAG 2.1 Compliance

```
Requirements:
- Keyboard navigation
- Screen reader support
- Sufficient color contrast
- Focus indicators
- Alt text for images
- Captions for videos
- Adjustable text size
```

### Responsive Design

```
Breakpoints:
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

Adapt:
- Navigation (hamburger menu on mobile)
- Chart sizes
- Data density
- Touch targets
```

## Quality Checklist

For dashboard implementation, verify:

- [ ] All progress data accurate and synced
- [ ] Visualizations render correctly
- [ ] Navigation is intuitive
- [ ] Settings are functional
- [ ] Accessibility standards met
- [ ] Responsive on all devices
- [ ] Real-time updates working
- [ ] Export features functional
- [ ] Admin features secured
- [ ] Performance optimized

---

## References

See `references/` for:
- Dashboard component library
- Visualization best practices
- Accessibility guidelines
- API endpoint specifications
- State management patterns
