"""File management utilities for QuizForge API."""

import json
from pathlib import Path
from typing import Any, Dict, List


def read_json_file(file_path: str | Path) -> Dict[str, Any] | List[Any]:
    """
    Read and parse a JSON file.
    
    Args:
        file_path: Path to the JSON file.
        
    Returns:
        Parsed JSON data.
        
    Raises:
        FileNotFoundError: If file doesn't exist.
        json.JSONDecodeError: If file contains invalid JSON.
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json_file(file_path: str | Path, data: Dict[str, Any] | List[Any], indent: int = 2) -> None:
    """
    Write data to a JSON file.
    
    Args:
        file_path: Path to the JSON file.
        data: Data to write.
        indent: JSON indentation level.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def validate_file_exists(file_path: str | Path) -> bool:
    """
    Check if a file exists.
    
    Args:
        file_path: Path to check.
        
    Returns:
        True if file exists, False otherwise.
    """
    return Path(file_path).exists()


def get_file_size(file_path: str | Path) -> int:
    """
    Get the size of a file in bytes.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        File size in bytes.
        
    Raises:
        FileNotFoundError: If file doesn't exist.
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    return path.stat().st_size

