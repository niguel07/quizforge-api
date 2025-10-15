"""Scoring, session tracking, and leaderboard endpoints for QuizForge API."""

from fastapi import APIRouter, HTTPException, Query, Body
from src.utils import scorer
from src.schemas.scoring_schema import (
    UserSession,
    LeaderboardEntry,
    SubmitAnswerRequest,
    LeaderboardResponse,
    UsersListResponse
)
from typing import List

router = APIRouter(prefix="/api/score", tags=["Scoring"])


@router.post("/submit", response_model=UserSession, response_description="User session updated successfully")
def submit_answer(
    username: str = Query(..., min_length=1, max_length=50, description="Username"),
    question_id: int = Query(..., ge=0, description="Question ID"),
    correct: bool = Query(..., description="Whether the answer was correct")
) -> UserSession:
    """
    Submit an answer and update user statistics.
    
    Records a user's answer to a question and automatically updates:
    - Total score (increments if correct)
    - Accuracy percentage
    - Total attempts counter
    - Answer history
    
    Args:
        username: User's username (1-50 characters)
        question_id: ID of the question answered
        correct: Whether the answer was correct
        
    Returns:
        Updated user session with all statistics.
        
    Raises:
        HTTPException: If username is invalid.
    """
    if not username.strip():
        raise HTTPException(
            status_code=400,
            detail="Username cannot be empty"
        )
    
    try:
        result = scorer.record_answer(username, question_id, correct)
        return UserSession(**result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to record answer: {str(e)}"
        )


@router.get("/{username}", response_model=UserSession, response_description="User session retrieved successfully")
def get_user_score(username: str) -> UserSession:
    """
    Retrieve a user's session statistics.
    
    Returns complete session data including:
    - Total score and accuracy
    - All answer history
    - Session timestamps
    
    Args:
        username: The username to look up.
        
    Returns:
        Complete user session data.
        
    Raises:
        HTTPException: If user not found.
    """
    user = scorer.get_user_score(username)
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User '{username}' not found. Submit at least one answer to create a session."
        )
    
    return UserSession(**user)


@router.get("/leaderboard/top", response_model=LeaderboardResponse, response_description="Leaderboard retrieved successfully")
def get_leaderboard(
    limit: int = Query(10, ge=1, le=50, description="Number of top users to return")
) -> LeaderboardResponse:
    """
    Get global leaderboard sorted by score and accuracy.
    
    Returns top users ranked by:
    1. Total score (primary)
    2. Accuracy percentage (tiebreaker)
    
    Args:
        limit: Maximum number of entries to return (1-50).
        
    Returns:
        Leaderboard with top users.
    """
    leaderboard_data = scorer.get_leaderboard(limit)
    
    leaderboard_entries = [
        LeaderboardEntry(
            username=entry["username"],
            score=entry["score"],
            accuracy=entry["accuracy"],
            total_attempts=entry["total_attempts"]
        )
        for entry in leaderboard_data
    ]
    
    all_users = scorer.get_all_users()
    
    return LeaderboardResponse(
        total_users=len(all_users),
        leaderboard=leaderboard_entries
    )


@router.delete("/{username}", response_description="User session deleted successfully")
def reset_user_session(username: str) -> dict:
    """
    Reset (delete) a user's session data.
    
    Permanently removes all session data for the specified user.
    
    Args:
        username: Username to reset.
        
    Returns:
        Success message.
        
    Raises:
        HTTPException: If user not found.
    """
    success = scorer.reset_user_session(username)
    
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"User '{username}' not found"
        )
    
    return {
        "message": f"Session for user '{username}' has been reset successfully",
        "username": username
    }


@router.get("/users/list", response_model=UsersListResponse, response_description="Users list retrieved successfully")
def get_all_users() -> UsersListResponse:
    """
    Get list of all users with sessions.
    
    Returns:
        List of all usernames with active sessions.
    """
    usernames = scorer.get_all_users()
    
    return UsersListResponse(
        total_users=len(usernames),
        usernames=sorted(usernames)
    )

