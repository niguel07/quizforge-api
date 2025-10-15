"""Base routes for QuizForge API."""

from fastapi import APIRouter, HTTPException
from src.core.config import settings
from src.core.loader import QUESTIONS_DATA
from typing import Dict, Any

router = APIRouter()


@router.get("/health", tags=["System"])
def health() -> Dict[str, Any]:
    """
    Health check endpoint.
    
    Returns:
        Dictionary with system status information.
    """
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "data_loaded": len(QUESTIONS_DATA) > 0
    }


@router.get("/api/info", tags=["System"])
def info() -> Dict[str, Any]:
    """
    API information endpoint.
    
    Returns:
        Dictionary with API metadata and dataset information.
    """
    if not QUESTIONS_DATA:
        raise HTTPException(
            status_code=503,
            detail="Dataset not loaded. Please check server logs."
        )
    
    # Get unique categories and difficulties
    categories = set(q.get("category", "Unknown") for q in QUESTIONS_DATA)
    difficulties = set(q.get("difficulty", "Unknown") for q in QUESTIONS_DATA)
    
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "total_questions": len(QUESTIONS_DATA),
        "data_path": settings.DATA_PATH,
        "categories": sorted(list(categories)),
        "difficulty_levels": sorted(list(difficulties)),
        "endpoints": {
            "health": "/health",
            "api_info": "/api/info"
        }
    }

