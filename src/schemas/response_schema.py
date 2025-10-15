"""Response schemas for QuizForge API."""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any, Dict
from src.schemas.question_schema import Question


class QuestionResponse(BaseModel):
    """Response model for question lists."""
    
    count: int = Field(..., description="Number of questions returned")
    questions: List[Question] = Field(..., description="List of questions")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "count": 10,
                "questions": [
                    {
                        "question": "What is the capital of France?",
                        "options": {"A": "London", "B": "Paris", "C": "Berlin", "D": "Madrid"},
                        "answer": "B",
                        "category": "Geography",
                        "difficulty": "Easy",
                        "explanation": "Paris is the capital of France.",
                        "quality_score": 1.0,
                        "source_topic": "geography"
                    }
                ]
            }
        }
    )


class AnswerValidationRequest(BaseModel):
    """Request model for answer validation."""
    
    question_id: int = Field(..., description="ID of the question being answered", ge=0)
    selected_answer: str = Field(..., description="Selected answer (A, B, C, or D)", min_length=1, max_length=1)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question_id": 1,
                "selected_answer": "B"
            }
        }
    )


class AnswerValidationResponse(BaseModel):
    """Response model for answer validation."""
    
    question_id: int = Field(..., description="ID of the question")
    correct: bool = Field(..., description="Whether the answer was correct")
    correct_answer: str = Field(..., description="The correct answer")
    selected_answer: str = Field(..., description="The answer that was selected")
    explanation: str = Field(..., description="Explanation of the correct answer")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question_id": 1,
                "correct": True,
                "correct_answer": "B",
                "selected_answer": "B",
                "explanation": "Paris is the capital and most populous city of France."
            }
        }
    )


class CategoryListResponse(BaseModel):
    """Response model for category list."""
    
    count: int = Field(..., description="Number of categories")
    categories: List[str] = Field(..., description="List of unique categories")


class DifficultyListResponse(BaseModel):
    """Response model for difficulty levels list."""
    
    count: int = Field(..., description="Number of difficulty levels")
    levels: List[str] = Field(..., description="List of difficulty levels")

