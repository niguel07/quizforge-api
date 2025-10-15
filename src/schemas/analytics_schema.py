"""Analytics response schemas for QuizForge API."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Any


class StatsResponse(BaseModel):
    """Comprehensive dataset statistics response."""
    
    total_questions: int = Field(..., description="Total number of questions in dataset")
    categories: Dict[str, int] = Field(..., description="Distribution of questions by category")
    difficulty: Dict[str, int] = Field(..., description="Distribution of questions by difficulty")
    topics: List[str] = Field(..., description="List of unique topics")
    quality_stats: Dict[str, float] = Field(..., description="Quality score statistics")
    unique_counts: Dict[str, int] = Field(..., description="Count of unique values")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_questions": 99,
                "categories": {
                    "Colonial History": 15,
                    "African History": 12,
                    "Geography": 8
                },
                "difficulty": {
                    "Easy": 30,
                    "Medium": 45,
                    "Hard": 24
                },
                "topics": ["history", "geography", "science"],
                "quality_stats": {
                    "min": 0.8,
                    "max": 1.0,
                    "average": 0.95
                },
                "unique_counts": {
                    "categories": 48,
                    "difficulties": 3,
                    "topics": 5
                }
            }
        }
    )


class CountResponse(BaseModel):
    """Simple question count response."""
    
    total_questions: int = Field(..., description="Total number of questions", ge=0)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_questions": 99
            }
        }
    )


class CategoriesResponse(BaseModel):
    """Categories list response."""
    
    count: int = Field(..., description="Number of unique categories")
    categories: List[str] = Field(..., description="List of category names")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "count": 48,
                "categories": ["African History", "Ancient History", "Colonial History"]
            }
        }
    )


class DifficultiesResponse(BaseModel):
    """Difficulty levels response."""
    
    count: int = Field(..., description="Number of difficulty levels")
    difficulty_levels: List[str] = Field(..., description="List of difficulty levels")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "count": 3,
                "difficulty_levels": ["Easy", "Medium", "Hard"]
            }
        }
    )


class TopicsResponse(BaseModel):
    """Topics list response."""
    
    count: int = Field(..., description="Number of unique topics")
    topics: List[str] = Field(..., description="List of topic names")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "count": 5,
                "topics": ["history", "geography", "science"]
            }
        }
    )


class CategoryStatDetail(BaseModel):
    """Detailed statistics for a single category."""
    
    category: str = Field(..., description="Category name")
    count: int = Field(..., description="Number of questions in category")
    percentage: float = Field(..., description="Percentage of total questions")
    difficulty_breakdown: Dict[str, int] = Field(..., description="Question count by difficulty")


class DifficultyStatDetail(BaseModel):
    """Detailed statistics for a single difficulty level."""
    
    level: str = Field(..., description="Difficulty level")
    count: int = Field(..., description="Number of questions at this level")
    percentage: float = Field(..., description="Percentage of total questions")


class CategoryStatsResponse(BaseModel):
    """Detailed category statistics response."""
    
    total_categories: int = Field(..., description="Total number of categories")
    stats: List[CategoryStatDetail] = Field(..., description="Detailed stats per category")


class DifficultyStatsResponse(BaseModel):
    """Detailed difficulty statistics response."""
    
    total_levels: int = Field(..., description="Total number of difficulty levels")
    stats: List[DifficultyStatDetail] = Field(..., description="Detailed stats per difficulty")


class SummaryResponse(BaseModel):
    """Compact summary of all metadata."""
    
    summary: Dict[str, Any] = Field(..., description="Complete dataset summary")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "summary": {
                    "total_questions": 99,
                    "categories": {"History": 50, "Geography": 30},
                    "difficulty": {"Easy": 30, "Medium": 45, "Hard": 24},
                    "topics": ["history", "geography"],
                    "quality_stats": {"min": 0.8, "max": 1.0, "average": 0.95}
                }
            }
        }
    )

