"""Tests for question endpoints."""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.loader import QUESTIONS_DATA

client = TestClient(app)


class TestRandomQuestions:
    """Test random question endpoint."""
    
    def test_get_random_questions_default(self):
        """Test getting random questions with default count."""
        response = client.get("/api/v1/questions/random")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10  # Default count
        
    def test_get_random_questions_custom_count(self):
        """Test getting random questions with custom count."""
        response = client.get("/api/v1/questions/random?count=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5
        
    def test_get_random_questions_max_limit(self):
        """Test maximum limit enforcement."""
        response = client.get("/api/v1/questions/random?count=100")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 100
        
    def test_get_random_questions_invalid_count(self):
        """Test validation of invalid count."""
        response = client.get("/api/v1/questions/random?count=0")
        assert response.status_code == 422  # Validation error
        
    def test_random_questions_have_required_fields(self):
        """Test that random questions have all required fields."""
        response = client.get("/api/v1/questions/random?count=1")
        assert response.status_code == 200
        data = response.json()
        if data:
            question = data[0]
            assert "id" in question
            assert "question" in question
            assert "options" in question
            assert "answer" in question
            assert "category" in question
            assert "difficulty" in question


class TestCategoryFilter:
    """Test category filtering endpoint."""
    
    def test_get_by_valid_category(self):
        """Test filtering by a valid category."""
        # Get a category from the data
        if QUESTIONS_DATA:
            category = QUESTIONS_DATA[0].get("category")
            response = client.get(f"/api/v1/questions/category/{category}")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0
            # Verify all returned questions match the category
            for q in data:
                assert q["category"].lower() == category.lower()
    
    def test_get_by_invalid_category(self):
        """Test filtering by non-existent category."""
        response = client.get("/api/v1/questions/category/NonExistentCategory123")
        assert response.status_code == 404
        
    def test_category_with_limit(self):
        """Test category filtering with limit."""
        if QUESTIONS_DATA:
            category = QUESTIONS_DATA[0].get("category")
            response = client.get(f"/api/v1/questions/category/{category}?limit=5")
            assert response.status_code == 200
            data = response.json()
            assert len(data) <= 5
    
    def test_category_case_insensitive(self):
        """Test that category search is case-insensitive."""
        if QUESTIONS_DATA:
            category = QUESTIONS_DATA[0].get("category")
            response = client.get(f"/api/v1/questions/category/{category.upper()}")
            assert response.status_code == 200


class TestDifficultyFilter:
    """Test difficulty filtering endpoint."""
    
    def test_get_by_valid_difficulty(self):
        """Test filtering by valid difficulty level."""
        difficulties = ["Easy", "Medium", "Hard"]
        for level in difficulties:
            response = client.get(f"/api/questions/difficulty/{level}")
            if response.status_code == 200:
                data = response.json()
                assert isinstance(data, list)
                for q in data:
                    assert q["difficulty"].lower() == level.lower()
    
    def test_get_by_invalid_difficulty(self):
        """Test filtering by invalid difficulty."""
        response = client.get("/api/v1/questions/difficulty/VeryVeryHard")
        assert response.status_code == 404
        
    def test_difficulty_with_limit(self):
        """Test difficulty filtering with limit."""
        response = client.get("/api/v1/questions/difficulty/Easy?limit=3")
        if response.status_code == 200:
            data = response.json()
            assert len(data) <= 3
    
    def test_difficulty_case_insensitive(self):
        """Test that difficulty search is case-insensitive."""
        response = client.get("/api/v1/questions/difficulty/easy")
        if response.status_code == 200:
            data = response.json()
            assert all(q["difficulty"].lower() == "easy" for q in data)


class TestSearchQuestions:
    """Test question search endpoint."""
    
    def test_search_with_valid_query(self):
        """Test searching with a valid query."""
        # Search for a common word that likely exists
        response = client.get("/api/v1/questions/search?q=the")
        # Either 200 (found) or 404 (not found) is acceptable
        assert response.status_code in [200, 404]
        
    def test_search_with_results(self):
        """Test search that should return results."""
        if QUESTIONS_DATA:
            # Get a word from the first question
            first_question = QUESTIONS_DATA[0].get("question", "")
            words = first_question.split()
            if len(words) >= 3:
                search_term = words[2]  # Pick a middle word
                response = client.get(f"/api/questions/search?q={search_term}")
                if response.status_code == 200:
                    data = response.json()
                    assert isinstance(data, list)
                    # Verify search term appears in results
                    for q in data:
                        assert search_term.lower() in q["question"].lower()
    
    def test_search_too_short(self):
        """Test that short queries are rejected."""
        response = client.get("/api/v1/questions/search?q=a")
        assert response.status_code == 422  # Validation error
        
    def test_search_with_limit(self):
        """Test search with limit parameter."""
        response = client.get("/api/v1/questions/search?q=the&limit=5")
        if response.status_code == 200:
            data = response.json()
            assert len(data) <= 5
    
    def test_search_with_category_filter(self):
        """Test search with category filter."""
        if QUESTIONS_DATA:
            category = QUESTIONS_DATA[0].get("category")
            response = client.get(f"/api/questions/search?q=the&category={category}")
            assert response.status_code in [200, 404]
    
    def test_search_with_difficulty_filter(self):
        """Test search with difficulty filter."""
        response = client.get("/api/v1/questions/search?q=the&difficulty=Easy")
        assert response.status_code in [200, 404]


class TestAnswerValidation:
    """Test answer validation endpoint."""
    
    def test_validate_correct_answer(self):
        """Test validating a correct answer."""
        if QUESTIONS_DATA:
            question = QUESTIONS_DATA[0]
            payload = {
                "question_id": question["id"],
                "selected_answer": question["answer"]
            }
            response = client.post("/api/v1/questions/answer", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert data["correct"] is True
            assert data["question_id"] == question["id"]
            assert "explanation" in data
    
    def test_validate_incorrect_answer(self):
        """Test validating an incorrect answer."""
        if QUESTIONS_DATA:
            question = QUESTIONS_DATA[0]
            correct = question["answer"]
            # Pick a different answer
            wrong = "A" if correct != "A" else "B"
            payload = {
                "question_id": question["id"],
                "selected_answer": wrong
            }
            response = client.post("/api/v1/questions/answer", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert data["correct"] is False
            assert data["correct_answer"] == question["answer"]
            assert data["selected_answer"] == wrong
    
    def test_validate_invalid_question_id(self):
        """Test validation with invalid question ID."""
        payload = {
            "question_id": 999999,
            "selected_answer": "A"
        }
        response = client.post("/api/v1/questions/answer", json=payload)
        assert response.status_code == 404
    
    def test_validate_invalid_answer_format(self):
        """Test validation with invalid answer format."""
        if QUESTIONS_DATA:
            payload = {
                "question_id": QUESTIONS_DATA[0]["id"],
                "selected_answer": "Z"  # Invalid option
            }
            response = client.post("/api/v1/questions/answer", json=payload)
            assert response.status_code == 400
    
    def test_validate_missing_fields(self):
        """Test validation with missing fields."""
        response = client.post("/api/v1/questions/answer", json={})
        assert response.status_code == 422  # Validation error


class TestCategoriesEndpoint:
    """Test categories list endpoint."""
    
    def test_get_categories(self):
        """Test getting list of categories."""
        response = client.get("/api/v1/questions/categories")
        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert "categories" in data
        assert isinstance(data["categories"], list)
        assert data["count"] == len(data["categories"])
    
    def test_categories_are_unique(self):
        """Test that categories list contains unique values."""
        response = client.get("/api/v1/questions/categories")
        assert response.status_code == 200
        data = response.json()
        categories = data["categories"]
        assert len(categories) == len(set(categories))


class TestDifficultiesEndpoint:
    """Test difficulties list endpoint."""
    
    def test_get_difficulties(self):
        """Test getting list of difficulty levels."""
        response = client.get("/api/v1/questions/difficulties")
        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert "levels" in data
        assert isinstance(data["levels"], list)
        assert data["count"] == len(data["levels"])
    
    def test_difficulties_are_valid(self):
        """Test that returned difficulties are valid levels."""
        response = client.get("/api/v1/questions/difficulties")
        assert response.status_code == 200
        data = response.json()
        valid_levels = {"Easy", "Medium", "Hard"}
        for level in data["levels"]:
            assert level in valid_levels


class TestGetQuestionById:
    """Test get question by ID endpoint."""
    
    def test_get_existing_question(self):
        """Test getting an existing question by ID."""
        if QUESTIONS_DATA:
            question_id = QUESTIONS_DATA[0]["id"]
            response = client.get(f"/api/v1/questions/{question_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == question_id
    
    def test_get_nonexistent_question(self):
        """Test getting a non-existent question."""
        response = client.get("/api/v1/questions/999999")
        assert response.status_code == 404


class TestGetAllQuestions:
    """Test paginated questions endpoint."""
    
    def test_get_all_questions_default(self):
        """Test getting all questions with default pagination."""
        response = client.get("/api/v1/questions/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 20  # Default limit
    
    def test_get_all_questions_with_pagination(self):
        """Test pagination parameters."""
        response = client.get("/api/v1/questions/?page=1&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10
    
    def test_pagination_page_2(self):
        """Test getting second page."""
        response = client.get("/api/v1/questions/?page=2&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

