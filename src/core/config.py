"""Configuration management for QuizForge API."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )
    
    APP_NAME: str = "QuizForge API"
    APP_VERSION: str = "1.0.0"
    DATA_PATH: str = "docs/questions.json"
    PORT: int = 8000


settings = Settings()

