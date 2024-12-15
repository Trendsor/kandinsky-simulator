import logging
import sys
import os
from logging.handlers import RotatingFileHandler


def setup_logger(
        name: str,
        log_file: str = None,
        level: int = logging.INFO,
        file_log_level: int = logging.DEBUG,
        console_log_level: int = logging.INFO,
        max_bytes: int = 5 * 1024 * 1024,
        backup_count: int = 3,
):
    """
    Set up a logger with both console and optional file handlers.

    Args:
        name (str): Name of the logger.
        log_file (str, optional): Path to the log file. If None, no file logging is used.
        level (int): Overall logging level for the logger.
        file_log_level (int): Logging level for the file handler.
        console_log_level (int): Logging level for console handler.
        max_bytes (int): Maximum size of a log file before it is rotated.
        backup_count (int): Number of backup log files to keep after rotation.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_log_level)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)

    # Add console handler to the logger
    logger.addHandler(console_handler)

    if log_file:
        # Ensure the log file directory exists
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create file handler with rotation
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count
        )
        file_handler.setLevel(file_log_level)
        file_handler.setFormatter(formatter)

        # Add file handler to the logger
        logger.addHandler(file_handler)

    return logger
