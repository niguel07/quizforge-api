"""Scoring and session tracking schemas for QuizForge API."""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class AnswerRecord(BaseModel):
    """Model for a single answer record."""
    
    question_id: int = Field(..., description="ID of the question answered")
    correct: bool = Field(..., description="Whether the answer was correct")
    timestamp: str = Field(..., description="ISO timestamp of when answer was recorded")


class UserSession(BaseModel):
    """Complete user session with all statistics."""
    
    username: str = Field(..., description="Username")
    answers: List[AnswerRecord] = Field(..., description="List of all answers")
    score: int = Field(..., description="Total correct answers", ge=0)
    accuracy: float = Field(..., description="Accuracy percentage (0-100)", ge=0.0, le=100.0)
    total_attempts: int = Field(..., description="Total questions attempted", ge=0)
    created_at: str = Field(..., description="ISO timestamp of session creation")
    last_updated: str = Field(..., description="ISO timestamp of last update")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "Niguel",
                "answers": [
                    {
                        "question_id": 1,
                        "correct": True,
                        "timestamp": "2025-10-15T12:00:00"
                    }
                ],
                "score": 8,
                "accuracy": 80.0,
                "total_attempts": 10,
                "created_at": "2025-10-15T10:00:00",
                "last_updated": "2025-10-15T12:00:00"
            }
        }
    )


class LeaderboardEntry(BaseModel):
    """Leaderboard entry showing user ranking."""
    
    username: str = Field(..., description="Username")
    score: int = Field(..., description="Total correct answers", ge=0)
    accuracy: float = Field(..., description="Accuracy percentage", ge=0.0, le=100.0)
    total_attempts: int = Field(..., description="Total attempts", ge=0)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "Niguel",
                "score": 45,
                "accuracy": 90.0,
                "total_attempts": 50
            }
        }
    )


class SubmitAnswerRequest(BaseModel):
    """Request model for submitting an answer."""
    
    username: str = Field(..., description="Username", min_length=1, max_length=50)
    question_id: int = Field(..., description="Question ID", ge=0)
    correct: bool = Field(..., description="Whether answer was correct")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "Niguel",
                "question_id": 1,
                "correct": True
            }
        }
    )


class LeaderboardResponse(BaseModel):
    """Response model for leaderboard."""
    
    total_users: int = Field(..., description="Total number of users", ge=0)
    leaderboard: List[LeaderboardEntry] = Field(..., description="Top users")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_users": 25,
                "leaderboard": [
                    {
                        "username": "Niguel",
                        "score": 45,
                        "accuracy": 90.0,
                        "total_attempts": 50
                    }
                ]
            }
        }
    )


class UsersListResponse(BaseModel):
    """Response model for all users list."""
    
    total_users: int = Field(..., description="Total number of users")
    usernames: List[str] = Field(..., description="List of all usernames")

