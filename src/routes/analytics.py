"""Analytics and insights endpoints for QuizForge API."""

from fastapi import APIRouter, HTTPException
from src.core.loader import QUESTIONS_DATA
from src.utils import analyzer
from src.schemas.analytics_schema import (
    StatsResponse,
    CountResponse,
    CategoriesResponse,
    DifficultiesResponse,
    TopicsResponse,
    SummaryResponse,
    CategoryStatsResponse,
    DifficultyStatsResponse,
    CategoryStatDetail,
    DifficultyStatDetail
)

router = APIRouter(prefix="/api", tags=["Analytics"])


@router.get("/stats", response_model=StatsResponse)
def get_stats() -> StatsResponse:
    """
    Get comprehensive dataset statistics.
    
    Returns detailed analytics including:
    - Total question count
    - Category distribution
    - Difficulty distribution
    - Topic list
    - Quality score statistics
    - Unique counts
    
    Returns:
        Complete dataset statistics.
    """
    if not QUESTIONS_DATA:
        raise HTTPException(
            status_code=503,
            detail="Dataset not loaded. Please check server configuration."
        )
    
    summary = analyzer.get_dataset_summary(QUESTIONS_DATA)
    return StatsResponse(**summary)


@router.get("/categories", response_model=CategoriesResponse)
def get_categories() -> CategoriesResponse:
    """
    Get list of all unique categories in the dataset.
    
    Returns:
        List of category names sorted alphabetically.
    """
    if not QUESTIONS_DATA:
        raise HTTPException(
            status_code=503,
            detail="Dataset not loaded."
        )
    
    categories = analyzer.get_unique_categories(QUESTIONS_DATA)
    return CategoriesResponse(
        count=len(categories),
        categories=categories
    )


@router.get("/difficulty", response_model=DifficultiesResponse)
def get_difficulties() -> DifficultiesResponse:
    """
    Get list of all difficulty levels in the dataset.
    
    Returns:
        List of difficulty levels (Easy, Medium, Hard).
    """
    if not QUESTIONS_DATA:
        raise HTTPException(
            status_code=503,
            detail="Dataset not loaded."
        )
    
    difficulties = analyzer.get_unique_difficulties(QUESTIONS_DATA)
    return DifficultiesResponse(
        count=len(difficulties),
        difficulty_levels=difficulties
    )


@router.get("/topics", response_model=TopicsResponse)
def get_topics() -> TopicsResponse:
    """
    Get list of all unique topics in the dataset.
    
    Returns:
        List of topic names sorted alphabetically.
    """
    if not QUESTIONS_DATA:
        raise HTTPException(
            status_code=503,
            detail="Dataset not loaded."
        )
    
    topics = analyzer.get_topic_list(QUESTIONS_DATA)
    return TopicsResponse(
        count=len(topics),
        topics=topics
    )


@router.get("/count", response_model=CountResponse)
def get_total_questions() -> CountResponse:
    """
    Get total number of questions in the dataset.
    
    Returns:
        Total question count.
    """
    return CountResponse(total_questions=len(QUESTIONS_DATA))


@router.get("/summary", response_model=SummaryResponse)
def get_summary() -> SummaryResponse:
    """
    Get compact summary of all metadata in one response.
    
    This endpoint combines all analytics data for efficient 
    single-request retrieval.
    
    Returns:
        Complete dataset summary with all statistics.
    """
    if not QUESTIONS_DATA:
        raise HTTPException(
            status_code=503,
            detail="Dataset not loaded."
        )
    
    summary = analyzer.get_dataset_summary(QUESTIONS_DATA)
    return SummaryResponse(summary=summary)


@router.get("/categories/stats", response_model=CategoryStatsResponse)
def get_category_stats() -> CategoryStatsResponse:
    """
    Get detailed statistics for each category.
    
    Returns category-wise breakdown including:
    - Question count per category
    - Percentage of total questions
    - Difficulty distribution within each category
    
    Returns:
        Detailed category statistics.
    """
    if not QUESTIONS_DATA:
        raise HTTPException(
            status_code=503,
            detail="Dataset not loaded."
        )
    
    stats_list = analyzer.get_category_stats(QUESTIONS_DATA)
    
    # Convert to Pydantic models
    category_stats = [CategoryStatDetail(**stat) for stat in stats_list]
    
    return CategoryStatsResponse(
        total_categories=len(category_stats),
        stats=category_stats
    )


@router.get("/difficulty/stats", response_model=DifficultyStatsResponse)
def get_difficulty_stats() -> DifficultyStatsResponse:
    """
    Get detailed statistics for each difficulty level.
    
    Returns difficulty-wise breakdown including:
    - Question count per level
    - Percentage of total questions
    
    Returns:
        Detailed difficulty statistics.
    """
    if not QUESTIONS_DATA:
        raise HTTPException(
            status_code=503,
            detail="Dataset not loaded."
        )
    
    stats_list = analyzer.get_difficulty_stats(QUESTIONS_DATA)
    
    # Convert to Pydantic models
    difficulty_stats = [DifficultyStatDetail(**stat) for stat in stats_list]
    
    return DifficultyStatsResponse(
        total_levels=len(difficulty_stats),
        stats=difficulty_stats
    )

