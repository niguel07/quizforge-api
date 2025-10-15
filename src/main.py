"""Main FastAPI application entrypoint for QuizForge API - v1.0.0"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import base, questions, analytics, scoring
from src.core.config import settings
from src.core.error_handler import register_exception_handlers

# Initialize FastAPI application with metadata
app = FastAPI(
    title="QuizForge API",
    description="""
    **QuizForge API** is a production-grade RESTful backend for educational quiz platforms.
    
    ## Features
    
    * **Question Management**: Browse, search, and filter questions
    * **Analytics & Insights**: Comprehensive dataset statistics
    * **User Scoring**: Track user performance and accuracy
    * **Leaderboard**: Global rankings and competition
    * **Random Quizzes**: Generate random question sets
    
    ## Base URL
    
    All API endpoints are versioned under `/api/v1/`
    
    ## Authentication
    
    Currently no authentication required (v1.0.0)
    """,
    version="1.0.0",
    contact={
        "name": "BIGOUAWE Effoudou Niguel Clark",
        "url": "https://github.com/niguel07/quizforge-api",
        "email": "contact@niguelclark.dev"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=[
        {
            "name": "Root",
            "description": "API root and version information"
        },
        {
            "name": "System",
            "description": "Health checks and system information"
        },
        {
            "name": "Questions",
            "description": "Browse, search, and filter quiz questions"
        },
        {
            "name": "Analytics",
            "description": "Dataset statistics and insights"
        },
        {
            "name": "Scoring",
            "description": "User scoring, sessions, and leaderboard"
        }
    ],
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register global error handlers
register_exception_handlers(app)

# Include routers with /api/v1 prefix
app.include_router(base.router, prefix="/api/v1")
app.include_router(questions.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(scoring.router, prefix="/api/v1")


@app.get("/", tags=["Root"], summary="API Root")
def root():
    """
    API root endpoint with version information and quick links.
    
    Returns basic API metadata and navigation links.
    """
    return {
        "name": "QuizForge API",
        "version": "1.0.0",
        "description": "Production-grade quiz management API",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_schema": "/openapi.json"
        },
        "endpoints": {
            "health": "/api/v1/health",
            "questions": "/api/v1/questions",
            "analytics": "/api/v1/stats",
            "leaderboard": "/api/v1/score/leaderboard/top"
        },
        "github": "https://github.com/niguel07/quizforge-api"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True
    )
