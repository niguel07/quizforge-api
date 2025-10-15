"""Tests for scoring and leaderboard endpoints."""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from pathlib import Path
import json

client = TestClient(app)

# Clean up sessions before/after tests
SESSION_FILE = Path("data/sessions.json")


@pytest.fixture(autouse=True)
def cleanup_sessions():
    """Clean up sessions file before and after each test."""
    if SESSION_FILE.exists():
        SESSION_FILE.write_text("[]")
    yield
    if SESSION_FILE.exists():
        SESSION_FILE.write_text("[]")


class TestSubmitAnswer:
    """Test answer submission endpoint."""
    
    def test_submit_first_answer_correct(self):
        """Test submitting first correct answer creates session."""
        response = client.post(
            "/api/score/submit",
            params={"username": "TestUser1", "question_id": 1, "correct": True}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["username"] == "TestUser1"
        assert data["score"] == 1
        assert data["total_attempts"] == 1
        assert data["accuracy"] == 100.0
        assert len(data["answers"]) == 1
    
    def test_submit_first_answer_incorrect(self):
        """Test submitting first incorrect answer."""
        response = client.post(
            "/api/score/submit",
            params={"username": "TestUser2", "question_id": 1, "correct": False}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["username"] == "TestUser2"
        assert data["score"] == 0
        assert data["total_attempts"] == 1
        assert data["accuracy"] == 0.0
    
    def test_submit_multiple_answers(self):
        """Test submitting multiple answers updates stats correctly."""
        username = "TestUser3"
        
        # Submit correct answer
        client.post("/api/score/submit", params={"username": username, "question_id": 1, "correct": True})
        
        # Submit incorrect answer
        client.post("/api/score/submit", params={"username": username, "question_id": 2, "correct": False})
        
        # Submit correct answer
        response = client.post("/api/score/submit", params={"username": username, "question_id": 3, "correct": True})
        
        assert response.status_code == 200
        data = response.json()
        assert data["score"] == 2
        assert data["total_attempts"] == 3
        assert data["accuracy"] == 66.67
    
    def test_submit_empty_username(self):
        """Test that empty username is rejected."""
        response = client.post(
            "/api/score/submit",
            params={"username": "   ", "question_id": 1, "correct": True}
        )
        assert response.status_code == 400
    
    def test_submit_answer_persistence(self):
        """Test that answers are persisted to file."""
        client.post("/api/score/submit", params={"username": "PersistTest", "question_id": 1, "correct": True})
        
        # Read file directly
        assert SESSION_FILE.exists()
        with open(SESSION_FILE, "r") as f:
            sessions = json.load(f)
        
        assert len(sessions) == 1
        assert sessions[0]["username"] == "PersistTest"


class TestGetUserScore:
    """Test retrieving user scores."""
    
    def test_get_existing_user(self):
        """Test retrieving an existing user's score."""
        # Create user session
        client.post("/api/score/submit", params={"username": "GetUser1", "question_id": 1, "correct": True})
        
        # Retrieve it
        response = client.get("/api/score/GetUser1")
        assert response.status_code == 200
        
        data = response.json()
        assert data["username"] == "GetUser1"
        assert "score" in data
        assert "accuracy" in data
    
    def test_get_nonexistent_user(self):
        """Test retrieving a non-existent user returns 404."""
        response = client.get("/api/score/NonExistentUser")
        assert response.status_code == 404
    
    def test_get_user_shows_all_answers(self):
        """Test that user endpoint shows complete answer history."""
        username = "HistoryUser"
        
        # Submit multiple answers
        client.post("/api/score/submit", params={"username": username, "question_id": 1, "correct": True})
        client.post("/api/score/submit", params={"username": username, "question_id": 2, "correct": False})
        client.post("/api/score/submit", params={"username": username, "question_id": 3, "correct": True})
        
        response = client.get(f"/api/score/{username}")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["answers"]) == 3
        assert all("question_id" in ans and "correct" in ans for ans in data["answers"])


class TestLeaderboard:
    """Test leaderboard endpoint."""
    
    def test_leaderboard_empty(self):
        """Test leaderboard when no users exist."""
        response = client.get("/api/score/leaderboard/top")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_users"] == 0
        assert data["leaderboard"] == []
    
    def test_leaderboard_single_user(self):
        """Test leaderboard with single user."""
        client.post("/api/score/submit", params={"username": "Leader1", "question_id": 1, "correct": True})
        
        response = client.get("/api/score/leaderboard/top")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_users"] == 1
        assert len(data["leaderboard"]) == 1
        assert data["leaderboard"][0]["username"] == "Leader1"
    
    def test_leaderboard_sorting(self):
        """Test that leaderboard is sorted by score."""
        # Create users with different scores
        for i in range(3):
            client.post("/api/score/submit", params={"username": f"User{i}", "question_id": 1, "correct": True})
        
        # Add more points to User1
        client.post("/api/score/submit", params={"username": "User1", "question_id": 2, "correct": True})
        client.post("/api/score/submit", params={"username": "User1", "question_id": 3, "correct": True})
        
        response = client.get("/api/score/leaderboard/top")
        assert response.status_code == 200
        
        data = response.json()
        leaderboard = data["leaderboard"]
        
        # User1 should be first with 3 points
        assert leaderboard[0]["username"] == "User1"
        assert leaderboard[0]["score"] == 3
    
    def test_leaderboard_limit(self):
        """Test leaderboard respects limit parameter."""
        # Create 5 users
        for i in range(5):
            client.post("/api/score/submit", params={"username": f"LimitUser{i}", "question_id": 1, "correct": True})
        
        # Request only top 3
        response = client.get("/api/score/leaderboard/top?limit=3")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["leaderboard"]) == 3
        assert data["total_users"] == 5
    
    def test_leaderboard_invalid_limit(self):
        """Test that invalid limit is rejected."""
        response = client.get("/api/score/leaderboard/top?limit=0")
        assert response.status_code == 422
        
        response = client.get("/api/score/leaderboard/top?limit=100")
        assert response.status_code == 422


class TestResetUserSession:
    """Test resetting user sessions."""
    
    def test_reset_existing_user(self):
        """Test resetting an existing user's session."""
        # Create user
        client.post("/api/score/submit", params={"username": "ResetUser", "question_id": 1, "correct": True})
        
        # Verify user exists
        assert client.get("/api/score/ResetUser").status_code == 200
        
        # Reset
        response = client.delete("/api/score/ResetUser")
        assert response.status_code == 200
        assert "message" in response.json()
        
        # Verify user is gone
        assert client.get("/api/score/ResetUser").status_code == 404
    
    def test_reset_nonexistent_user(self):
        """Test resetting non-existent user returns 404."""
        response = client.delete("/api/score/NonExistent")
        assert response.status_code == 404


class TestGetAllUsers:
    """Test get all users endpoint."""
    
    def test_get_users_empty(self):
        """Test getting users when none exist."""
        response = client.get("/api/score/users/list")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_users"] == 0
        assert data["usernames"] == []
    
    def test_get_users_multiple(self):
        """Test getting multiple users."""
        # Create users
        for i in range(3):
            client.post("/api/score/submit", params={"username": f"ListUser{i}", "question_id": 1, "correct": True})
        
        response = client.get("/api/score/users/list")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_users"] == 3
        assert len(data["usernames"]) == 3
        assert all(f"ListUser{i}" in data["usernames"] for i in range(3))
    
    def test_get_users_sorted(self):
        """Test that usernames are returned sorted."""
        # Create users in random order
        for username in ["Zebra", "Alpha", "Mike"]:
            client.post("/api/score/submit", params={"username": username, "question_id": 1, "correct": True})
        
        response = client.get("/api/score/users/list")
        data = response.json()
        
        usernames = data["usernames"]
        assert usernames == sorted(usernames)


class TestScoringIntegration:
    """Integration tests for scoring system."""
    
    def test_full_quiz_session(self):
        """Test complete quiz session workflow."""
        username = "IntegrationUser"
        
        # Simulate answering 5 questions
        results = [True, True, False, True, False]
        
        for idx, correct in enumerate(results):
            response = client.post(
                "/api/score/submit",
                params={"username": username, "question_id": idx, "correct": correct}
            )
            assert response.status_code == 200
        
        # Check final stats
        response = client.get(f"/api/score/{username}")
        data = response.json()
        
        assert data["score"] == 3  # 3 correct out of 5
        assert data["total_attempts"] == 5
        assert data["accuracy"] == 60.0
        assert len(data["answers"]) == 5
    
    def test_leaderboard_accuracy_tiebreaker(self):
        """Test that leaderboard uses accuracy as tiebreaker."""
        # User1: 2/2 = 100% accuracy
        client.post("/api/score/submit", params={"username": "AccUser1", "question_id": 1, "correct": True})
        client.post("/api/score/submit", params={"username": "AccUser1", "question_id": 2, "correct": True})
        
        # User2: 2/3 = 66.67% accuracy
        client.post("/api/score/submit", params={"username": "AccUser2", "question_id": 1, "correct": True})
        client.post("/api/score/submit", params={"username": "AccUser2", "question_id": 2, "correct": True})
        client.post("/api/score/submit", params={"username": "AccUser2", "question_id": 3, "correct": False})
        
        response = client.get("/api/score/leaderboard/top")
        leaderboard = response.json()["leaderboard"]
        
        # Both have score 2, but AccUser1 should rank higher due to better accuracy
        assert leaderboard[0]["username"] == "AccUser1"
        assert leaderboard[0]["accuracy"] == 100.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

