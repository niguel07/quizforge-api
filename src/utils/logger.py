"""Logging configuration for QuizForge API."""

import logging
import sys
from pathlib import Path


def setup_logger(name: str = "quizforge", level: int = logging.INFO) -> logging.Logger:
    """
    Set up and configure a logger.
    
    Args:
        name: Logger name.
        level: Logging level (default: INFO).
        
    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger


# Default logger instance
logger = setup_logger()

