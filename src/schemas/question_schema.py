"""Pydantic models for question data validation."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Dict


class QuestionOptions(BaseModel):
    """Model for question options (A, B, C, D)."""
    
    A: str
    B: str
    C: str
    D: str


class Question(BaseModel):
    """
    Question model representing a single quiz question.
    
    This schema validates the structure of questions loaded from the dataset.
    """
    
    id: int = Field(..., description="Unique question ID", ge=0)
    question: str = Field(..., description="The question text")
    options: QuestionOptions = Field(..., description="Answer options A-D")
    answer: str = Field(..., description="Correct answer (A, B, C, or D)")
    category: str = Field(..., description="Question category/topic")
    difficulty: str = Field(..., description="Difficulty level (Easy, Medium, Hard)")
    explanation: str = Field(..., description="Explanation of the correct answer")
    quality_score: float = Field(..., ge=0.0, le=1.0, description="Quality score (0-1)")
    source_topic: str = Field(..., description="Original source topic")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "question": "What is the capital of France?",
                "options": {
                    "A": "London",
                    "B": "Paris",
                    "C": "Berlin",
                    "D": "Madrid"
                },
                "answer": "B",
                "category": "Geography",
                "difficulty": "Easy",
                "explanation": "Paris is the capital and most populous city of France.",
                "quality_score": 1.0,
                "source_topic": "geography"
            }
        }
    )

