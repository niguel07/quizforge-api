"""Scoring and session tracking utilities for QuizForge API."""

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

SESSION_PATH = Path("data/sessions.json")


def _read_sessions() -> List[Dict[str, Any]]:
    """
    Read all user sessions from the JSON file.
    
    Returns:
        List of user session dictionaries.
    """
    if not SESSION_PATH.exists():
        SESSION_PATH.parent.mkdir(parents=True, exist_ok=True)
        _write_sessions([])
        return []
    
    try:
        with open(SESSION_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def _write_sessions(data: List[Dict[str, Any]]) -> None:
    """
    Write user sessions to the JSON file.
    
    Args:
        data: List of user session dictionaries to persist.
    """
    SESSION_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SESSION_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def record_answer(username: str, question_id: int, correct: bool) -> Dict[str, Any]:
    """
    Record a user's answer and update their session statistics.
    
    Args:
        username: The user's username.
        question_id: ID of the question answered.
        correct: Whether the answer was correct.
        
    Returns:
        Updated user session dictionary.
    """
    sessions = _read_sessions()
    
    # Find existing user session or create new one
    user_session = next(
        (s for s in sessions if s["username"] == username),
        None
    )
    
    if not user_session:
        user_session = {
            "username": username,
            "answers": [],
            "score": 0,
            "accuracy": 0.0,
            "total_attempts": 0,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
        sessions.append(user_session)
    
    # Update session statistics
    user_session["answers"].append({
        "question_id": question_id,
        "correct": correct,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    user_session["total_attempts"] += 1
    
    if correct:
        user_session["score"] += 1
    
    # Calculate accuracy
    user_session["accuracy"] = round(
        (user_session["score"] / user_session["total_attempts"]) * 100, 2
    )
    user_session["last_updated"] = datetime.now(timezone.utc).isoformat()
    
    _write_sessions(sessions)
    return user_session


def get_user_score(username: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user's session statistics.
    
    Args:
        username: The user's username.
        
    Returns:
        User session dictionary or None if not found.
    """
    sessions = _read_sessions()
    return next(
        (s for s in sessions if s["username"] == username),
        None
    )


def get_leaderboard(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get global leaderboard sorted by score.
    
    Args:
        limit: Maximum number of entries to return.
        
    Returns:
        List of top user sessions sorted by score (descending).
    """
    sessions = _read_sessions()
    sorted_sessions = sorted(
        sessions,
        key=lambda x: (x["score"], x["accuracy"]),
        reverse=True
    )
    return sorted_sessions[:limit]


def reset_user_session(username: str) -> bool:
    """
    Reset a user's session (delete their data).
    
    Args:
        username: The user's username.
        
    Returns:
        True if user was found and deleted, False otherwise.
    """
    sessions = _read_sessions()
    original_length = len(sessions)
    sessions = [s for s in sessions if s["username"] != username]
    
    if len(sessions) < original_length:
        _write_sessions(sessions)
        return True
    return False


def get_all_users() -> List[str]:
    """
    Get list of all usernames with sessions.
    
    Returns:
        List of usernames.
    """
    sessions = _read_sessions()
    return [s["username"] for s in sessions]

