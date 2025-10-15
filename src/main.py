"""Main FastAPI application entrypoint for QuizForge API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import base, questions, analytics, scoring
from src.core.config import settings

# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A production-grade quiz management API built with FastAPI",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(base.router)
app.include_router(questions.router)
app.include_router(analytics.router)
app.include_router(scoring.router)


@app.get("/", tags=["Root"])
def root():
    """Root endpoint - API welcome message."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health",
        "info": "/api/info"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True
    )

