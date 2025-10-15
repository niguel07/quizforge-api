"""Integration tests for QuizForge API."""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from pathlib import Path

client = TestClient(app)

# Clean up sessions for scoring tests
SESSION_FILE = Path("data/sessions.json")


@pytest.fixture(autouse=True)
def cleanup_sessions():
    """Clean up sessions file before each test."""
    if SESSION_FILE.exists():
        SESSION_FILE.write_text("[]")
    yield


class TestAPIVersioning:
    """Test API versioning structure."""
    
    def test_root_endpoint(self):
        """Test root endpoint provides API information."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "version" in data
        assert data["version"] == "1.0.0"
        assert "endpoints" in data
    
    def test_versioned_health_endpoint(self):
        """Test health endpoint under /api/v1."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
    
    def test_old_health_endpoint_not_found(self):
        """Test that non-versioned endpoints don't exist."""
        response = client.get("/health")
        assert response.status_code == 404


class TestEndToEndWorkflow:
    """Test complete end-to-end workflows."""
    
    def test_complete_quiz_workflow(self):
        """Test full quiz taking workflow."""
        username = "E2EUser"
        
        # Step 1: Get random questions
        response = client.get("/api/v1/questions/random?count=3")
        assert response.status_code == 200
        questions = response.json()
        assert len(questions) <= 3
        
        # Step 2: Answer questions and record scores
        for question in questions:
            # Simulate correct answer
            response = client.post(
                "/api/v1/score/submit",
                params={
                    "username": username,
                    "question_id": question["id"],
                    "correct": True
                }
            )
            assert response.status_code == 200
        
        # Step 3: Check user score
        response = client.get(f"/api/v1/score/{username}")
        assert response.status_code == 200
        
        user_data = response.json()
        assert user_data["score"] == len(questions)
        assert user_data["accuracy"] == 100.0
        
        # Step 4: Verify user appears on leaderboard
        response = client.get("/api/v1/score/leaderboard/top")
        assert response.status_code == 200
        
        leaderboard = response.json()["leaderboard"]
        assert any(entry["username"] == username for entry in leaderboard)
    
    def test_analytics_and_questions_consistency(self):
        """Test data consistency across analytics and question endpoints."""
        # Get total count from analytics
        stats_response = client.get("/api/v1/stats")
        assert stats_response.status_code == 200
        stats = stats_response.json()
        total_from_stats = stats["total_questions"]
        
        # Get count from count endpoint
        count_response = client.get("/api/v1/count")
        assert count_response.status_code == 200
        total_from_count = count_response.json()["total_questions"]
        
        # Both should match
        assert total_from_stats == total_from_count
        
        # Categories should be consistent
        cat_response = client.get("/api/v1/categories")
        categories_list = cat_response.json()["categories"]
        
        stats_categories = list(stats["categories"].keys())
        assert set(categories_list) == set(stats_categories)


class TestErrorHandling:
    """Test global error handling."""
    
    def test_404_error_format(self):
        """Test 404 errors have proper format."""
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == 404
        
        data = response.json()
        assert "error" in data or "detail" in data
    
    def test_validation_error_format(self):
        """Test validation errors have proper format."""
        # Invalid count parameter
        response = client.get("/api/v1/questions/random?count=-1")
        assert response.status_code == 422
        
        data = response.json()
        assert "detail" in data or "error" in data
    
    def test_user_not_found_error(self):
        """Test user not found returns proper error."""
        response = client.get("/api/v1/score/NonExistentUser999")
        assert response.status_code == 404
        
        data = response.json()
        assert "error" in data or "detail" in data


class TestDocumentation:
    """Test API documentation endpoints."""
    
    def test_openapi_schema_accessible(self):
        """Test OpenAPI schema is accessible."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["version"] == "1.0.0"
    
    def test_swagger_ui_accessible(self):
        """Test Swagger UI is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_accessible(self):
        """Test ReDoc is accessible."""
        response = client.get("/redoc")
        assert response.status_code == 200
    
    def test_api_tags_in_schema(self):
        """Test that all expected tags are in OpenAPI schema."""
        response = client.get("/openapi.json")
        schema = response.json()
        
        tags = [tag["name"] for tag in schema.get("tags", [])]
        expected_tags = ["Root", "System", "Questions", "Analytics", "Scoring"]
        
        for expected in expected_tags:
            assert expected in tags


class TestPerformance:
    """Basic performance tests."""
    
    def test_random_questions_response_time(self):
        """Test random questions endpoint responds quickly."""
        import time
        
        start = time.time()
        response = client.get("/api/v1/questions/random?count=10")
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 1.0  # Should respond in under 1 second
    
    def test_stats_endpoint_response_time(self):
        """Test stats endpoint responds quickly."""
        import time
        
        start = time.time()
        response = client.get("/api/v1/stats")
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 1.0  # Should respond in under 1 second


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

