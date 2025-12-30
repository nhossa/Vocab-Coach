"""
Simple logging configuration for production-ready app
Logs go to console (Docker will capture them)
"""
import logging
import os
import sys

# Get environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def setup_logging():
    """Configure basic logging for the application"""
    
    # Create logger
    logger = logging.getLogger()
    # Normalize LOG_LEVEL to numeric level without using deprecated helpers
    if LOG_LEVEL.isdigit():
        level = int(LOG_LEVEL)
    else:
        name_to_level = {
            "CRITICAL": 50, "FATAL": 50, "ERROR": 40, "WARNING": 30,
            "WARN": 30, "INFO": 20, "DEBUG": 10, "NOTSET": 0
        }
        level = name_to_level.get(LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(level)
    
    # Create formatter
    if ENVIRONMENT == "production":
        # Production: JSON-like format for CloudWatch
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
        )
    else:
        # Development: Human-readable format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    # Create console handler (explicitly write to stdout so Docker captures consistently)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    # Avoid adding duplicate handlers on repeated imports/reloads
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        logger.addHandler(console_handler)
    
    # Log startup message
    root_logger = logging.getLogger(__name__)
    root_logger.info(f"Logging initialized - Environment: {ENVIRONMENT}, Level: {LOG_LEVEL}")


# Initialize on import
setup_logging()
