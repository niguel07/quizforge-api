"""Pagination utilities for QuizForge API."""

from typing import List, Any, Dict
from math import ceil


def paginate(
    data: List[Any],
    page: int = 1,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Paginate a list of items.
    
    Args:
        data: List of items to paginate.
        page: Page number (1-indexed).
        limit: Number of items per page.
        
    Returns:
        Dictionary with pagination metadata and items.
    """
    total_items = len(data)
    total_pages = ceil(total_items / limit) if limit > 0 else 0
    
    # Ensure page is within valid range
    page = max(1, min(page, total_pages if total_pages > 0 else 1))
    
    start = (page - 1) * limit
    end = start + limit
    
    return {
        "items": data[start:end],
        "pagination": {
            "page": page,
            "limit": limit,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        }
    }


def get_slice(data: List[Any], start: int, end: int) -> List[Any]:
    """
    Get a slice of data with bounds checking.
    
    Args:
        data: List to slice.
        start: Start index.
        end: End index.
        
    Returns:
        Sliced list.
    """
    return data[max(0, start):min(len(data), end)]

