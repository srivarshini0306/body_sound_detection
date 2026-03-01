import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

def setup_logger(name: str):
    """
    Sets up a logger with daily rotation.
    Logs are stored in the 'logs' directory.
    """
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Base log file name
    log_file = os.path.join(log_dir, f"{name}.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if not logger.handlers:
        # Timed Rotating File Handler (Daily at midnight)
        file_handler = TimedRotatingFileHandler(
            log_file, 
            when="midnight", 
            interval=1, 
            backupCount=30,
            encoding="utf-8"
        )
        file_handler.suffix = "%Y-%m-%d"
        file_handler.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Modern Formatter
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
