"""Question endpoints for QuizForge API."""

from fastapi import APIRouter, Query, HTTPException, Path as PathParam
from typing import List, Optional
from src.core.loader import QUESTIONS_DATA
from src.schemas.question_schema import Question
from src.schemas.response_schema import (
    AnswerValidationRequest,
    AnswerValidationResponse,
    CategoryListResponse,
    DifficultyListResponse
)
from src.utils.randomizer import random_sample
from src.utils.pagination import paginate

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get("/random", response_model=List[Question])
def get_random_questions(
    count: int = Query(10, ge=1, le=100, description="Number of random questions to return")
) -> List[Question]:
    """
    Get random questions from the dataset.
    
    Args:
        count: Number of questions to return (1-100).
        
    Returns:
        List of random questions.
        
    Raises:
        HTTPException: If no questions are available.
    """
    if len(QUESTIONS_DATA) == 0:
        raise HTTPException(
            status_code=503,
            detail="No questions available. Please check server configuration."
        )
    
    questions = random_sample(QUESTIONS_DATA, count)
    return questions


@router.get("/category/{category}", response_model=List[Question])
def get_by_category(
    category: str = PathParam(..., description="Category name"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of questions to return")
) -> List[Question]:
    """
    Get questions filtered by category.
    
    Args:
        category: Category name (case-insensitive).
        limit: Maximum number of questions to return.
        
    Returns:
        List of questions in the specified category.
        
    Raises:
        HTTPException: If no questions found for the category.
    """
    # Case-insensitive category search
    results = [
        q for q in QUESTIONS_DATA
        if q.get("category", "").lower() == category.lower()
    ]
    
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"No questions found for category '{category}'. Use /api/categories to see available categories."
        )
    
    return results[:limit]


@router.get("/difficulty/{level}", response_model=List[Question])
def get_by_difficulty(
    level: str = PathParam(..., description="Difficulty level (Easy, Medium, Hard)"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of questions to return")
) -> List[Question]:
    """
    Get questions filtered by difficulty level.
    
    Args:
        level: Difficulty level (case-insensitive: Easy, Medium, Hard).
        limit: Maximum number of questions to return.
        
    Returns:
        List of questions at the specified difficulty.
        
    Raises:
        HTTPException: If no questions found for the difficulty level.
    """
    # Case-insensitive difficulty search
    results = [
        q for q in QUESTIONS_DATA
        if q.get("difficulty", "").lower() == level.lower()
    ]
    
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"No questions found for difficulty '{level}'. Valid levels: Easy, Medium, Hard."
        )
    
    return results[:limit]


@router.get("/search", response_model=List[Question])
def search_questions(
    q: str = Query(..., min_length=2, description="Search query (minimum 2 characters)"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty")
) -> List[Question]:
    """
    Search questions by keyword in question text.
    
    Args:
        q: Search query (case-insensitive).
        limit: Maximum number of results.
        category: Optional category filter.
        difficulty: Optional difficulty filter.
        
    Returns:
        List of matching questions.
        
    Raises:
        HTTPException: If no results found.
    """
    search_term = q.lower()
    
    # Filter by search term
    results = [
        item for item in QUESTIONS_DATA
        if search_term in item.get("question", "").lower()
    ]
    
    # Apply optional category filter
    if category:
        results = [
            q for q in results
            if q.get("category", "").lower() == category.lower()
        ]
    
    # Apply optional difficulty filter
    if difficulty:
        results = [
            q for q in results
            if q.get("difficulty", "").lower() == difficulty.lower()
        ]
    
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"No results found for search term '{q}' with the given filters."
        )
    
    return results[:limit]


@router.post("/answer", response_model=AnswerValidationResponse)
def validate_answer(payload: AnswerValidationRequest) -> AnswerValidationResponse:
    """
    Validate a learner's answer to a question.
    
    Args:
        payload: Answer validation request containing question_id and selected_answer.
        
    Returns:
        Answer validation response with correctness and explanation.
        
    Raises:
        HTTPException: If question not found or invalid data.
    """
    question_id = payload.question_id
    selected = payload.selected_answer.strip().upper()
    
    # Validate answer format
    if selected not in ["A", "B", "C", "D"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid answer format. Must be A, B, C, or D."
        )
    
    # Find the question
    question = next(
        (q for q in QUESTIONS_DATA if q.get("id") == question_id),
        None
    )
    
    if not question:
        raise HTTPException(
            status_code=404,
            detail=f"Question with ID {question_id} not found."
        )
    
    # Check if answer is correct
    correct_answer = question.get("answer", "").strip().upper()
    is_correct = selected == correct_answer
    
    return AnswerValidationResponse(
        question_id=question_id,
        correct=is_correct,
        correct_answer=correct_answer,
        selected_answer=selected,
        explanation=question.get("explanation", "No explanation available.")
    )


@router.get("/categories", response_model=CategoryListResponse)
def get_categories() -> CategoryListResponse:
    """
    Get list of all available question categories.
    
    Returns:
        List of unique categories.
    """
    categories = sorted(set(
        q.get("category", "Unknown")
        for q in QUESTIONS_DATA
        if q.get("category")
    ))
    
    return CategoryListResponse(
        count=len(categories),
        categories=categories
    )


@router.get("/difficulties", response_model=DifficultyListResponse)
def get_difficulty_levels() -> DifficultyListResponse:
    """
    Get list of all available difficulty levels.
    
    Returns:
        List of difficulty levels.
    """
    levels = sorted(set(
        q.get("difficulty", "Unknown")
        for q in QUESTIONS_DATA
        if q.get("difficulty")
    ))
    
    return DifficultyListResponse(
        count=len(levels),
        levels=levels
    )


@router.get("/{question_id}", response_model=Question)
def get_question_by_id(
    question_id: int = PathParam(..., ge=0, description="Question ID")
) -> Question:
    """
    Get a specific question by its ID.
    
    Args:
        question_id: The question ID.
        
    Returns:
        The question object.
        
    Raises:
        HTTPException: If question not found.
    """
    question = next(
        (q for q in QUESTIONS_DATA if q.get("id") == question_id),
        None
    )
    
    if not question:
        raise HTTPException(
            status_code=404,
            detail=f"Question with ID {question_id} not found."
        )
    
    return question


@router.get("/", response_model=List[Question])
def get_all_questions(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page")
) -> List[Question]:
    """
    Get paginated list of all questions.
    
    Args:
        page: Page number (1-indexed).
        limit: Number of items per page.
        
    Returns:
        Paginated list of questions.
    """
    result = paginate(QUESTIONS_DATA, page, limit)
    return result["items"]

