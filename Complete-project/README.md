# Course Companion FTE 🚀

**An AI-Native Digital Full-Time Equivalent (FTE) Educational Tutor**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 Project Overview

Course Companion FTE is a sophisticated **Digital Full-Time Equivalent** tutor built for the Panaversity Agent Factory Hackathon IV. It leverages a **Dual-Frontend Architecture** (ChatGPT App + Standalone Web App) to deliver a seamless, 24/7 educational experience for AI Agent Development.

### 🧠 The Intelligence Evolution
The project follows the "Zero-Backend-LLM Default" principle, evolving through three distinct phases:

1.  **Phase 1 (Zero-Backend-LLM)**: A deterministic backend serving content and quizzes with 0.0 marginal LLM cost.
2.  **Phase 2 (Selective Hybrid Intelligence)**: Introduction of premium AI features (Adaptive Learning, Detailed Grading) powered by Cerebras API.
3.  **Phase 3 (Enterprise Web App)**: A full-scale Next.js dashboard integrating all features with a professional UI/UX.

---

## 🏗️ Technical Architecture

This project implements the **Agent Factory 8-Layer Architecture**:

*   **L3 (FastAPI)**: Robust HTTP interface & A2A communication.
*   **L4/L5 (Hybrid SDK)**: Selective backend reasoning using Cerebras (Llama 3.1 70B).
*   **L6 (Skills & MCP)**: 13+ specialized Agent Skills for socratic tutoring, conceptual explanation, and progress motivation.
*   **Dual Frontends**:
    *   **ChatGPT App**: Conversational UI with 800M+ user reach.
    *   **Dashboard (Next.js)**: Rich Visual Studio-like experience for deep learning.

---

## ✨ Premium Features (Hybrid Intelligence)

| Feature | Powered By | Description |
| :--- | :--- | :--- |
| **🗺️ Adaptive Path** | Cerebras LLM | Analyzes scores & progress to generate a personalized study roadmap. |
| **📝 AI Assessments** | Cerebras LLM | Grades free-form written answers with detailed conceptual feedback. |
| **📊 Cost Analytics** | Custom Service | Real-time tracking of AI token usage and costs per user. |
| **🎓 AI Mentor** | Agentic Skills | Socratic guidance that helps students think through problems. |

---

## 🚀 Quick Start

### 1. Prerequisites
*   Python 3.12+
*   Node.js 18+ & npm
*   PostgreSQL (Neon/Supabase)
*   Cerebras API Key (for Premium features)

### 2. Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -e .

# Environment Variables: Copy .env.example to .env and fill in:
# DATABASE_URL, CEREBRAS_API_KEY, R2_BUCKET, etc.

# Run migrations & seed data
alembic upgrade head
python -m seed.seed_chapters
python -m seed.seed_quizzes

# Start Server
uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install

# Environment Variables: Create .env.local
# NEXT_PUBLIC_API_URL="http://localhost:8000"

# Start App
npm run dev
```

---

## 🔒 Constitutional Compliance

The system is built on **Constitutional Principles** to ensure reliability and cost-efficiency:
*   **Principle VIII (Hybrid Selectivity)**: LLMs are used only for high-value premium features.
*   **Principle X (Cost Control)**: Comprehensive logging and token caps prevent runaway expenses.
*   **Principle XI (Quality Standards)**: AI outputs are grounded in course content to prevent hallucinations.

---

## 📚 Deliverables & Documentation

*   **Architecture Diagram**: [`docs/architecture-diagram.svg`](docs/architecture-diagram.svg)
*   **ChatGPT App Manifest**: [`chatgpt-app/openapi.yaml`](chatgpt-app/openapi.yaml)
*   **Cost Analysis**: [`docs/cost-analysis.md`](docs/cost-analysis.md)
*   **Agent Skills**: Documentation located in `/skills`

---

## 📄 License
MIT License - see [LICENSE](LICENSE) file for details.

Built for the **Panaversity Agent Factory Hackathon IV**. 🚀
