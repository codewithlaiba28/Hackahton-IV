# PHASE 1 COMPLIANCE: This file MUST NOT import or call any LLM API.
# Forbidden: openai, anthropic, langchain, llama_index, cohere, groq
# This is a Zero-Backend-LLM architecture. Violation = disqualification.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import init_db, close_db
from app.routers import chapters, quizzes, progress, access, users, search, auth

# Phase 2: Hybrid Intelligence Routers (isolated from Phase 1)
from app.routers import adaptive_path, assessments

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


# Create FastAPI application
app = FastAPI(
    title="Course Companion FTE",
    description="Zero-Backend-LLM Educational Tutor API",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
# In development, allow all origins for testing. In production, restrict to ChatGPT.
if settings.APP_ENV == "development":
    allow_origins = ["*"]
else:
    allow_origins = [settings.CHATGPT_APP_ORIGIN]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint (no auth required)
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "environment": settings.APP_ENV}


# Include routers
app.include_router(auth.router, tags=["Phase 3: Authentication"])
app.include_router(chapters.router, prefix="/chapters", tags=["Chapters"])
app.include_router(quizzes.router, prefix="/quizzes", tags=["Quizzes"])
app.include_router(progress.router, prefix="/progress", tags=["Progress"])
app.include_router(access.router, prefix="/access", tags=["Access"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(search.router, prefix="/search", tags=["Search"])

# Phase 2: Hybrid Intelligence Routers
app.include_router(adaptive_path.router, tags=["Phase 2: Adaptive Learning"])
app.include_router(assessments.router, tags=["Phase 2: Assessments"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.is_development,
    )
