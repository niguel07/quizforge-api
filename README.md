# QuizForge API

> A production-grade FastAPI backend for quiz management

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📖 Overview

QuizForge API is a robust, scalable backend service built with FastAPI for managing and serving quiz questions. This Phase 1 implementation establishes the foundational architecture with clean code organization, environment configuration, and comprehensive testing.

### Key Features

✅ **Production-Ready Architecture** - Modular structure with clear separation of concerns  
✅ **Environment Configuration** - Flexible settings management with `.env` support  
✅ **Dataset Management** - Efficient loading and validation of JSON question datasets  
✅ **RESTful API** - Clean endpoints with automatic OpenAPI documentation  
✅ **Type Safety** - Full Pydantic validation for data integrity  
✅ **Testing Suite** - Comprehensive tests for all core functionality  
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
│   │   └── base.py             # Health & info routes
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── question_schema.py  # Pydantic models
│   └── utils/
│       ├── __init__.py
│       ├── file_manager.py     # File utilities
│       └── logger.py           # Logging configuration
├── tests/
│   ├── __init__.py
│   └── test_setup.py           # Test suite
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
| GET    | `/health`     | Health check                         |
| GET    | `/api/info`   | API metadata and dataset information |

### Documentation

| Endpoint   | Description                    |
|------------|--------------------------------|
| `/docs`    | Interactive Swagger UI         |
| `/redoc`   | Alternative ReDoc documentation|

### Example Responses

**Health Check (`/health`):**
```json
{
  "status": "ok",
  "app": "QuizForge API",
  "version": "1.0.0",
  "data_loaded": true
}
```

**API Info (`/api/info`):**
```json
{
  "app_name": "QuizForge API",
  "version": "1.0.0",
  "total_questions": 99,
  "data_path": "docs/questions.json",
  "categories": [
    "African Ethnography",
    "African Geography",
    "African History",
    "Ancient History",
    ...
  ],
  "difficulty_levels": [
    "Easy",
    "Hard",
    "Medium"
  ],
  "endpoints": {
    "health": "/health",
    "api_info": "/api/info"
  }
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
pytest tests/test_setup.py -v

# Run with coverage report
pytest --cov=src tests/
```

**Test Coverage:**
- ✅ System endpoint functionality
- ✅ Dataset loading and validation
- ✅ API documentation accessibility
- ✅ Data structure validation

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

Phase 2+ planned features:
- Question filtering by category/difficulty
- Random question selection
- User authentication
- Quiz session management
- Score tracking
- Database integration (PostgreSQL)
- Caching layer (Redis)
- Rate limiting
- Admin dashboard

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
**Status:** Phase 1 - Foundation Complete ✅

