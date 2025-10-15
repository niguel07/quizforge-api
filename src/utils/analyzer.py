"""Analytics and aggregation utilities for QuizForge API."""

from collections import Counter
from typing import List, Dict, Any


def get_category_distribution(data: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Get distribution of questions across categories.
    
    Args:
        data: List of question dictionaries.
        
    Returns:
        Dictionary mapping category names to question counts.
    """
    if not data:
        return {}
    
    categories = [q.get("category", "Unknown") for q in data if q.get("category")]
    return dict(Counter(categories))


def get_difficulty_distribution(data: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Get distribution of questions across difficulty levels.
    
    Args:
        data: List of question dictionaries.
        
    Returns:
        Dictionary mapping difficulty levels to question counts.
    """
    if not data:
        return {}
    
    difficulties = [q.get("difficulty", "Unknown") for q in data if q.get("difficulty")]
    return dict(Counter(difficulties))


def get_topic_list(data: List[Dict[str, Any]]) -> List[str]:
    """
    Get sorted list of unique topics from the dataset.
    
    Args:
        data: List of question dictionaries.
        
    Returns:
        Sorted list of unique topic names.
    """
    if not data:
        return []
    
    topics = set(q.get("source_topic", "unknown") for q in data if q.get("source_topic"))
    return sorted(list(topics))


def get_unique_categories(data: List[Dict[str, Any]]) -> List[str]:
    """
    Get sorted list of unique categories.
    
    Args:
        data: List of question dictionaries.
        
    Returns:
        Sorted list of unique category names.
    """
    if not data:
        return []
    
    categories = set(q.get("category", "Unknown") for q in data if q.get("category"))
    return sorted(list(categories))


def get_unique_difficulties(data: List[Dict[str, Any]]) -> List[str]:
    """
    Get sorted list of unique difficulty levels.
    
    Args:
        data: List of question dictionaries.
        
    Returns:
        Sorted list of difficulty levels.
    """
    if not data:
        return []
    
    difficulties = set(q.get("difficulty", "Unknown") for q in data if q.get("difficulty"))
    return sorted(list(difficulties))


def get_quality_stats(data: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Calculate quality score statistics.
    
    Args:
        data: List of question dictionaries.
        
    Returns:
        Dictionary with min, max, and average quality scores.
    """
    if not data:
        return {"min": 0.0, "max": 0.0, "average": 0.0}
    
    scores = [q.get("quality_score", 0.0) for q in data if "quality_score" in q]
    
    if not scores:
        return {"min": 0.0, "max": 0.0, "average": 0.0}
    
    return {
        "min": round(min(scores), 2),
        "max": round(max(scores), 2),
        "average": round(sum(scores) / len(scores), 2)
    }


def get_dataset_summary(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate comprehensive dataset summary with all analytics.
    
    Args:
        data: List of question dictionaries.
        
    Returns:
        Dictionary containing complete dataset statistics.
    """
    return {
        "total_questions": len(data),
        "categories": get_category_distribution(data),
        "difficulty": get_difficulty_distribution(data),
        "topics": get_topic_list(data),
        "quality_stats": get_quality_stats(data),
        "unique_counts": {
            "categories": len(get_unique_categories(data)),
            "difficulties": len(get_unique_difficulties(data)),
            "topics": len(get_topic_list(data))
        }
    }


def get_category_stats(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Get detailed statistics for each category.
    
    Args:
        data: List of question dictionaries.
        
    Returns:
        List of dictionaries with category statistics.
    """
    if not data:
        return []
    
    category_dist = get_category_distribution(data)
    total_questions = len(data)
    
    stats = []
    for category, count in sorted(category_dist.items(), key=lambda x: x[1], reverse=True):
        # Get questions for this category
        cat_questions = [q for q in data if q.get("category") == category]
        
        # Calculate difficulty breakdown
        difficulty_breakdown = {}
        for q in cat_questions:
            diff = q.get("difficulty", "Unknown")
            difficulty_breakdown[diff] = difficulty_breakdown.get(diff, 0) + 1
        
        stats.append({
            "category": category,
            "count": count,
            "percentage": round((count / total_questions) * 100, 2),
            "difficulty_breakdown": difficulty_breakdown
        })
    
    return stats


def get_difficulty_stats(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Get detailed statistics for each difficulty level.
    
    Args:
        data: List of question dictionaries.
        
    Returns:
        List of dictionaries with difficulty statistics.
    """
    if not data:
        return []
    
    difficulty_dist = get_difficulty_distribution(data)
    total_questions = len(data)
    
    # Define standard order
    order = {"Easy": 1, "Medium": 2, "Hard": 3}
    
    stats = []
    for difficulty, count in sorted(difficulty_dist.items(), key=lambda x: order.get(x[0], 999)):
        stats.append({
            "level": difficulty,
            "count": count,
            "percentage": round((count / total_questions) * 100, 2)
        })
    
    return stats

