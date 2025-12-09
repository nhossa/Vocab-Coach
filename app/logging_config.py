"""
Logging configuration for Vocab Coach
Provides JSON logging in production, regular logging in development
"""
import logging
import sys
import os
from pythonjsonlogger import jsonlogger


def setup_logging():
    """
    Configure logging based on ENVIRONMENT variable
    
    Development: Human-readable console output
    Production: JSON formatted logs for CloudWatch
    """
    environment = os.getenv('ENVIRONMENT', 'development')
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    if environment == 'production':
        # Production: JSON formatted logs
        formatter = jsonlogger.JsonFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s'
        )
    else:
        # Development: Human-readable format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured - Environment: {environment}, Level: {log_level}")


# Initialize logging when this module is imported
setup_logging()
