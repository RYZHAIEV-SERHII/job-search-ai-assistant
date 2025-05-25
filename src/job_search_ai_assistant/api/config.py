"""API configuration module."""

import logging
from logging.config import dictConfig

# Logging configuration
log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        }
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {
        "job_search_ai": {
            "handlers": ["default"],
            "level": "INFO",
        }
    },
}


def setup_logging() -> None:
    """Configure logging for the API."""
    dictConfig(log_config)


logger = logging.getLogger("job_search_ai")
