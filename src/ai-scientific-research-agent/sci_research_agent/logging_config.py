import logging
import os
from pathlib import Path


def setup_logging():
    """Setup logging configuration with file handler."""
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create file handler
    log_file = log_dir / "sci_research_agent.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(file_handler)

    # Prevent logs from being displayed on console
    logger.propagate = False

    return logger
