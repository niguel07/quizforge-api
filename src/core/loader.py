"""Dataset loader for QuizForge API."""

import json
from pathlib import Path
from typing import List, Dict, Any
from src.core.config import settings


def load_questions() -> List[Dict[str, Any]]:
    """
    Load questions from the JSON dataset.
    
    Returns:
        List of question dictionaries.
        
    Raises:
        FileNotFoundError: If the dataset file doesn't exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    path = Path(settings.DATA_PATH)
    
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. "
            f"Please ensure the questions.json file exists in the docs/ directory."
        )
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON in dataset file: {e.msg}",
            e.doc,
            e.pos
        )
    
    if not isinstance(data, list):
        raise ValueError("Dataset must be a JSON array of questions")
    
    print(f"✅ Loaded {len(data)} questions from {path}")
    return data


# Load data on module import for efficiency
try:
    QUESTIONS_DATA = load_questions()
except Exception as e:
    print(f"⚠️  Warning: Could not load questions data: {e}")
    QUESTIONS_DATA = []

