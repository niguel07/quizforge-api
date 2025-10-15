# QuizForge API

> A production-grade FastAPI backend for quiz management

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📖 Overview

QuizForge API is a robust, scalable backend service built with FastAPI for managing and serving quiz questions. This implementation provides a complete REST API with filtering, search, randomization, and answer validation capabilities - optimized for educational platforms and quiz applications.

### Key Features

✅ **Production-Ready Architecture** - Modular structure with clear separation of concerns  
✅ **Environment Configuration** - Flexible settings management with `.env` support  
✅ **Dataset Management** - Efficient loading and validation of JSON question datasets  
✅ **RESTful API** - Clean endpoints with automatic OpenAPI documentation  
✅ **Question Filtering** - Filter by category, difficulty, or search by keyword  
✅ **Random Questions** - Generate random question sets for quizzes  
✅ **Answer Validation** - Validate learner answers with detailed feedback  
✅ **Analytics & Insights** - Comprehensive dataset statistics and aggregations  
✅ **Performance Optimized** - Efficient aggregations for 10,000+ questions  
✅ **Pagination Support** - Efficient handling of large datasets  
✅ **Type Safety** - Full Pydantic validation for data integrity  
✅ **Testing Suite** - Comprehensive tests (110 tests) for all functionality  
✅ **Docker Support** - Production-ready containerization  
✅ **API Versioning** - Version control with `/api/v1/` prefix  
✅ **Session Management** - User session tracking and persistence  
✅ **Leaderboard System** - User rankings and competition tracking  
✅ **CORS Support** - Cross-origin resource sharing enabled  

---

## 🏗️ Project Structure

```
quizforge-api/
├── docs/
│   └── questions.json          # Dataset with 99 questions
├── data/
│   └── sessions.json           # User session data storage
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entrypoint
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Environment configuration
│   │   ├── loader.py           # Dataset loading logic
│   │   └── error_handler.py   # Global error handling
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── base.py             # Health & info routes
│   │   ├── questions.py        # Question endpoints
│   │   ├── analytics.py        # Analytics endpoints
│   │   └── scoring.py          # Scoring & leaderboard endpoints
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── question_schema.py  # Question models
│   │   ├── response_schema.py  # Response models
│   │   ├── analytics_schema.py # Analytics models
│   │   └── scoring_schema.py   # Scoring models
│   └── utils/
│       ├── __init__.py
│       ├── file_manager.py     # File utilities
│       ├── logger.py           # Logging configuration
│       ├── randomizer.py       # Random sampling
│       ├── pagination.py       # Pagination utilities
│       ├── analyzer.py         # Analytics aggregations
│       └── scorer.py           # Session & scoring logic
├── tests/
│   ├── __init__.py
│   ├── test_setup.py           # Setup tests
│   ├── test_questions.py       # Question endpoint tests
│   ├── test_analytics.py       # Analytics endpoint tests
│   ├── test_scoring.py         # Scoring endpoint tests
│   └── test_integration.py     # End-to-end integration tests
├── Dockerfile                  # Docker container configuration
├── .dockerignore               # Docker ignore rules
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/niguel07/quizforge-api.git
   cd quizforge-api
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment (optional)**
   ```bash
   cp .env.example .env
   # Edit .env with your custom settings
   ```

### Running the API

**Development Server:**
```bash
uvicorn src.main:app --reload --port 8000
```

**Or using Python directly:**
```bash
python -m src.main
```

The API will be available at: **http://localhost:8000**

### Running with Docker

**Build the Docker image:**
```bash
docker build -t quizforge-api .
```

**Run the container:**
```bash
docker run -d -p 8000:8000 --name quizforge quizforge-api
```

**Using Docker Compose (optional):**
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - APP_NAME=QuizForge API
      - PORT=8000
```

```bash
docker-compose up -d
```

---

## 📚 API Endpoints

> **Note:** All endpoints use the `/api/v1/` prefix for version control

### System Endpoints

| Method | Endpoint          | Description                          |
|--------|-------------------|--------------------------------------|
| GET    | `/`               | Root endpoint - Welcome message      |
| GET    | `/api/v1/health`  | Health check with system status      |
| GET    | `/api/v1/info`    | API metadata and dataset information |

### Question Endpoints

| Method | Endpoint                                   | Description                                    |
|--------|--------------------------------------------|------------------------------------------------|
| GET    | `/api/v1/questions/`                       | Get all questions (paginated)                  |
| GET    | `/api/v1/questions/{id}`                   | Get specific question by ID                    |
| GET    | `/api/v1/questions/random`                 | Get random questions                           |
| GET    | `/api/v1/questions/category/{name}`        | Filter questions by category                   |
| GET    | `/api/v1/questions/difficulty/{level}`     | Filter questions by difficulty (Easy/Medium/Hard)|
| GET    | `/api/v1/questions/search`                 | Search questions by keyword                    |
| GET    | `/api/v1/questions/categories`             | Get list of all categories                     |
| GET    | `/api/v1/questions/difficulties`           | Get list of all difficulty levels              |
| POST   | `/api/v1/questions/answer`                 | Validate answer and get feedback               |

### Analytics Endpoints

| Method | Endpoint                        | Description                                        |
|--------|---------------------------------|----------------------------------------------------|
| GET    | `/api/v1/stats`                 | Comprehensive dataset statistics                   |
| GET    | `/api/v1/categories`            | List of all unique categories                      |
| GET    | `/api/v1/difficulty`            | List of all difficulty levels                      |
| GET    | `/api/v1/topics`                | List of all unique topics                          |
| GET    | `/api/v1/count`                 | Total question count                               |
| GET    | `/api/v1/summary`               | Compact summary of all metadata                    |
| GET    | `/api/v1/categories/stats`      | Detailed category statistics with percentages      |
| GET    | `/api/v1/difficulty/stats`      | Detailed difficulty statistics with percentages    |

### Scoring & Leaderboard Endpoints

| Method | Endpoint                          | Description                                        |
|--------|-----------------------------------|----------------------------------------------------|
| POST   | `/api/v1/score/submit`            | Submit an answer and update user session           |
| GET    | `/api/v1/score/{username}`        | Get user session statistics                        |
| GET    | `/api/v1/score/leaderboard/top`   | Get global leaderboard (top users)                 |
| GET    | `/api/v1/score/users/list`        | Get list of all users with active sessions         |
| DELETE | `/api/v1/score/{username}`        | Reset (delete) a user's session data               |

### Documentation

| Endpoint   | Description                    |
|------------|--------------------------------|
| `/docs`    | Interactive Swagger UI         |
| `/redoc`   | Alternative ReDoc documentation|

### Example API Usage

#### 1. Get Random Questions
```bash
GET /api/v1/questions/random?count=5
```
```json
[
  {
    "id": 42,
    "question": "When was the German-Douala Treaty signed?",
    "options": {"A": "12 June 1884", "B": "12 July 1884", "C": "...", "D": "..."},
    "answer": "B",
    "category": "Colonial History",
    "difficulty": "Easy",
    "explanation": "The treaty was signed on July 12, 1884...",
    "quality_score": 1.0,
    "source_topic": "history"
  }
]
```

#### 2. Filter by Category
```bash
GET /api/v1/questions/category/Geography?limit=10
```
Returns up to 10 questions from the Geography category.

#### 3. Search Questions
```bash
GET /api/v1/questions/search?q=Cameroon&limit=5
```
Returns up to 5 questions containing "Cameroon" in the question text.

#### 4. Validate Answer
```bash
POST /api/v1/questions/answer
Content-Type: application/json

{
  "question_id": 42,
  "selected_answer": "B"
}
```
**Response:**
```json
{
  "question_id": 42,
  "correct": true,
  "correct_answer": "B",
  "selected_answer": "B",
  "explanation": "The German-Douala Treaty was signed on July 12, 1884..."
}
```

#### 5. Get Categories List
```bash
GET /api/v1/questions/categories
```
```json
{
  "count": 48,
  "categories": ["African Ethnography", "African Geography", "Ancient History", ...]
}
```

#### 6. Get Analytics Statistics
```bash
GET /api/v1/stats
```
```json
{
  "total_questions": 99,
  "categories": {
    "Colonial History": 15,
    "African History": 12,
    "Geography": 8
  },
  "difficulty": {
    "Easy": 30,
    "Medium": 45,
    "Hard": 24
  },
  "topics": ["history", "geography", "science"],
  "quality_stats": {
    "min": 0.96,
    "max": 1.0,
    "average": 0.99
  },
  "unique_counts": {
    "categories": 48,
    "difficulties": 3,
    "topics": 1
  }
}
```

#### 7. Get Detailed Category Stats
```bash
GET /api/v1/categories/stats
```
```json
{
  "total_categories": 48,
  "stats": [
    {
      "category": "Colonial History",
      "count": 15,
      "percentage": 15.15,
      "difficulty_breakdown": {
        "Easy": 5,
        "Medium": 7,
        "Hard": 3
      }
    }
  ]
}
```

#### 8. Submit Answer and Track Score
```bash
POST /api/v1/score/submit?username=JohnDoe&question_id=42&correct=true
```
**Response:**
```json
{
  "username": "JohnDoe",
  "score": 15,
  "accuracy": 78.95,
  "total_attempts": 19,
  "created_at": "2025-10-15T10:30:00",
  "last_updated": "2025-10-15T14:22:00",
  "answers": [
    {
      "question_id": 42,
      "correct": true,
      "timestamp": "2025-10-15T14:22:00"
    }
  ]
}
```

#### 9. Get User Statistics
```bash
GET /api/v1/score/JohnDoe
```
Returns complete user session with score, accuracy, and answer history.

#### 10. Get Leaderboard
```bash
GET /api/v1/score/leaderboard/top?limit=10
```
**Response:**
```json
{
  "total_users": 45,
  "leaderboard": [
    {
      "username": "TopPlayer",
      "score": 98,
      "accuracy": 98.0,
      "total_attempts": 100
    },
    {
      "username": "JohnDoe",
      "score": 95,
      "accuracy": 95.0,
      "total_attempts": 100
    }
  ]
}
```

#### 11. Get All Users
```bash
GET /api/v1/score/users/list
```
Returns list of all users with active sessions.

#### 12. Reset User Session
```bash
DELETE /api/v1/score/JohnDoe
```
Permanently deletes user session data.

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_questions.py -v

# Run with coverage report
pytest --cov=src tests/
```

**Test Coverage (110 Tests):**
- ✅ System endpoints (health, info, root)
- ✅ Dataset loading and validation
- ✅ Random question generation
- ✅ Category filtering (case-insensitive)
- ✅ Difficulty filtering
- ✅ Search functionality with filters
- ✅ Answer validation (correct/incorrect)
- ✅ Pagination
- ✅ Analytics & statistics endpoints
- ✅ Category and difficulty statistics
- ✅ Data consistency across endpoints
- ✅ Scoring & session management
- ✅ Leaderboard functionality
- ✅ User session persistence
- ✅ Integration tests (end-to-end workflows)
- ✅ API versioning (`/api/v1/` prefix)
- ✅ Global error handling
- ✅ Performance benchmarks
- ✅ Error handling (404, 422, 400, 500, 503)
- ✅ API documentation accessibility

---

## ⚙️ Configuration

Configuration is managed through environment variables. Create a `.env` file in the project root:

```env
APP_NAME=QuizForge API
APP_VERSION=1.0.0
DATA_PATH=docs/questions.json
PORT=8000
```

### Configuration Options

| Variable      | Default              | Description                    |
|---------------|----------------------|--------------------------------|
| `APP_NAME`    | QuizForge API        | Application name               |
| `APP_VERSION` | 1.0.0                | API version                    |
| `DATA_PATH`   | docs/questions.json  | Path to questions dataset      |
| `PORT`        | 8000                 | Server port                    |

---

## 📊 Dataset Structure

Questions follow this schema:

```json
{
  "question": "What is the capital of France?",
  "options": {
    "A": "London",
    "B": "Paris",
    "C": "Berlin",
    "D": "Madrid"
  },
  "answer": "B",
  "category": "Geography",
  "difficulty": "Easy",
  "explanation": "Paris is the capital and most populous city of France.",
  "quality_score": 1.0,
  "source_topic": "geography"
}
```

### Dataset Statistics

- **Total Questions:** 99
- **Categories:** 48 unique categories
- **Difficulty Levels:** Easy, Medium, Hard
- **Source Topic:** History (Cameroon focus)

---

## 🛠️ Development

### Code Quality

The project follows these principles:
- **PEP 8** style guidelines
- **Type hints** for better IDE support
- **Docstrings** for all functions and classes
- **Modular architecture** for scalability

### Adding New Features

1. Create feature branch from `main`
2. Implement changes with tests
3. Run test suite to ensure no regressions
4. Submit pull request with clear description

---

## 🔄 Git Workflow

This project uses a feature branch workflow:

```bash
# Create and switch to feature branch
git checkout -b feature-name

# Make changes and commit
git add .
git commit -m "Description of changes"

# Push to remote
git push origin feature-name
```

**Current Branch:** `phase-5-final-release`

---

## 📝 API Documentation

Once the server is running, visit:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Interactive documentation allows you to:
- Explore all endpoints
- Test API calls directly from browser
- View request/response schemas
- Download OpenAPI specification

---

## 🔮 Future Enhancements

Completed features:
- ✅ ~~Question filtering by category/difficulty~~ (Phase 2 Complete)
- ✅ ~~Random question selection~~ (Phase 2 Complete)
- ✅ ~~Answer validation~~ (Phase 2 Complete)
- ✅ ~~Analytics & statistics~~ (Phase 3 Complete)
- ✅ ~~Score tracking & leaderboards~~ (Phase 5 Complete)
- ✅ ~~Quiz session management~~ (Phase 5 Complete)
- ✅ ~~User progress analytics~~ (Phase 5 Complete)
- ✅ ~~API versioning~~ (Phase 5 Complete)
- ✅ ~~Docker support~~ (Phase 5 Complete)
- ✅ ~~Global error handling~~ (Phase 5 Complete)

Planned features (Phase 6+):
- 🔄 User authentication & authorization (JWT)
- 🔄 Database integration (PostgreSQL/MongoDB)
- 🔄 Caching layer (Redis)
- 🔄 Rate limiting & API throttling
- 🔄 Admin dashboard
- 🔄 Question contribution system
- 🔄 Multi-language support
- 🔄 Email notifications
- 🔄 Real-time quiz competitions
- 🔄 Advanced analytics dashboards

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your fork
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Authors

- **niguel07** - Initial work - [GitHub](https://github.com/niguel07)

---

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Contact: [GitHub Issues](https://github.com/niguel07/quizforge-api/issues)

---

## 🙏 Acknowledgments

- FastAPI framework by Sebastián Ramírez
- Pydantic for data validation
- The Python community

---

**Version:** 1.0.0  
**Last Updated:** October 2025  
**Status:** Phase 5 - Final Release Complete ✅

---

## 📋 API Query Parameters

### Random Questions
- `count` (int, 1-100): Number of questions to return (default: 10)

### Category/Difficulty Filters
- `limit` (int, 1-100): Maximum questions to return (default: 20)

### Search
- `q` (string, min 2 chars): Search query
- `limit` (int, 1-100): Maximum results (default: 20)
- `category` (string, optional): Filter by category
- `difficulty` (string, optional): Filter by difficulty

### Pagination (All Questions)
- `page` (int, ≥1): Page number (default: 1)
- `limit` (int, 1-100): Items per page (default: 20)

