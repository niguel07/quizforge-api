"""Tests for analytics endpoints."""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.loader import QUESTIONS_DATA

client = TestClient(app)


class TestStatsEndpoint:
    """Test the main stats endpoint."""
    
    def test_stats_endpoint_success(self):
        """Test that stats endpoint returns all required fields."""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_questions" in data
        assert "categories" in data
        assert "difficulty" in data
        assert "topics" in data
        assert "quality_stats" in data
        assert "unique_counts" in data
    
    def test_stats_total_questions(self):
        """Test that total_questions matches actual data."""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_questions"] == len(QUESTIONS_DATA)
    
    def test_stats_categories_is_dict(self):
        """Test that categories is a dictionary."""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data["categories"], dict)
        assert len(data["categories"]) > 0
    
    def test_stats_difficulty_is_dict(self):
        """Test that difficulty is a dictionary."""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data["difficulty"], dict)
        assert len(data["difficulty"]) > 0
    
    def test_stats_topics_is_list(self):
        """Test that topics is a list."""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data["topics"], list)
        assert len(data["topics"]) > 0
    
    def test_stats_quality_stats(self):
        """Test quality_stats structure."""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        
        data = response.json()
        quality_stats = data["quality_stats"]
        assert "min" in quality_stats
        assert "max" in quality_stats
        assert "average" in quality_stats
        assert quality_stats["min"] <= quality_stats["average"] <= quality_stats["max"]
    
    def test_stats_unique_counts(self):
        """Test unique_counts structure."""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        
        data = response.json()
        unique_counts = data["unique_counts"]
        assert "categories" in unique_counts
        assert "difficulties" in unique_counts
        assert "topics" in unique_counts
        assert all(isinstance(v, int) and v > 0 for v in unique_counts.values())


class TestCategoriesEndpoint:
    """Test the categories endpoint."""
    
    def test_categories_endpoint_success(self):
        """Test that categories endpoint returns data."""
        response = client.get("/api/v1/categories")
        assert response.status_code == 200
        
        data = response.json()
        assert "count" in data
        assert "categories" in data
    
    def test_categories_list_is_sorted(self):
        """Test that categories are sorted alphabetically."""
        response = client.get("/api/v1/categories")
        assert response.status_code == 200
        
        data = response.json()
        categories = data["categories"]
        assert categories == sorted(categories)
    
    def test_categories_count_matches_list(self):
        """Test that count matches list length."""
        response = client.get("/api/v1/categories")
        assert response.status_code == 200
        
        data = response.json()
        assert data["count"] == len(data["categories"])
    
    def test_categories_are_unique(self):
        """Test that all categories are unique."""
        response = client.get("/api/v1/categories")
        assert response.status_code == 200
        
        data = response.json()
        categories = data["categories"]
        assert len(categories) == len(set(categories))


class TestDifficultyEndpoint:
    """Test the difficulty endpoint."""
    
    def test_difficulty_endpoint_success(self):
        """Test that difficulty endpoint returns data."""
        response = client.get("/api/v1/difficulty")
        assert response.status_code == 200
        
        data = response.json()
        assert "count" in data
        assert "difficulty_levels" in data
    
    def test_difficulty_levels_valid(self):
        """Test that difficulty levels are valid."""
        response = client.get("/api/v1/difficulty")
        assert response.status_code == 200
        
        data = response.json()
        levels = data["difficulty_levels"]
        valid_levels = {"Easy", "Medium", "Hard"}
        
        for level in levels:
            assert level in valid_levels
    
    def test_difficulty_count_matches_list(self):
        """Test that count matches list length."""
        response = client.get("/api/v1/difficulty")
        assert response.status_code == 200
        
        data = response.json()
        assert data["count"] == len(data["difficulty_levels"])
    
    def test_difficulty_levels_sorted(self):
        """Test that difficulty levels are sorted."""
        response = client.get("/api/v1/difficulty")
        assert response.status_code == 200
        
        data = response.json()
        levels = data["difficulty_levels"]
        assert levels == sorted(levels)


class TestTopicsEndpoint:
    """Test the topics endpoint."""
    
    def test_topics_endpoint_success(self):
        """Test that topics endpoint returns data."""
        response = client.get("/api/v1/topics")
        assert response.status_code == 200
        
        data = response.json()
        assert "count" in data
        assert "topics" in data
    
    def test_topics_list_is_sorted(self):
        """Test that topics are sorted alphabetically."""
        response = client.get("/api/v1/topics")
        assert response.status_code == 200
        
        data = response.json()
        topics = data["topics"]
        assert topics == sorted(topics)
    
    def test_topics_count_matches_list(self):
        """Test that count matches list length."""
        response = client.get("/api/v1/topics")
        assert response.status_code == 200
        
        data = response.json()
        assert data["count"] == len(data["topics"])
    
    def test_topics_are_unique(self):
        """Test that all topics are unique."""
        response = client.get("/api/v1/topics")
        assert response.status_code == 200
        
        data = response.json()
        topics = data["topics"]
        assert len(topics) == len(set(topics))


class TestQuestionCountEndpoint:
    """Test the question count endpoint."""
    
    def test_count_endpoint_success(self):
        """Test that count endpoint returns data."""
        response = client.get("/api/v1/count")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_questions" in data
    
    def test_count_is_positive(self):
        """Test that count is a positive number."""
        response = client.get("/api/v1/count")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_questions"] > 0
    
    def test_count_matches_data(self):
        """Test that count matches actual dataset size."""
        response = client.get("/api/v1/count")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_questions"] == len(QUESTIONS_DATA)


class TestSummaryEndpoint:
    """Test the summary endpoint."""
    
    def test_summary_endpoint_success(self):
        """Test that summary endpoint returns data."""
        response = client.get("/api/v1/summary")
        assert response.status_code == 200
        
        data = response.json()
        assert "summary" in data
    
    def test_summary_contains_all_stats(self):
        """Test that summary contains all expected fields."""
        response = client.get("/api/v1/summary")
        assert response.status_code == 200
        
        summary = response.json()["summary"]
        assert "total_questions" in summary
        assert "categories" in summary
        assert "difficulty" in summary
        assert "topics" in summary
        assert "quality_stats" in summary
        assert "unique_counts" in summary
    
    def test_summary_matches_stats_endpoint(self):
        """Test that summary matches stats endpoint data."""
        stats_response = client.get("/api/v1/stats")
        summary_response = client.get("/api/v1/summary")
        
        assert stats_response.status_code == 200
        assert summary_response.status_code == 200
        
        stats_data = stats_response.json()
        summary_data = summary_response.json()["summary"]
        
        assert stats_data["total_questions"] == summary_data["total_questions"]
        assert len(stats_data["categories"]) == len(summary_data["categories"])


class TestCategoryStatsEndpoint:
    """Test the detailed category stats endpoint."""
    
    def test_category_stats_endpoint_success(self):
        """Test that category stats endpoint returns data."""
        response = client.get("/api/v1/categories/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_categories" in data
        assert "stats" in data
    
    def test_category_stats_structure(self):
        """Test that each category stat has required fields."""
        response = client.get("/api/v1/categories/stats")
        assert response.status_code == 200
        
        data = response.json()
        stats = data["stats"]
        
        if stats:
            first_stat = stats[0]
            assert "category" in first_stat
            assert "count" in first_stat
            assert "percentage" in first_stat
            assert "difficulty_breakdown" in first_stat
    
    def test_category_stats_percentages(self):
        """Test that percentages add up correctly."""
        response = client.get("/api/v1/categories/stats")
        assert response.status_code == 200
        
        data = response.json()
        stats = data["stats"]
        
        total_percentage = sum(stat["percentage"] for stat in stats)
        # Allow small floating point error
        assert 99.9 <= total_percentage <= 100.1
    
    def test_category_stats_sorted_by_count(self):
        """Test that stats are sorted by count (descending)."""
        response = client.get("/api/v1/categories/stats")
        assert response.status_code == 200
        
        data = response.json()
        stats = data["stats"]
        
        if len(stats) > 1:
            counts = [stat["count"] for stat in stats]
            assert counts == sorted(counts, reverse=True)


class TestDifficultyStatsEndpoint:
    """Test the detailed difficulty stats endpoint."""
    
    def test_difficulty_stats_endpoint_success(self):
        """Test that difficulty stats endpoint returns data."""
        response = client.get("/api/v1/difficulty/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_levels" in data
        assert "stats" in data
    
    def test_difficulty_stats_structure(self):
        """Test that each difficulty stat has required fields."""
        response = client.get("/api/v1/difficulty/stats")
        assert response.status_code == 200
        
        data = response.json()
        stats = data["stats"]
        
        if stats:
            first_stat = stats[0]
            assert "level" in first_stat
            assert "count" in first_stat
            assert "percentage" in first_stat
    
    def test_difficulty_stats_percentages(self):
        """Test that percentages add up to 100."""
        response = client.get("/api/v1/difficulty/stats")
        assert response.status_code == 200
        
        data = response.json()
        stats = data["stats"]
        
        total_percentage = sum(stat["percentage"] for stat in stats)
        # Allow small floating point error
        assert 99.9 <= total_percentage <= 100.1
    
    def test_difficulty_stats_order(self):
        """Test that difficulty stats are in correct order."""
        response = client.get("/api/v1/difficulty/stats")
        assert response.status_code == 200
        
        data = response.json()
        stats = data["stats"]
        levels = [stat["level"] for stat in stats]
        
        # Check if Easy, Medium, Hard order is maintained (when all present)
        expected_order = ["Easy", "Medium", "Hard"]
        for level in levels:
            assert level in expected_order


class TestAnalyticsIntegration:
    """Test analytics endpoints integration."""
    
    def test_all_analytics_endpoints_accessible(self):
        """Test that all analytics endpoints are accessible."""
        endpoints = [
            "/api/v1/stats",
            "/api/v1/categories",
            "/api/v1/difficulty",
            "/api/v1/topics",
            "/api/v1/count",
            "/api/v1/summary",
            "/api/v1/categories/stats",
            "/api/v1/difficulty/stats"
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200, f"Failed to access {endpoint}"
    
    def test_analytics_data_consistency(self):
        """Test consistency across different analytics endpoints."""
        stats = client.get("/api/v1/stats").json()
        categories = client.get("/api/v1/categories").json()
        difficulties = client.get("/api/v1/difficulty").json()
        topics = client.get("/api/v1/topics").json()
        count = client.get("/api/v1/count").json()
        
        # All should reflect same dataset size
        assert stats["total_questions"] == count["total_questions"]
        
        # Unique counts should match
        assert stats["unique_counts"]["categories"] == categories["count"]
        assert stats["unique_counts"]["difficulties"] == difficulties["count"]
        assert stats["unique_counts"]["topics"] == topics["count"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

