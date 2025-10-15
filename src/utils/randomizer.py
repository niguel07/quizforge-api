"""Randomization utilities for QuizForge API."""

import random
from typing import List, Any


def random_sample(data: List[Any], count: int) -> List[Any]:
    """
    Get a random sample of items from a list.
    
    Args:
        data: List of items to sample from.
        count: Number of items to return.
        
    Returns:
        List of randomly selected items.
    """
    if not data:
        return []
    
    # Use random.sample for better performance on large datasets
    sample_size = min(count, len(data))
    return random.sample(data, sample_size)


def shuffle_list(data: List[Any]) -> List[Any]:
    """
    Shuffle a list and return a copy.
    
    Args:
        data: List to shuffle.
        
    Returns:
        Shuffled copy of the list.
    """
    shuffled = data.copy()
    random.shuffle(shuffled)
    return shuffled

