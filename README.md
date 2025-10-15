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
✅ **Pagination Support** - Efficient handling of large datasets (10,000+ questions)  
✅ **Type Safety** - Full Pydantic validation for data integrity  
✅ **Testing Suite** - Comprehensive tests (41 tests) for all functionality  
✅ **CORS Support** - Cross-origin resource sharing enabled  

---

## 🏗️ Project Structure

```
quizforge-api/
├── docs/
│   └── questions.json          # Dataset with 99 questions
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entrypoint
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Environment configuration
│   │   └── loader.py           # Dataset loading logic
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── base.py             # Health & info routes
│   │   └── questions.py        # Question endpoints
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── question_schema.py  # Question models
│   │   └── response_schema.py  # Response models
│   └── utils/
│       ├── __init__.py
│       ├── file_manager.py     # File utilities
│       ├── logger.py           # Logging configuration
│       ├── randomizer.py       # Random sampling
│       └── pagination.py       # Pagination utilities
├── tests/
│   ├── __init__.py
│   ├── test_setup.py           # Setup tests
│   └── test_questions.py       # Question endpoint tests
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

---

## 📚 API Endpoints

### System Endpoints

| Method | Endpoint      | Description                          |
|--------|---------------|--------------------------------------|
| GET    | `/`           | Root endpoint - Welcome message      |
| GET    | `/health`     | Health check with system status      |
| GET    | `/api/info`   | API metadata and dataset information |

### Question Endpoints

| Method | Endpoint                           | Description                                    |
|--------|------------------------------------|------------------------------------------------|
| GET    | `/api/questions/`                  | Get all questions (paginated)                  |
| GET    | `/api/questions/{id}`              | Get specific question by ID                    |
| GET    | `/api/questions/random`            | Get random questions                           |
| GET    | `/api/questions/category/{name}`   | Filter questions by category                   |
| GET    | `/api/questions/difficulty/{level}`| Filter questions by difficulty (Easy/Medium/Hard)|
| GET    | `/api/questions/search`            | Search questions by keyword                    |
| GET    | `/api/questions/categories`        | Get list of all categories                     |
| GET    | `/api/questions/difficulties`      | Get list of all difficulty levels              |
| POST   | `/api/questions/answer`            | Validate answer and get feedback               |

### Documentation

| Endpoint   | Description                    |
|------------|--------------------------------|
| `/docs`    | Interactive Swagger UI         |
| `/redoc`   | Alternative ReDoc documentation|

### Example API Usage

#### 1. Get Random Questions
```bash
GET /api/questions/random?count=5
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
GET /api/questions/category/Geography?limit=10
```
Returns up to 10 questions from the Geography category.

#### 3. Search Questions
```bash
GET /api/questions/search?q=Cameroon&limit=5
```
Returns up to 5 questions containing "Cameroon" in the question text.

#### 4. Validate Answer
```bash
POST /api/questions/answer
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
GET /api/questions/categories
```
```json
{
  "count": 48,
  "categories": ["African Ethnography", "African Geography", "Ancient History", ...]
}
```

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

**Test Coverage (41 Tests):**
- ✅ System endpoints (health, info, root)
- ✅ Dataset loading and validation
- ✅ Random question generation
- ✅ Category filtering (case-insensitive)
- ✅ Difficulty filtering
- ✅ Search functionality with filters
- ✅ Answer validation (correct/incorrect)
- ✅ Pagination
- ✅ Error handling (404, 422, 400)
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

**Current Branch:** `phase-1-setup`

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

Phase 3+ planned features:
- ✅ ~~Question filtering by category/difficulty~~ (Phase 2 Complete)
- ✅ ~~Random question selection~~ (Phase 2 Complete)
- ✅ ~~Answer validation~~ (Phase 2 Complete)
- User authentication & authorization
- Quiz session management
- Score tracking & leaderboards
- User progress analytics
- Database integration (PostgreSQL)
- Caching layer (Redis)
- Rate limiting
- Admin dashboard
- Question contribution system
- Multi-language support

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
**Status:** Phase 2 - Core Endpoints Complete ✅

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

