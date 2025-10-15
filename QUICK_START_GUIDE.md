# QuizForge API v1.0.0 - Quick Start Guide

## 🚀 Running the Application

### Option 1: Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn src.main:app --reload --port 8000
```

### Option 2: Docker
```bash
# Build and run
docker build -t quizforge-api .
docker run -d -p 8000:8000 --name quizforge quizforge-api
```

The API will be available at: **http://localhost:8000**

---

## 📚 API Endpoints Overview

### Core Features (Questions)
- `GET /api/v1/questions/random?count=5` - Get random questions
- `GET /api/v1/questions/category/{name}` - Filter by category
- `GET /api/v1/questions/search?q=keyword` - Search questions
- `POST /api/v1/questions/answer` - Validate answer

### Analytics
- `GET /api/v1/stats` - Complete dataset statistics
- `GET /api/v1/categories` - List all categories
- `GET /api/v1/categories/stats` - Detailed category breakdown

### Scoring & Leaderboard (NEW in v1.0.0)
- `POST /api/v1/score/submit?username=USER&question_id=1&correct=true`
- `GET /api/v1/score/{username}` - Get user stats
- `GET /api/v1/score/leaderboard/top?limit=10` - View leaderboard
- `DELETE /api/v1/score/{username}` - Reset user session

---

## 🎮 Example Workflow

### 1. Get Random Questions for Quiz
```bash
curl http://localhost:8000/api/v1/questions/random?count=5
```

### 2. User Takes Quiz and Submits Answers
```bash
# Correct answer
curl -X POST "http://localhost:8000/api/v1/score/submit?username=Alice&question_id=1&correct=true"

# Incorrect answer
curl -X POST "http://localhost:8000/api/v1/score/submit?username=Alice&question_id=2&correct=false"
```

### 3. Check User Progress
```bash
curl http://localhost:8000/api/v1/score/Alice
```

**Response:**
```json
{
  "username": "Alice",
  "score": 1,
  "accuracy": 50.0,
  "total_attempts": 2,
  "created_at": "2025-10-15T10:00:00",
  "last_updated": "2025-10-15T10:05:00",
  "answers": [...]
}
```

### 4. View Leaderboard
```bash
curl http://localhost:8000/api/v1/score/leaderboard/top?limit=10
```

---

## 🧪 Testing

Run the complete test suite:
```bash
pytest tests/ -v
```

Run specific test categories:
```bash
pytest tests/test_scoring.py -v      # Scoring tests
pytest tests/test_integration.py -v  # Integration tests
pytest tests/test_questions.py -v    # Question tests
```

---

## 📖 Documentation

Interactive API documentation available at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🔧 Configuration

Create a `.env` file:
```env
APP_NAME=QuizForge API
APP_VERSION=1.0.0
DATA_PATH=docs/questions.json
PORT=8000
```

---

## 💾 Data Persistence

User sessions are automatically saved to:
- **File:** `data/sessions.json`
- **Format:** JSON array of user sessions
- **Backup:** Recommended to backup this file regularly

---

## 🎯 Key Features

### ✅ What's New in v1.0.0
- **API Versioning** with `/api/v1/` prefix
- **User Scoring System** - Track user performance
- **Global Leaderboard** - Competitive rankings
- **Session Persistence** - Save user progress
- **Docker Support** - Easy deployment
- **Global Error Handling** - Consistent error responses
- **Integration Tests** - End-to-end testing
- **110 Comprehensive Tests** - Full coverage

### ✅ Core Features
- 99 curated quiz questions
- 48 unique categories
- 3 difficulty levels (Easy, Medium, Hard)
- Random question generation
- Search and filtering
- Answer validation with explanations
- Comprehensive analytics

---

## 🚨 Important Notes

1. **API Versioning:** All endpoints now use `/api/v1/` prefix
2. **Sessions:** User data persists across restarts via `data/sessions.json`
3. **Leaderboard:** Sorted by score (primary) and accuracy (tiebreaker)
4. **Docker:** Container includes health checks and proper security settings
5. **Testing:** All 110 tests must pass before deployment

---

## 📞 Support

- **Documentation:** `/docs` endpoint
- **GitHub Issues:** For bug reports and feature requests
- **Tests:** Run `pytest -v` to verify installation

---

**Version:** 1.0.0  
**Status:** Production Ready ✅  
**Tests:** 110/110 passing ✅

