import logging
from pathlib import Path


def setup_logger() -> logging.Logger:
    
    # Project root directory
    project_root = Path(__file__).resolve().parent.parent

    # Create logs folder if it doesn't exist
    log_directory = project_root / "logs"
    log_directory.mkdir(exist_ok=True)

    log_file = log_directory / "application.log"

    logger = logging.getLogger("UniversalFileExtractor")

    # Prevent duplicate handlers
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Log to file
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Create a reusable logger instance
logger = setup_logger()