# Course Companion FTE - Web Frontend

## 🎨 Features Implemented

This is a comprehensive, production-ready web frontend for the Course Companion FTE with all 6 Phase 1 features:

### ✅ All 6 Phase 1 Features

| Feature | Implementation | Status |
|---------|----------------|--------|
| 1. Content Delivery | Chapter cards with rich metadata, markdown rendering | ✅ |
| 2. Navigation | Next/Prev chapter navigation, chapter sequencing | ✅ |
| 3. Grounded Q&A | Full-text search with result highlighting | ✅ |
| 4. Rule-Based Quizzes | Interactive quiz with instant feedback | ✅ |
| 5. Progress Tracking | Dashboard with stats, streaks, progress bars | ✅ |
| 6. Freemium Gate | Visual locked chapters, upgrade prompts | ✅ |

### 🎯 Additional Features

- **Responsive Design** - Works on desktop, tablet, and mobile
- **Modern UI** - Gradient backgrounds, smooth animations, card-based layout
- **Real-time Progress** - Auto-updates as you complete chapters
- **Quiz System** - Multiple choice with instant grading and explanations
- **Search** - Full-text search across all course content
- **User Tiers** - Visual badges for Free/Premium/Pro users

---

## 🚀 Quick Start

### Prerequisites

1. Backend server running on `http://127.0.0.1:8000`
2. Valid API key seeded in database

### Running the Frontend

**Option 1: Simple HTTP Server**
```bash
cd frontend
python -m http.server 3000
# Open http://localhost:3000
```

**Option 2: Live Server (VS Code)**
- Install "Live Server" extension
- Right-click `index.html`
- Select "Open with Live Server"

**Option 3: Direct File**
- Simply open `index.html` in your browser

---

## ⚙️ Configuration

Update the API configuration in `index.html`:

```javascript
const API_URL = "http://127.0.0.1:8000";
const API_KEY = "test_api_key_12345"; // Replace with your seeded API key
```

### Getting Your API Key

After running the seed script, use the test API key:
```bash
# Default test key
test_api_key_12345
```

Or create a user via the database:
```sql
INSERT INTO users (email, tier) VALUES ('you@example.com', 'premium');
-- Then get the generated api_key
```

---

## 📱 Sections

### 1. Chapters (📚)
- View all course chapters
- See difficulty level and read time
- Free vs Premium indicators
- Click to read chapter content

### 2. Progress (📊)
- Chapters completed counter
- Current and longest streak
- Overall progress percentage
- Last activity date

### 3. Quiz (📝)
- Select chapter from dropdown
- Answer multiple choice questions
- Instant feedback with explanations
- Score summary at the end

### 4. Search (🔍)
- Search across all content
- Keyword highlighting
- Quick navigation to chapters

---

## 🎨 UI Components

### Chapter Cards
- Visual chapter number badges
- Title and metadata
- Difficulty level indicator
- Read time estimate
- Free/Premium badge
- Locked state for premium content

### Progress Dashboard
- Statistics cards (completed, streak)
- Animated progress bar
- Percentage display
- Quick action buttons

### Quiz Interface
- Question cards
- Radio button options
- Selected state highlighting
- Submit button
- Results with score and explanations

### Search Results
- Chapter title
- Content excerpt
- Quick navigation button

---

## 🎯 User Flow

1. **First Visit**
   - User sees chapter list
   - Free chapters (1-3) are accessible
   - Premium chapters (4-5) show lock icon

2. **Reading a Chapter**
   - Click chapter card or "Read" button
   - Content loads in viewer
   - Progress auto-updates to "in_progress"

3. **Taking a Quiz**
   - Navigate to Quiz tab
   - Select chapter from dropdown
   - Answer questions
   - Submit for instant grading

4. **Tracking Progress**
   - Progress panel updates automatically
   - Streak tracked on chapter completion
   - Overall percentage calculated

---

## 📱 Responsive Design

### Desktop (1400px+)
- Two-column dashboard layout
- Full navigation bar
- Large content viewer

### Tablet (768px - 1400px)
- Single column layout
- Compact navigation
- Optimized content display

### Mobile (< 768px)
- Full-width cards
- Scrollable navigation
- Touch-friendly buttons

---

## 🎨 Design System

### Colors
```css
--primary: #2563eb (Blue)
--secondary: #10b981 (Green)
--warning: #f59e0b (Amber)
--danger: #ef4444 (Red)
--bg: #f8fafc (Light gray)
--surface: #ffffff (White)
```

### Typography
- Font: System font stack (SF Pro, Segoe UI, Roboto)
- Headings: Bold, clear hierarchy
- Body: 1rem, 1.8 line height

### Spacing
- Card padding: 1.5rem
- Section gap: 2rem
- Border radius: 8-12px

---

## 🔧 Customization

### Change Theme Colors
Edit CSS variables in `<style>` section:
```css
:root {
    --primary: #your-color;
    --secondary: #your-color;
}
```

### Add New Sections
1. Add nav button in `<nav class="nav">`
2. Add section in `<main class="main">`
3. Implement `showSection()` handler

### Modify API Endpoint
Update `API_URL` constant:
```javascript
const API_URL = "https://your-api.com";
```

---

## 🐛 Troubleshooting

### "Backend not running" error
```bash
cd backend
uv run uvicorn app.main:app --reload
```

### "Authentication failed" error
- Check API_KEY is correct
- Verify user exists in database
- Run seed script to create test user

### Chapters not loading
- Check backend is running
- Verify database is seeded
- Check browser console for errors

### Quiz not working
- Ensure chapter has quiz questions
- Check API endpoint `/quizzes/{id}`
- Verify API key has access

---

## 📊 Features Checklist

- [x] Chapter listing with metadata
- [x] Chapter content viewer
- [x] Markdown rendering
- [x] Progress tracking
- [x] Streak calculation
- [x] Quiz system
- [x] Search functionality
- [x] Freemium gate visuals
- [x] User tier badges
- [x] Responsive design
- [x] Loading states
- [x] Error handling
- [x] Navigation between sections

---

## 🚀 Next Steps (Optional Enhancements)

1. **Authentication UI** - Login/signup forms
2. **Premium Upgrade** - Payment integration
3. **Dark Mode** - Theme toggle
4. **Bookmarks** - Save favorite sections
5. **Notes** - Add personal annotations
6. **Social Sharing** - Share achievements
7. **Certificates** - Download completion certs
8. **Discussion** - Chapter comments

---

## 📄 License

MIT License - Part of Course Companion FTE project

---

**Built with ❤️ for Panaversity Agent Factory Hackathon IV**
