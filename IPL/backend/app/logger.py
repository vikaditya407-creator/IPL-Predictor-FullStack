"""Logging configuration for IPL Predictor"""

import logging
import sys
from app.config import get_settings

try:
    from pythonjsonlogger import jsonlogger
    HAS_JSON_LOGGER = True
except ImportError:
    HAS_JSON_LOGGER = False


def setup_logger(name: str = "ipl_predictor") -> logging.Logger:
    """Setup logger with console handler (JSON if available)"""
    
    settings = get_settings()
    logger = logging.getLogger(name)
    logger.setLevel(settings.log_level)

    # Remove existing handlers
    logger.handlers = []

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    
    if HAS_JSON_LOGGER:
        # Use JSON formatter if available
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s"
        )
    else:
        # Use standard formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


# Create default logger
logger = setup_logger()
