"""Setup and integration tests for QuizForge API."""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.loader import QUESTIONS_DATA

# Create test client
client = TestClient(app)


class TestSystemEndpoints:
    """Test system endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "1.0.0"
    
    def test_health_route(self):
        """Test health endpoint returns OK status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["app"] == "QuizForge API"
        assert data["version"] == "1.0.0"
        assert "data_loaded" in data
    
    def test_api_info_route(self):
        """Test API info endpoint returns metadata."""
        response = client.get("/api/info")
        assert response.status_code == 200
        data = response.json()
        assert "total_questions" in data
        assert "data_path" in data
        assert "categories" in data
        assert "difficulty_levels" in data
        assert data["app_name"] == "QuizForge API"
        assert data["total_questions"] > 0


class TestDatasetLoading:
    """Test dataset loading functionality."""
    
    def test_dataset_loaded(self):
        """Test that dataset is loaded successfully."""
        assert len(QUESTIONS_DATA) > 0, "Dataset should contain questions"
    
    def test_dataset_structure(self):
        """Test that loaded questions have correct structure."""
        if QUESTIONS_DATA:
            sample_question = QUESTIONS_DATA[0]
            required_fields = [
                "question",
                "options",
                "answer",
                "category",
                "difficulty",
                "explanation",
                "quality_score",
                "source_topic"
            ]
            for field in required_fields:
                assert field in sample_question, f"Question missing field: {field}"
    
    def test_options_structure(self):
        """Test that question options have correct structure."""
        if QUESTIONS_DATA:
            sample_question = QUESTIONS_DATA[0]
            options = sample_question.get("options", {})
            assert isinstance(options, dict), "Options should be a dictionary"
            required_options = ["A", "B", "C", "D"]
            for option in required_options:
                assert option in options, f"Options missing key: {option}"


class TestDocumentation:
    """Test API documentation endpoints."""
    
    def test_openapi_docs_accessible(self):
        """Test that OpenAPI docs are accessible."""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_accessible(self):
        """Test that ReDoc documentation is accessible."""
        response = client.get("/redoc")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

